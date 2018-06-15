import requests
from bs4 import BeautifulSoup


def month_from_ru_to_eng(month):
    out = ''
    if month == 'января': out = 'jan'
    if month == 'декабря': out = 'dec'
    if month == 'февраля': out = 'feb'
    if month == 'марта': out = 'mar'
    if month == 'апреля': out = 'apr'
    if month == 'мая': out = 'may'
    if month == 'июня': out = 'jun'
    if month == 'июня': out = 'jul'
    if month == 'августа': out = 'aug'
    if month == 'сентябся': out = 'sep'
    if month == 'октября': out = 'oct'
    if month == 'ноября': out = 'nov'
    if month == 'декабря': out = 'dec'
    return out


# a = month_from_ru_to_eng('января')
# print(a)


html = requests.get('http://sitespy.ru/my-ip').text
soup = BeautifulSoup(html, 'html.parser')
ip = soup.find('span', class_='ip').text.strip()
user_agent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()

print('my ip: ', ip)
print(user_agent)