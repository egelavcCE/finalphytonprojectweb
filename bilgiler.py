from bs4 import BeautifulSoup
import requests

url = "https://www.defacto.com.tr/erkek-kazak"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# Sayfayı çekmek için GET isteği gönder
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "lxml")

# Ürün bilgilerini depolamak için boş listeler oluştur
products_link = []
products_isim = []
products_fiyat = []
en_çok_yorum_sayısı = 0
en_yüksek_yorumlu_ürün = ""

# Ürünlerin bulunduğu konteynerı bul
ürünler = soup.find('div', class_='row catalog-products--style catalog-products--style-v2')

# Eğer ürün bulunamazsa
if not ürünler:
    print("Ürünler bulunamadı.")
else:
    print(f"Bulunan ürün sayısı: {len(ürünler)}")  # Ürün sayısını yazdır

# Her bir ürün bağlantısını içeren div'leri bul
ürün_linkleri = ürünler.find_all_next("div", class_='catalog-products__item')

# Her bir ürün bağlantısını çek
for i in ürün_linkleri:
    link = i.find_next("div", class_='product-card').find_next("div", class_='product-card__info').find_next("div", class_='product-card__content').find_next("div", class_='product-card__details')
    
    # Ürün bağlantısını ve ismini çek
    for a in link:
        if a:
            link_a = a.find_next("h3", class_='product-card__title')
            if link_a:
                link_e = link.find_next("a")
                if link_e:
                    link_devam = link_e.get("href")
                    isim_devam = link_e.get("title")  
                    link_basi = "https://www.defacto.com.tr"
                    link_tamami = link_basi + link_devam
                    products_link.append(link_tamami)
                    products_isim.append(isim_devam)  
                    
    # Ürün fiyatını çek
    if a:
        fiyat = a.find_next("div", class_='product-card__price-list product-card__price-list--basket-discount')
        if fiyat:
            fiyat_text = fiyat.get_text(strip=True)
            products_fiyat.append(fiyat_text)
            
    # Ürün yorum sayısını çek
    if a:
        ef_deg = a.find_next("div", class_='product-card__rating d-inline-flex')
        if ef_deg:
            yorum = ef_deg.find_next("div", class_='product-card__rating-count')
            if yorum:
                efy_text = yorum.get_text(strip=True)
                efy_text = efy_text.replace("(", "").replace(")", "")
                ef_yorum = int(efy_text)
                # En çok yorum sayısına sahip ürünü bul
                if ef_yorum > en_çok_yorum_sayısı:
                    en_çok_yorum_sayısı = ef_yorum
                    en_yüksek_yorumlu_ürün = link_tamami

# Sonucu yazdır
print(f"En yüksek yorum sayısına sahip ürün: {en_yüksek_yorumlu_ürün} - Yorum Sayısı: {en_çok_yorum_sayısı}")

# Her bir ürünün bilgilerini yazdır
for i in range(len(products_link)):
    print(f"Ürün {i+1}")
    print(f"Link: {products_link[i]}")
    print(f"İsim: {products_isim[i]}")
    print(f"Fiyat: {products_fiyat[i]}\n")

            




         

   

      
   
