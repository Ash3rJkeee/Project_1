from bs4 import BeautifulSoup
import datetime


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


def transform_to_date(day):
    # функция преобразует дату из GISMETEO в нормальную дату
    day = str(day).replace('\n', '', 2)
    day = day.strip()
    day = day.split(',')[1]
    day = day[1:]
    day = day[:2] + " " + month_from_ru_to_eng(day.split(' ')[1])
    day = datetime.datetime.strptime(day, '%d %b')
    day = day.replace(year=datetime.datetime.today().year)     # переприсвоение года
    return day


# чтение файла с указанием его кодировки. Обработка исключения, если запускается на домашнем компе (другой путь файла)
try:
    html = open('C:\\Users\\a.ryadinskih\YandexDisk\YaDiscPyProjects\Project_1\\GISMETEO.htm', encoding='utf-8').read()
except FileNotFoundError:
    html = open('C:\\Users\\Asher\YandexDisk\YaDiscPyProjects\Project_1\\GISMETEO.htm', encoding='utf-8').read()


def gismeteo_parser():
    global info
    # создание объекта Soup
    soup = BeautifulSoup(html, 'html.parser')

    # поиск тегов 'time' и 'span' нужных классов
    days = soup.findAll('div', class_='eeac4214ba5')
    temps = soup.findAll('div', class_='c2c0b7a7a57')

    # отсеивание лишних дат
    days = days[::2]
    days = days[1:]


    # отвеивание лишних температур
    temps = temps[2:6]


    #
    # for i in temps:
    #     print(i)

    # заготовка списков
    date = []
    temps_day = []
    temps_night = []
    info = []

    for i in [0, 1]:
        date.append(transform_to_date(days[i].text))
        # print(date[i])
        temps_night.append(temps[i*2].text)
        temps_day.append(temps[i*2+1].text)
        info.append('Температура ' + str(date[i].date()) + ' составит ' + str(temps_day[i]) + ' ' + str(temps_night[i]))
        # print(info[i])


if __name__ == '__main__':
    gismeteo_parser()


# что парсим:
# дата
# <div class="eeac4214ba5">Пн, 11 июня </div>
# макс температура
# < div class ="c2c0b7a7a57" style="top: 0px; width: 50%;" > +19 < / div >
# мин температура
# < div class ="c2c0b7a7a57" style="top: 16px; width: 50%;" > +7 < / div >