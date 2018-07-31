import requests
import smart_request
from bs4 import BeautifulSoup

picked_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
# html = requests.get('https://2ip.ru')
html = requests.get('https://2ip.ru', proxies={'http': '178.62.251.66:80'},
                    headers={'User-Agent': picked_agent})

# html = requests.get('http://sitespy.ru')

print(html.status_code)
# print(html.text)


soup = BeautifulSoup(html.text, 'html.parser')
# print(soup)

my_ip = soup.find('big', id='d_clip_button').text
print(my_ip)

spans = soup.findAll('span', class_='ip-info-entry__value')

# for i in spans:
#     print(i)

print(spans[0].text)
