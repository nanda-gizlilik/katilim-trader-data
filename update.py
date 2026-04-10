import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://www.oyakyatirim.com.tr/piyasa-verileri/XKTUM"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

stocks = []

# ⚠️ tabloyu parse ediyoruz (site değişirse burası güncellenir)
for td in soup.find_all("td"):
    text = td.get_text(strip=True)

    if text.isupper() and 3 <= len(text) <= 6:
        stocks.append(text)

stocks = list(set(stocks))  # tekrarları sil

data = {
    "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "stocks": stocks
}

with open("katilim_stocks.json", "w") as f:
    json.dump(data, f, indent=2)

print("Güncellendi:", len(stocks))
