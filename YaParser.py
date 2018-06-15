from bs4 import BeautifulSoup
import datetime


# TODO Добавить чтение файла с нета. Возможно, написать отдельный модуль для этого.


def yaParser():
    global info

    # чтение файла с указанием его кодировки. Обработка исключения, если запускается на домашнем компе (другой путь файла)
    try:
        html = open('C:\\Users\\a.ryadinskih\YandexDisk\YaDiscPyProjects\Project_1\\Yandex.htm', encoding='utf-8').read()
    except FileNotFoundError:
        html = open('C:\\Users\\Asher\YandexDisk\YaDiscPyProjects\Project_1\\Yandex.htm', encoding='utf-8').read()

    # создание объекта Soup
    soup = BeautifulSoup(html, 'html.parser')

    # поиск тегов 'time' и 'span' нужных классов
    days = soup.findAll('time', class_='time forecast-briefly__date')
    temps = soup.findAll('span', class_='temp__value')

    # отбрасывание лишних данных от результата парсинга
    del temps[0:3]
    del temps[6:]

    # заготовка списков
    date = []
    temps_day = []
    temps_night = []
    info = []

    # вывод на печать сегодняшней даты
    # today = datetime.date.today()
    # print('Сегодня: ', today)

    for i in [0, 1, 2]:
        date.append(days[i].get('datetime'))
        date[i] = date[i].split('+', 1)[:1]          # отбросить указание часового пояса
        date[i] = str(date[i])[2:]                   # отбросить ['
        date[i] = str(date[i])[:16]                  # отбросить ']
        date[i] = datetime.datetime.strptime(str(date[i]), "%Y-%m-%d %H:%M")   # преобразование даты в формат даты модуля datetime
        temps_day.append(temps[i*2].text)          # разбиение на списки дневных и ночных температур
        temps_night.append(temps[i*2+1].text)        #
        info.append('Температура ' + str(date[i].date()) + ' составит ' + str(temps_day[i]) + ' ' + str(temps_night[i]))
        # print(info[i])


if __name__ == '__main__':
    yaParser()



# классы и теги, которые необходимо было спарсить
# <time class="time forecast-briefly__date" datetime="2018-06-05 00:00+0300">5 июня</time>
# <span class="temp__value">+14</span>