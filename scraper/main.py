from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def run_scraper():
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.dropit.bm/shop/frozen_foods/d/22886624#!/?limit=96&page=1'  # 更換成你需要爬的頁面
    driver.get(url)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".fp-item-content"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('div.fp-item-content')

    for item in items:
        name_tag = item.select_one('div.fp-item-name span a')
        price_tag = item.select_one('div.fp-item-price span.fp-item-base-price')
        unit_tag = item.select_one('div.fp-item-price span.fp-item-size')
        product_name = name_tag.text.strip() if name_tag else 'N/A'
        product_price = price_tag.text.strip() if price_tag else 'N/A'
        product_unit = unit_tag.text.strip() if unit_tag else 'N/A'

        print(f'product_name: {product_name}, product_price: {product_price}, product_unit: {product_unit}')
        print('\n')

    driver.quit()

if __name__ == "__main__":
    run_scraper()
