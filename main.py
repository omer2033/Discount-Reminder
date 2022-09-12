import requests
import smtplib
from bs4 import BeautifulSoup
import lxml
MY_EMAIL = "@mail.com"
MY_PASSWORD = "password"
BUY_PRICE = 200

URL_PRODUCT = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url=URL_PRODUCT ,headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, "lxml")

price_tag = soup.find(name="span", class_ = "a-size-medium a-color-price priceBlockBuyingPriceString")
price = float(price_tag.getText().split("$")[1])
title_product = soup.find(id="productTitle").get_text().strip()

message = f"{title_product} is now {price}".encode('utf-8')
if price < 200:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="my@gmail.com",
                            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL_PRODUCT}"
                            )
