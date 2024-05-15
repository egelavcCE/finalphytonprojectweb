from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

# WebDriver'ı kurulumu
chrome_options = Options()
chrome_options.headless = True  # Tarayıcıyı başsız modda çalıştır (GUI olmadan)
driver = webdriver.Chrome(options=chrome_options)

# Veritabanına bağlan
conn = sqlite3.connect('reviews.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS reviews
    (link text, review_date text, review_text text, star_rating text)
''')

url = "https://www.defacto.com.tr/erkek-kazak"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# requests kütüphanesi kullanarak GET isteği gönder
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

# Ürün konteynerlarını bul
urunler = soup.find('div', class_='row catalog-products--style catalog-products--style-v2')
urun_linkleri = urunler.find_all_next("div", class_='catalog-products__item')

# Her bir ürün bağlantısı için döngü
for i, urun in enumerate(urun_linkleri, start=1):
    # Ürün başlığını ve bağlantısını bul
    link_a = urun.find_next("h3", class_='product-card__title')
    if link_a:
        link_e = link_a.find_next("a")
        if link_e:
            link_devam = link_e.get("href")
            link_tamami = "https://www.defacto.com.tr" + link_devam

            # Her bir ürün sayfasını ziyaret et
            driver.get(link_tamami)
            time.sleep(3)  # Sayfanın yüklenmesine izin vermek için bekleyin

            # Daha fazla yorum görmek için aşağı doğru kaydır
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Yorumların yüklenmesine izin vermek için bekleyin

            # "Tüm Yorumları Gör" düğmesini bulun ve tıklayın (varsa)
            try:
                wait = WebDriverWait(driver, 10)
                see_all_reviews_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-reviews__list--more')))
                while see_all_reviews_button.is_displayed():
                    driver.execute_script("arguments[0].click();", see_all_reviews_button)
                    time.sleep(5)  # İnternet hızınıza bağlı olarak zamanı ayarlayın
            except Exception as e:
                pass  # "Tüm Yorumları Gör" düğmesi bulunamazsa, tıklama olmadan devam et

            # Yorum bilgilerini çek
            reviews = driver.find_elements(By.CLASS_NAME, 'product-reviews__list--item')[:100]  # 100 yorumla sınırla
            for review in reviews:
                time.sleep(2)
                review_text = review.find_element(By.CLASS_NAME, 'product-reviews__list--description').text
                review_date = review.find_element(By.CLASS_NAME, 'product-reviews__list--date').text
                star_rating_class = review.find_element(By.CLASS_NAME, 'product-rating__star--percentage').get_attribute('class')
                star_rating = star_rating_class.split('-')[-1] if star_rating_class else None

                print(f"Ürün {i}")
                print(f"Bağlantı: {link_tamami}")
                print(f"İnceleme Tarihi: {review_date}")
                print(f"İnceleme Metni: {review_text}")
                print(f"Yıldız Derecesi: {star_rating}\n")
                c.execute("INSERT INTO reviews VALUES (?, ?, ?, ?)", (link_tamami, review_date, review_text, star_rating))
                # Değişiklikleri kaydet
                conn.commit()

# Bağlantıyı kapat
conn.close()

# WebDriver'ı kapat
driver.quit()