import os
import time
import requests
import instaloader
import re
import platform
from subprocess import check_output, CalledProcessError
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
        r = requests.get(url)
        r.raise_for_status()
        with open(os.path.join(folder, filename), "wb") as f:
            f.write(r.content)
        print(f"✅ Zapisano: {filename}")
    except Exception as e:
        print(f"❌ Błąd pobierania zdjęcia: {e}")

def get_chrome_version_windows():
    # Wyciągnij wersję Chrome na Windows przez PowerShell
    try:
        version = check_output(
            ['powershell', '-Command',
             '(Get-Item "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe").VersionInfo.ProductVersion']
        ).decode("utf-8").strip()
        return version
    except (CalledProcessError, FileNotFoundError):
        # Spróbuj 32-bitową wersję
        try:
            version = check_output(
                ['powershell', '-Command',
                 '(Get-Item "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe").VersionInfo.ProductVersion']
            ).decode("utf-8").strip()
            return version
        except Exception as e:
            print(f"❌ Nie udało się odczytać wersji Chrome: {e}")
            return None

def get_chrome_driver():
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Wymuszamy ścieżkę do Chrome
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")

    # Pobierz pełną wersję Chrome
    version_output = check_output(["google-chrome", "--version"]).decode("utf-8")
    # Przykładowy output: 'Google Chrome 136.0.7103.104'
    match = re.search(r"(\d+)\.(\d+)", version_output)
    if not match:
        raise Exception("Nie udało się odczytać wersji Chrome")

    major_version = match.group(1)  # np. "136"
    minor_version = match.group(2)  # np. "0"
    driver_version = f"{major_version}.{minor_version}"  # np. "136.0"

    service = Service(ChromeDriverManager(version=driver_version).install())
    return webdriver.Chrome(service=service, options=options)

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
        time.sleep(5)
        html = driver.page_source
        start = html.find('"avatarLarger":"')
        if start != -1:
            start += len('"avatarLarger":"')
            end = html.find('"', start)
            avatar_url = html[start:end].replace("\\u002F", "/").replace("\\u0026", "&")
            if "http" in avatar_url:
                download_image(avatar_url, folder, "tiktok.jpg")
                profile_data["tiktok"] = {
                    "url": f"https://www.tiktok.com/@{username}",
                    "name": username
                }
        else:
            print("❌ TikTok: Avatar nie został znaleziony.")
    except Exception as e:
        print(f"❌ TikTok error: {e}")

def twitch_pfp(username, folder, driver):
    print(f"\n🎮 Twitch: {username}")
    try:
        driver.get(f"https://www.twitch.tv/{username}")
        time.sleep(5)
        img_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
              "//*[@id='offline-channel-main-content']/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/a/div/div/img"))
        )
        img_url = img_element.get_attribute("src")
        if img_url:
            download_image(img_url, folder, "twitch.jpg")
            profile_data["twitch"] = {
                "url": f"https://www.twitch.tv/{username}",
                "name": username
            }
    except Exception as e:
        print(f"❌ Twitch error: {e}")

def run_scraper(instagram, tiktok, twitch, folder):
    global profile_data
    profile_data = {}
    OUTPUT_FOLDER = os.path.join("static", folder)
    ensure_output_folder(OUTPUT_FOLDER)
    driver = get_chrome_driver()

    if instagram:
        instagram_pfp(instagram, OUTPUT_FOLDER)
    if tiktok:
        tiktok_pfp(tiktok, OUTPUT_FOLDER, driver)
    if twitch:
        twitch_pfp(twitch, OUTPUT_FOLDER, driver)

    driver.quit()
    return profile_data
