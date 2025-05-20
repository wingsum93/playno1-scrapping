from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from cookie_helper import save_cookies, load_cookies
import csv
import json

def scrap_playno1(url):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 ...")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # ✅ 加載 cookies
    load_cookies(driver, url)

    driver.get(url)
    

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.fire_float"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('div.fire_float')
    result_list = []
    for item in items:
        image_tag = item.select_one('div.fire_imgbox a img')
        tiltle_tag = item.select_one('h3 a')
        date_tag = item.select_one('.fire_left')
        other_tag = item.select_one('.fire_right')

        image_url = image_tag.get('src') if image_tag and image_tag.has_attr('src') else 'N/A'
        title = tiltle_tag.text.strip() if tiltle_tag else 'N/A'
        date_string = date_tag.text.strip() if date_tag else 'N/A'
        other = other_tag.text.strip() if other_tag else 'N/A'

        # 將每個 item 放入 list（字典形式）
        result_list.append({
            'image_url': image_url,
            'title': title,
            'date': date_string,
            'other': other
        })
    driver.quit()
    return result_list

def save_to_json(data, filename='output.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['image_url', 'title', 'date', 'other'])
        writer.writeheader()
        writer.writerows(data)
def generate_urls(num_pages=1):
    if num_pages < 1:
        return []
    base_url = 'http://www.playno1.com/portal.php?mod=list&catid=23&page='
    return [f'{base_url}{page}' for page in range(1, num_pages + 1)]

if __name__ == "__main__":
    num_pages = 30
    urls = generate_urls(num_pages)

    all_data = []

    for url in urls:
        page_data = scrap_playno1(url)
        all_data.extend(page_data)  # 將每頁的項目加到主 list

    # 一次過輸出所有結果
    for item in all_data:
        print(item)
    save_to_csv(all_data)
