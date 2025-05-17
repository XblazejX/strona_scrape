from flask import Flask, render_template, request, jsonify
import os
import json
from scraper import run_scraper

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/check-folder', methods=['POST'])
def check_folder():
    data = request.get_json()
    folder = data.get('folder', '').strip()
    path = os.path.join('static', folder)
    exists = os.path.isdir(path)

    available = []
    if exists:
        files = os.listdir(path)
        mapping = {
            'instagram': 'instagram.jpg',
            'youtube':   'youtube.jpg',
            'tiktok':    'tiktok.jpg',
            'twitch':    'twitch.jpg'
        }
        for plat, fname in mapping.items():
            if fname in files:
                available.append(plat)

    return jsonify({'exists': exists, 'available': available})

@app.route('/run-scraper', methods=['POST'])
def run_scraper_route():
    data = request.get_json()
    folder = data.get('folder').strip()
    instagram = data.get('instagram')
    tiktok    = data.get('tiktok')
    twitch    = data.get('twitch')

    # Uruchom scraper i zbierz dane
    profile_data = run_scraper(instagram, tiktok, twitch, folder)

    # Upewnij się, że folder istnieje
    output_dir = os.path.join('static', folder)
    os.makedirs(output_dir, exist_ok=True)

    # Zapisz plik dane.js do katalogu static/{folder}/dane.js
    js_path = os.path.join(output_dir, 'dane.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('window.profileData = ')
        json.dump(profile_data, f, ensure_ascii=False, indent=2)
        f.write(';')


    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(debug=True)
