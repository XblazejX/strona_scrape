from flask import Flask, render_template, request, jsonify
import os
import json
from scraper import run_scraper

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper_route():
    data = request.get_json()

    instagram = data.get('instagram')
    tiktok = data.get('tiktok')
    twitch = data.get('twitch')

    # Uruchom scraper z danymi przekazanymi przez frontend
    profile_data = run_scraper(instagram, tiktok, twitch)

    # Zwróć dane profilowe jako JSON
    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(debug=True)
