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

# ==========================
# 💡 KONFIGURACJA
OUTPUT_FOLDER = "static/zdjecia"  # Folder, do którego będą zapisywane zdjęcia
profile_data = {}  # Zmienna na dane profilowe

def ensure_output_folder():
    """Tworzy folder, jeśli nie istnieje."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_image(url, filename):
    """Pobiera obrazek z URL i zapisuje go do pliku."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(os.path.join(OUTPUT_FOLDER, filename), "wb") as f:
            f.write(r.content)
        print(f"✅ Zapisano: {filename}")
    except Exception as e:
        print(f"❌ Błąd pobierania zdjęcia: {e}")

def get_chrome_driver():
    """Inicjalizuje sterownik Selenium za pomocą automatycznie pobranego ChromeDrivera."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def instagram_pfp(username):
    """Pobiera zdjęcie profilowe z Instagrama przy użyciu Instaloadera."""
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
        download_image(profile.profile_pic_url, "instagram.jpg")
        profile_data["instagram"] = {
            "url": f"https://instagram.com/{username}",
            "name": f"{username}"
        }
    except Exception as e:
        print(f"❌ Instagram error: {e}")

def tiktok_pfp(username, driver):
    """Pobiera zdjęcie profilowe z TikToka przy użyciu Selenium."""
    print(f"\n🎵 TikTok: {username}")
    try:
        driver.get(f"https://www.tiktok.com/@{username}")
        time.sleep(5)
        html = driver.page_source
        start = html.find('"avatarLarger":"')
        if start != -1:
            start += len('"avatarLarger":"')
            end = html.find('"', start)
            avatar_url = html[start:end]
            avatar_url = avatar_url.replace("\\u002F", "/").replace("\\u0026", "&")
            if "http" in avatar_url:
                download_image(avatar_url, "tiktok.jpg")
                profile_data["tiktok"] = {
                    "url": f"https://www.tiktok.com/@{username}",
                    "name": f"{username}"
                }
            else:
                print("❌ TikTok: Nie znaleziono prawidłowego URL zdjęcia.")
        else:
            print("❌ TikTok: Avatar nie został znaleziony w kodzie strony.")
    except Exception as e:
        print(f"❌ TikTok error: {e}")

def twitch_pfp(username, driver):
    """Pobiera zdjęcie profilowe z Twitcha przy użyciu Selenium i XPath."""
    print(f"\n🎮 Twitch: {username}")
    try:
        driver.get(f"https://www.twitch.tv/{username}")
        time.sleep(5)
        # XPath z Twojego zapytania
        img_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='offline-channel-main-content']/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/a/div/div/img"))
        )
        img_url = img_element.get_attribute("src")
        if img_url:
            download_image(img_url, "twitch.jpg")
            profile_data["twitch"] = {
                "url": f"https://www.twitch.tv/{username}",
                "name": f"{username}"
            }
        else:
            print("❌ Twitch: Nie znaleziono zdjęcia profilowego.")
    except Exception as e:
        print(f"❌ Twitch error: {e}")

def run_scraper(instagram, tiktok, twitch):
    """Uruchamia proces zbierania danych i zwraca je do aplikacji webowej."""
    ensure_output_folder()
    driver = get_chrome_driver()

    if instagram:
        instagram_pfp(instagram)
    if tiktok:
        tiktok_pfp(tiktok, driver)
    if twitch:
        twitch_pfp(twitch, driver)

    driver.quit()

    return profile_data
