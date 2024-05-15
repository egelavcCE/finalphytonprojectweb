from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# WebDriver'ı kurulumu
driver = webdriver.Chrome()

url = "https://www.defacto.com.tr/erkek-kazak"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# requests kütüphanesi kullanarak GET isteği gönder
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")  # Parser 'html.parser' olarak değiştirildi

en_cok_yildizli = 0.0
en_yuksek_yildizli_urun = None

# Ürün konteynerlarını bul
urunler = soup.find('div', class_='row catalog-products--style catalog-products--style-v2')
urun_linkleri = urunler.find_all_next("div", class_='catalog-products__item')

# Her bir ürün bağlantısı için döngü
for i in urun_linkleri:
    # Ürün başlığını ve bağlantısını bul
    link_a = i.find_next("h3", class_='product-card__title')
    if link_a:
        link_e = link_a.find_next("a")
        if link_e:
            link_devam = link_e.get("href")
            link_tamami = "https://www.defacto.com.tr" + link_devam

            # Her bir ürün sayfasını ziyaret et
            driver.get(link_tamami)

            try:
                # Yıldız derecesi değerini al
                ef_begeni = driver.find_element(By.CSS_SELECTOR, ".product-rating__star--percentage")
                style_attribute = ef_begeni.get_attribute("style")
                yildiz_deg = int(style_attribute.split(":")[1].replace("%", "").replace(";","").strip())
                
                if yildiz_deg > en_cok_yildizli:
                    en_cok_yildizli = yildiz_deg
                    en_yuksek_yildizli_urun = link_tamami
            except:
                continue

# Sonucu yazdır
print(f"En yüksek yıldız değerine sahip ürün: {en_yuksek_yildizli_urun} - Değeri: {en_cok_yildizli}")

# WebDriver'ı kapat
driver.quit()