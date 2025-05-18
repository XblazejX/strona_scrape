import os
import time
import requests
import instaloader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

profile_data = {}

def ensure_output_folder(path):
    os.makedirs(path, exist_ok=True)

def download_image(url, folder, filename):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"✅ Zapisano: {filename}")
    except Exception as e:
        print(f"❌ Błąd pobierania zdjęcia {filename}: {e}")

def get_chrome_driver():
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # wymuszona ścieżka
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")

    # Ustaw wersję chromedriver kompatybilną z Twoim Chrome (dostosuj w razie potrzeby)
    driver_version = "124.0.6367.60"
    service = Service(ChromeDriverManager(version=driver_version).install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def instagram_pfp(username, folder):
    print(f"\n📸 Instagram: {username}")
    try:
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            save_metadata=False,
            compress_json=False
        )
        profile = instaloader.Profile.from_username(loader.context, username)
        download_image(profile.profile_pic_url, folder, "instagram.jpg")
        profile_data["instagram"] = {
            "url": f"https://instagram.com/{username}",
            "name": username
        }
    except Exception as e:
        print(f"❌ Instagram error: {e}")

def tiktok_pfp(username, folder, driver):
    print(f"\n🎵 TikTok: {username}")
    try:
        driver.get(f"https://www.tiktok.com/@{username}")
        time.sleep(5)  # można zastąpić lepszym oczekiwaniem, ale TikTok bywa kapryśny
        html = driver.page_source
        start = html.find('"avatarLarger":"')
        if start != -1:
            start += len('"avatarLarger":"')
            end = html.find('"', start)
            avatar_url = html[start:end].replace("\\u002F", "/").replace("\\u0026", "&")
            if avatar_url.startswith("http"):
                download_image(avatar_url, folder, "tiktok.jpg")
                profile_data["tiktok"] = {
                    "url": f"https://www.tiktok.com/@{username}",
                    "name": username
                }
            else:
                print("❌ TikTok: Nieprawidłowy URL avatara.")
        else:
            print("❌ TikTok: Avatar nie został znaleziony.")
    except Exception as e:
        print(f"❌ TikTok error: {e}")

def twitch_pfp(username, folder, driver):
    print(f"\n🎮 Twitch: {username}")
    try:
        driver.get(f"https://www.twitch.tv/{username}")
        # XPath do avatara możesz dostosować, jeśli się zmienił layout strony
        img_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
              "//*[@id='offline-channel-main-content']/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/a/div/div/img"))
        )
        img_url = img_element.get_attribute("src")
        if img_url and img_url.startswith("http"):
            download_image(img_url, folder, "twitch.jpg")
            profile_data["twitch"] = {
                "url": f"https://www.twitch.tv/{username}",
                "name": username
            }
        else:
            print("❌ Twitch: Nie znaleziono poprawnego URL avatara.")
    except Exception as e:
        print(f"❌ Twitch error: {e}")

def run_scraper(instagram, tiktok, twitch, folder):
    global profile_data
    profile_data = {}
    OUTPUT_FOLDER = os.path.join("static", folder)
    ensure_output_folder(OUTPUT_FOLDER)
    
    driver = None
    try:
        driver = get_chrome_driver()
        if instagram:
            instagram_pfp(instagram, OUTPUT_FOLDER)
        if tiktok:
            tiktok_pfp(tiktok, OUTPUT_FOLDER, driver)
        if twitch:
            twitch_pfp(twitch, OUTPUT_FOLDER, driver)
    finally:
        if driver:
            driver.quit()
    return profile_data
