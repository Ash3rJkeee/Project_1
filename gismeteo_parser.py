from bs4 import BeautifulSoup
import datetime
import smart_request


def month_from_ru_to_eng(month):
    # преобразует месяцы из ru в eng #
    out = ''
    if month == 'января': out = 'jan'
    if month == 'декабря': out = 'dec'
    if month == 'февраля': out = 'feb'
    if month == 'марта': out = 'mar'
    if month == 'апреля': out = 'apr'
    if month == 'мая': out = 'may'
    if month == 'июня': out = 'jun'
    if month == 'июля': out = 'jul'
    if month == 'августа': out = 'aug'
    if month == 'сентябся': out = 'sep'
    if month == 'октября': out = 'oct'
    if month == 'ноября': out = 'nov'
    if month == 'декабря': out = 'dec'
    return out


def transform_date(days):
    """функция преобразует даты из GISMETEO в нормальные даты"""
    month = ''
    for i in range(len(days)):
        days[i] = days[i].text
        days[i] = days[i].split('\n')[1].strip()
        if len(days[i].split(' ')) > 1:
            month = month_from_ru_to_eng(days[i].split(' ')[1])
            # print(month)
            days[i] = days[i].split(' ')[0]
        days[i] = days[i] + ' ' + month
        # print(days[i])
        days[i] = datetime.datetime.strptime(days[i], '%d %b')
        days[i] = days[i].replace(year=datetime.datetime.today().year)     # переприсвоение года
        days[i] = str(days[i].date())

    days = days[1:]
    # print(days)
    return days


def gismeteo_parser():
    global info, date, temps_night, temps_day

    # чтение страницы с инета при помощи модуля smart_request
    # html = smart_request.smart_get_html('https://www.gismeteo.ru/weather-moscow-4368/tomorrow/')
    html = smart_request.smart_get_html('https://www.gismeteo.ru/weather-moscow-4368/10-days/')


    # # чтение файла с указанием его кодировки. Обработка исключения,
    # #  если запускается на домашнем компе (другой путь файла)
    # try:
    #     html = open('C:\\Users\\a.ryadinskih\YandexDisk\YaDiscPyProjects\Project_1\\GISMETEO.htm',
    #                 encoding='utf-8').read()
    # except FileNotFoundError:
    #     html = open('C:\\Users\\Asher\\Desktop\\Project_1\\GISMETEO.htm', encoding='utf-8').read()

    # создание объекта Soup
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)


    # поиск тегов 'time' и 'span' нужных классов
    days = soup.findAll('div', class_='w_date')
    temps = soup.findAll('div', class_='value')

    # отсеивание лишних дат
    # days = days[::2]
    days = days[:10]

    # for i in days:
    #     print(i.text.strip())

    # отвеивание лишних температур
    temps = temps[1:10]

    # for i in temps:
    #     print(i.text)

    # заготовка списков
    date = transform_date(days)

    # temps_day = []
    # temps_night = []
    # info = []

    for i in range(len(temps)):
        # print(temps[i].text.split('+'))
        temps_day.append(temps[i].text.split('+')[1])
        temps_night.append(temps[i].text.split('+')[2])

    for i in [0, 1, 2]:
        # формирование переменной для вывода в GUI
        info.append(str(date[i]) + '  Тн =' + str(temps_night[i]) + '  Тд =' + str(temps_day[i]))
        print(info[i])


date = []
temps_day = []
temps_night = []
info = []


if __name__ == '__main__':
    gismeteo_parser()

