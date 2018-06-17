import requests
from bs4 import BeautifulSoup
import smart_request

html = smart_request.smart_get_html('http://www.gismeteo.ru/weather-moscow-4368/tomorrow/')

# html = requests.get('https://www.gismeteo.ru/weather-moscow-4368/tomorrow/').text

# создание объекта Soup
soup = BeautifulSoup(html, 'html.parser')

# поиск тегов 'time' и 'span' нужных классов
days = soup.findAll('div', class_='c43595192c3')
temps = soup.findAll('div', class_='aa03387e397')

print(days)
print(temps)

# отсеивание лишних дат
days = days[::2]
days = days[1:]

for i in days:
    print(i)

# отвеивание лишних температур
temps = temps[2:6]

for i in temps:
    print(i)
