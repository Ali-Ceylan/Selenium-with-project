from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys

# Chrome tarayıcı için seçenekler belirliyoruz
chromedriver_path = "C:/Users/Q/Desktop/chromedriver-win64/chromedriver.exe"

# Chrome seçenekleri
co = webdriver.ChromeOptions()
co.add_argument("--incognito")  # Gizli mod

# ChromeDriver servisini başlat
service = Service(chromedriver_path)

# WebDriver başlatılıyor
driver = webdriver.Chrome(service=service, options=co)

# Fiyatları çekmek için fonksiyon
def get_price(symbol_url, price_xpath):
    driver.get(symbol_url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    try:
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, price_xpath))
        ).text
        return price
    except Exception as e:
        print(f"{symbol_url} fiyatı alınamadı: {e}")
        return None
def write_to_html(btc, altin, euro, dolar, bist100):
    with open("piyasalar.html", "w", encoding="utf-8") as file:
        file.write(f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Piyasa Verileri</title>
        </head>
        <body>
            <h1>Piyasa Verileri</h1>
            <p><strong>BTC Fiyatı:</strong> {btc}</p>
            <p><strong>Altın Fiyatı:</strong> {altin}</p>
            <p><strong>Euro Fiyatı:</strong> {euro}</p>
            <p><strong>Dolar Fiyatı:</strong> {dolar}</p>
            <p><strong>BIST100 Fiyatı:</strong> {bist100}</p>
        </body>
        </html>
        """)


try:
    while True:
        # BTC Fiyatı
        btc_fiyat = get_price("https://tr.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT", 
                              "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]")
        sleep(3)
        # Altın Fiyatı (XAUUSD)
        altin_fiyat = get_price("https://tr.tradingview.com/chart/?symbol=FX_IDC%3AXAUTRYG", 
                                "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]")
        sleep(3)
        # Euro Fiyatı (EURTRY)
        euro_fiyat = get_price("https://tr.tradingview.com/chart/?symbol=FX%3AEURTRY", 
                               "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]")
        sleep(3)
        # Dolar Fiyatı (USDTRY)
        dolar_fiyat = get_price("https://tr.tradingview.com/chart/?symbol=FX%3AUSDTRY", 
                                "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]")
        sleep(3)
        # BIST100 Fiyatı
        bist100_fiyat = get_price("https://tr.tradingview.com/chart/?symbol=BIST%3AXU100", 
                                  "/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]")
        sleep(3)
        # Sonuçları ekrana yazdır
        if btc_fiyat:
            print(f"BTC Fiyatı: {btc_fiyat}")
        if altin_fiyat:
            print(f"Altın Fiyatı: {altin_fiyat}")
        if euro_fiyat:
            print(f"Euro Fiyatı: {euro_fiyat}")
        if dolar_fiyat:
            print(f"Dolar Fiyatı: {dolar_fiyat}")
        if bist100_fiyat:
            print(f"BIST100 Fiyatı: {bist100_fiyat}")

        # 10 saniye bekleyip tekrar başla

        if btc_fiyat and altin_fiyat and euro_fiyat and dolar_fiyat and bist100_fiyat:
            write_to_html(btc_fiyat, altin_fiyat, euro_fiyat, dolar_fiyat, bist100_fiyat)
            print("Fiyatlar başarıyla HTML dosyasına yazıldı!")
        sleep(10)
finally:
    driver.quit()
