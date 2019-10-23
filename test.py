import requests
from bs4 import BeautifulSoup

page = requests.get("https://yandex.ru/internet/")
page = page.text

soup = BeautifulSoup(page, "html.parser")

divs = soup.findAll("div", class_="list-info__renderer")
ip = divs[0].text
browser = divs[7].text

print(ip)
print(browser)