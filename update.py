import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL
url = "https://www.oyakyatirim.com.tr/piyasa-verileri/XKTUM"

# DEFAULT LİSTE (FALLBACK)
default_stocks = [
    "ASELS", "THYAO", "TUPRS", "EREGL", "SASA", "KONTR", "KRDMD", "ALARK"
]

stocks = []

try:
    # HEADER EKLE (BOT ENGELİ AŞMA)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    # REQUEST (TIMEOUT İLE)
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    print("SITE STATUS OK")
    print("HTML PREVIEW:", response.text[:300])

    soup = BeautifulSoup(response.text, "html.parser")

    # PARSE
    for td in soup.select("td"):
        text = td.get_text(strip=True)

        if (
            text.isupper()
            and text.isalpha()
            and 3 <= len(text) <= 6
        ):
            stocks.append(text)

    # TEKRARLARI SİL + SIRALA
    stocks = sorted(list(set(stocks)))

    # BOŞSA FALLBACK
    if len(stocks) < 5:
        print("PARSE BAŞARISIZ -> DEFAULT KULLANILDI")
        stocks = default_stocks

except Exception as e:
    print("HATA:", e)
    print("DEFAULT LİSTE KULLANILDI")
    stocks = default_stocks

# JSON YAZ
data = {
    "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "stocks": stocks
}

with open("katilim_stocks.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("GÜNCELLENDİ ->", len(stocks), "hisse")
