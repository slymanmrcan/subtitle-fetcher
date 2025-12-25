import os
import re
import uuid
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

# Temporary directory for subtitles
TEMP_DIR = "temp_subs"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def clean_subtitles(raw_text):
    """
    Cleans WebVTT/SRT noise and returns a readable paragraph format with intelligent breaks.
    """
    # 1. Remove VTT/SRT headers and metadata
    lines = raw_text.splitlines()
    cleaned_lines = []
    
    # Simple regex for timestamps: 00:00:00.000 --> 00:00:00.000
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3})|(\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}\.\d{3})')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, headers, and timestamps
        if not line or line.upper() == "WEBVTT" or "Kind:" in line or "Language:" in line or timestamp_pattern.search(line):
            continue
            
        # 2. Remove HTML-like tags (e.g., <c>, <br>)
        line = re.sub(r'<[^>]+>', '', line)
        
        # 3. Basic cleanup
        if line:
            cleaned_lines.append(line)

    # 4. Deduplicate consecutive identical lines (YouTube progressive subs often repeat)
    final_lines = []
    for line in cleaned_lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)

    # 5. Join into paragraphs with intelligent breaks
    paragraphs = []
    current_paragraph = []
    
    for line in final_lines:
        current_paragraph.append(line)
        
        # Add paragraph break after sentences ending with . ! ? followed by capital letter
        # or after every ~5-7 lines for better readability
        if (line.endswith(('.', '!', '?')) or len(current_paragraph) >= 6):
            paragraph_text = ' '.join(current_paragraph)
            paragraph_text = re.sub(r'\s+', ' ', paragraph_text).strip()
            paragraphs.append(paragraph_text)
            current_paragraph = []
    
    # Add any remaining lines
    if current_paragraph:
        paragraph_text = ' '.join(current_paragraph)
        paragraph_text = re.sub(r'\s+', ' ', paragraph_text).strip()
        paragraphs.append(paragraph_text)
    
    # Join paragraphs with double newline for clear separation
    return '\n\n'.join(paragraphs)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_subtitles():
    data = request.json
    video_url = data.get('url')
    selected_lang = data.get('lang', 'tr')
    selected_browser = data.get('browser') # Optional: chrome, safari, firefox, brave, etc.
    
    if not video_url:
        return jsonify({'error': 'URL gerekli'}), 400

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(TEMP_DIR, f"{unique_id}.%(ext)s")

    # Priority list: selected lang -> tr -> en
    langs = [selected_lang]
    if 'tr' not in langs: langs.append('tr')
    if 'en' not in langs: langs.append('en')

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': langs,
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
    }

    # If a browser is selected, use it to fetch cookies
    if selected_browser and selected_browser != 'none':
        print(f"[DEBUG] Trying to use cookies from: {selected_browser}")
        ydl_opts['cookiesfrombrowser'] = (selected_browser,)
    else:
        print("[DEBUG] No browser selected, using cookiefile or no cookies")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            
            # Find the best match subtitle file
            # yt-dlp saves as unique_id.lang.vtt
            all_files = os.listdir(TEMP_DIR)
            found_file = None
            
            # Search order: exact lang, then others in priority
            for l in langs:
                potential = [f for f in all_files if f.startswith(unique_id) and f'.{l}.' in f]
                if potential:
                    found_file = os.path.join(TEMP_DIR, potential[0])
                    break
            
            # Fallback to ANY subtitle found for this request if none of the priority ones exist
            if not found_file:
                for f in all_files:
                    if f.startswith(unique_id):
                        found_file = os.path.join(TEMP_DIR, f)
                        break
            
            if not found_file:
                return jsonify({'error': 'Bu vidoda çekilebilecek (otomatik veya manuel) alt yazı bulunamadı. Lütfen videonun alt yazısı olduğundan emin olun.'}), 404

            with open(found_file, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            cleaned_text = clean_subtitles(raw_content)
            
            # Clean up all temp files for this request
            for f in all_files:
                if f.startswith(unique_id):
                    os.remove(os.path.join(TEMP_DIR, f))
            
            return jsonify({
                'title': info.get('title', 'Video'),
                'content': cleaned_text
            })

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return jsonify({'error': 'HTTP 429: YouTube tarafından geçici olarak engellendiniz. Lütfen bir süre bekleyin veya cookies.txt yöntemini deneyin.', 'code': 429}), 429
        return jsonify({'error': error_msg}), 500

@app.route('/download', methods=['POST'])
def download_txt():
    content = request.json.get('content')
    title = request.json.get('title', 'altyazi')
    if not content:
        return "İçerik yok", 400
    
    # Create temp file to send
    filename = f"{title}.txt"
    filepath = os.path.join(TEMP_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
