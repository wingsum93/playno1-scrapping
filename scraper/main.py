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
    options.add_argument("user-agent=Mozilla/5.0 ...")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'http://www.playno1.com/portal.php?mod=list&catid=23&page=1'  # 更換成你需要爬的頁面
    driver.get(url)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.fire_float"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('div.fire_float')

    for item in items:
        image_tag = item.select_one('div.fire_imgbox a img')
        tiltle_tag = item.select_one('h3 a')
        date_tag = item.select_one('.fire_left')
        other_tag = item.select_one('.fire_right')

        image_url = image_tag.get('src') if image_tag and image_tag.has_attr('src') else 'N/A'
        title = tiltle_tag.text.strip() if tiltle_tag else 'N/A'
        date_string = date_tag.text.strip() if date_tag else 'N/A'
        other = other_tag.text.strip() if other_tag else 'N/A'

        print(f'image_url: {image_url}, title: {title}, date_string: {date_string}, other: {other}')
        print('\n')

    driver.quit()

if __name__ == "__main__":
    run_scraper()
