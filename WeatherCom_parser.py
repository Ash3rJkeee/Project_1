"""Модуль парсинга с "https://weather.com/ru-RU/weather/5day/l/RSXX0063:1:RS"
 Порядок вывода температур:максимум ночной , затем максимум дневной того же числа.
 (ночь - день)"""

from bs4 import BeautifulSoup
import datetime
import smart_request


def month_from_ru_to_eng(month):
    """ преобразует месяцы из ru в eng """
    out = ''
    if month == 'ЯНВ': out = 'jan'
    if month == 'ФЕВ': out = 'feb'
    if month == 'МАР': out = 'mar'
    if month == 'АПР': out = 'apr'
    if month == 'МАЙ': out = 'may'
    if month == 'ИЮН': out = 'jun'
    if month == 'ИЮЛ': out = 'jul'
    if month == 'АВГ': out = 'aug'
    if month == 'СЕН': out = 'sep'
    if month == 'ОКТ': out = 'oct'
    if month == 'НОЯ': out = 'nov'
    if month == 'ДЕК': out = 'dec'
    return out


def transform_to_date(day):
    """функция преобразует дату из вида "20 июня"  в дату формата datetime"""
    day = day.split(' ')[1] + " " + month_from_ru_to_eng(day.split(' ')[0])
    day = datetime.datetime.strptime(day, '%d %b')
    day = day.replace(year=datetime.datetime.today().year)     # переприсвоение года
    return day
    # print(day.date())

def parser():
    global info, date, temps_night, temps_day
    html = smart_request.smart_get_html('https://weather.com/ru-RU/weather/5day/l/RSXX0063:1:RS')
    soup = BeautifulSoup(html, 'html.parser')

    # формирование списка дат
    days = soup.findAll('span', class_='day-detail clearfix')
    date = []
    for i in days:
        date.append(i.text)
        # print(date[-1])
    # print(date)

    date = date[1:4]

    # преобразование в нормальный формат даты datetime
    for i in range(len(date)):
        date[i] = transform_to_date(date[i])
        date[i] = date[i].date()
        # print(date[i])

    # формирование списка температур
    tds = soup.findAll('td', class_='temp', headers='hi-lo')

    # отсеивание сегодняшней даты
    tds = tds[1:]

    temps = []
    # temps_day = []
    # temps_night = []

    for i in range(len(tds)):
        temps.append(tds[i].text)
        # print(temps[i])
        temps_day.append(temps[i].split('°')[0])
        temps_night.append(temps[i].split('°')[1])
        temps_night[i] = temps_night[i].split('°')[0]      # удаление лишнего символа градуса в конце

    info = []

    # формирование переменной для вывода в GUI
    for i in [0, 1, 2]:
        info.append(str(date[i]) + '  Тн =' + str(temps_night[i]) + '  Тд =' + str(temps_day[i]))
        print(info[i])


date = []
temps_day = []
temps_night = []
info = []

if __name__ == '__main__':
    parser()


