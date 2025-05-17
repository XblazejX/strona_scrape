from flask import Flask, render_template, request, jsonify
import os
import json
from scraper import run_scraper  # teraz przyjmuje 4. parametr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper_route():
    data = request.get_json()
    folder = data.get('folder')            # nowy parametr
    instagram = data.get('instagram')
    tiktok = data.get('tiktok')
    twitch = data.get('twitch')

    # Uruchom scraper z przekazaną nazwą folderu
    profile_data = run_scraper(instagram, tiktok, twitch, folder)

    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(debug=True)
