# cookie_helper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
import time

COOKIE_FILE = 'cookies.pkl'

def save_cookies(driver, cookie_file=COOKIE_FILE):
    cookies = driver.get_cookies()
    with open(cookie_file, 'wb') as f:
        pickle.dump(cookies, f)
    print(f"✅ Cookies saved to {cookie_file}")

def load_cookies(driver, url, cookie_file=COOKIE_FILE):
    if not os.path.exists(cookie_file):
        print("⚠️ No cookie file found.")
        return

    driver.get(url)  # 必須先訪問 domain，否則 cookies 無法加入
    time.sleep(2)  # 確保頁面 load 完

    with open(cookie_file, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

    print(f"✅ Cookies loaded from {cookie_file}")


if __name__ == "__main__":
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 ...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('http://www.playno1.com/')
    # WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.portal_block_summary"))
    # )
    input("⏳ Press Enter after you finish login...")  # 等你 login


    save_cookies(driver)
    driver.quit()

