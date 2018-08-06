import requests
from bs4 import BeautifulSoup


url = 'https://yandex.ru/internet/'
proxies = {'https': 'socks5://Ash3rjkeee:Sfrffccc2511@109.248.166.10:1051'}

picked_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.143 Safari/537.36'

html = requests.get(url, proxies=proxies, headers={'User-Agent': picked_agent})
print('Статус соединения: ', html.status_code)

soup = BeautifulSoup(html.text, 'html.parser')

ip = soup.find('span', class_='info__value info__value_type_ipv4').text
print(ip)

browser = soup.find('span', classs_='info__value info__value_type_browser')
print('browser', browser)

os = soup.find('span', class_='info__value info__value_type_operating-system').text
print('OS: ', os)


div_browser = soup.find('div', class_='info__group info__group_type_browser')
print(div_browser.text)

# user_agent = soup.find('span', class_='info__value info__value_type_userAgent')
# print('UA: ', user_agent)

# div = soup.find('div', class_="info__group info__group_type_general")
# print(div.text)


# url = 'https://2ip.ru'
# html = requests.get(url, proxies=proxies, headers={'User-Agent': picked_agent})
# print('Статус соединения: ', html.status_code)
#
# soup = BeautifulSoup(html.text, 'html.parser')
#
# main_block = soup.find('table', id='main-info-block')
# # print(main_block)
#
# spans = main_block.findAll('span', class_='ip-info-entry__value')
#
# # for i in spans:
# #     print(i.text.strip())
#
# ip = spans[0].text.strip()
# os = spans[1].text.strip()
# browser = spans[2].text.strip()
# place = spans[3].text.strip()
#
# print('IP: ', ip)
# print('OS: ', os)
# print('Browser: ', browser)
# print('U from: ', place)