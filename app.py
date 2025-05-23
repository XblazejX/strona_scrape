from flask import Flask, render_template, request, jsonify
import os
import json
import shutil
from scraper import run_scraper
import shutil

app = Flask(__name__)

@app.route('/delete-folder', methods=['POST'])
def delete_folder():
    data = request.get_json()
    folder = data.get('folder', '').strip()
    path = os.path.join('static', folder)

    if os.path.isdir(path):
        import shutil
        shutil.rmtree(path)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Folder not found'}), 404

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
    print(f"[DEBUG] Folder '{folder}' istnieje: {exists}, dostępne platformy: {available}")
    return jsonify({'exists': exists, 'available': available})

@app.route('/run-scraper', methods=['POST'])
def run_scraper_route():
    data = request.get_json()
    folder = data.get('folder').strip()
    instagram = data.get('instagram')
    tiktok    = data.get('tiktok')
    twitch    = data.get('twitch')

    output_dir = os.path.join('static', folder)
    os.makedirs(output_dir, exist_ok=True)
    print(f"[DEBUG] Tworzenie / czyszczenie folderu: {output_dir}")

    # Usuń stare pliki zdjęć i dane.js
    for platform in ['instagram', 'youtube', 'tiktok', 'twitch']:
        img_path = os.path.join(output_dir, f"{platform}.jpg")
        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"[DEBUG] Usunięto stary plik: {img_path}")

    js_path = os.path.join(output_dir, 'dane.js')
    if os.path.exists(js_path):
        os.remove(js_path)
        print(f"[DEBUG] Usunięto stary plik: {js_path}")

    # Uruchom scraper
    profile_data = run_scraper(instagram, tiktok, twitch, folder)

    # Zapisz dane.js
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('window.profileData = ')
        json.dump(profile_data, f, ensure_ascii=False, indent=2)
        f.write(';')
    print(f"[DEBUG] Zapisano dane.js w: {js_path}")
    print(f"[DEBUG] Zawartość folderu po scrapingu: {os.listdir(output_dir)}")

    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(host="::", port=5000, debug=True, use_reloader=True)
