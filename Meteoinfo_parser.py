"""Модуль парсинга с "https://meteoinfo.ru/forecasts/russia/moscow-area/moscow"
 Порядок вывода температур: максимум дневной, затем максимум ночной того же числа.
 (день - ночь)"""

from bs4 import BeautifulSoup
import datetime
import smart_request


def month_from_ru_to_eng(month):
    """ преобразует месяцы из ru в eng """
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


def delete_name_of_day(day):
    """Удаление дня недели из даты"""
    day = str(day)
    for i in range(len(day)):
        if day[i].isdigit():
            day = day.split(day[i - 1])[1]
            break
    return day


def transform_to_date(day):
    # функция преобразует дату из вида 20 июня  в нормальную дату
    day = day.split(' ')[0] + " " + month_from_ru_to_eng(day.split(' ')[1])
    day = datetime.datetime.strptime(day, '%d %b')
    day = day.replace(year=datetime.datetime.today().year)     # переприсвоение года
    # print(day.date())
    return day

def parser():
    global info
    # чтение страницы с инета при помощи модуля smart_request
    html = smart_request.smart_get_html('https://meteoinfo.ru/hmc-output/forecast/tab_1.php')

    # чтение сохраненного файла
    # html = open('C:\\Users\\a.ryadinskih\\Desktop\\meteoinfo.ru\\meteoinfo.htm', encoding='utf-8').read()

    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', id='div_print_0')

    tds = div.findAll('td', class_='td_short_gr')

    dates = []
    for td in tds:
        dates.append(td.text)
        # print(dates[-1])

    # отбрасываем лишние дни
    dates = dates[2:4]


    for i in [0, 1]:
        dates[i] = transform_to_date(delete_name_of_day(dates[i]))

    # нужно для обхода зарезервированного питоном слова "data-toggle"
    kwargs = {'data-toggle': 'tooltip'}

    trs = div.findAll('span', kwargs)


    temps = []
    for tr in trs:
        temps.append(tr.text)
        # print(temps[-1])

    temps_day = temps[:6]    # отсеил дневные
    temps_day = temps_day[1:]     # отсеил сегодняшнюю дату
    temps_night = temps[6:]         # отсеил ночные
    # temps_night = temps_night[1:]   # отсеил сегодняшнюю дату

    # print(temps_night)
    #     # print(temps_day)

    # отсечение лишних символов, преобразование в число и вычисление средней максимальнй температуры за сутки период
    # (особенность meteoinfo.ru )
    for i in range(len(temps_day)):
        temps_day[i] = temps_day[i].split('°')[0]
        temps_day[i] = (int(temps_day[i].split('..')[0]) + int(temps_day[i].split('..')[1]))/2

    # отсечение лишних символов, преобразование в число и вычисление средней минимальной температуры за сутки период
    # (особенность meteoinfo.ru )
    for i in range(len(temps_night)):
        temps_night[i] = temps_night[i].split('°')[0]
        temps_night[i] = (int(temps_night[i].split('..')[0]) + int(temps_night[i].split('..')[1]))/2

    info = []
    for i in [0, 1]:
        info.append('Температура ' + str(dates[i].date()) + ' составит ' + str(temps_night[i]) + ' ' + str(temps_day[i]))
        print(info[i])


if __name__ == '__main__':
    parser()