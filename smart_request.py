import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep

"""Модуль содержит функцию для анонимного подключения к сайтам парсинга"""


# todo Попробовать импортировать в парсеры погодных сервисов.


def get_html(url_get, useragent=None, proxy=None):
    """получение странички через прокси с маскировкой под юзер агента.
    Так же выводит статус подключения к сайту"""
    got_html = requests.get(url_get, headers={'User-Agent': useragent}, proxies={'http': 'http://' + proxy})
    print('Подключение через прокси: ', proxy)
    print('Статус запроса:', url_get, ': ', got_html.status_code)
    got_html = got_html.text
    return got_html


def pick_proxy():
    """Получает обновленный список прокси и возвращает один любой из них"""
    global picked_proxy, proxies

    print('Выбор прокси для подключения....')

    if 'picked_proxy' not in globals():
        print("Получение списка прокси.....")
        url_proxy_site = 'https://proxylist.me/?avalibity=90&protocol=&sort=-updated&filtrar=Filtrar&type=&city' \
                         '__state__country__name='
        html = requests.get(url_proxy_site).text
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        td = table.findAll('td', class_='ip')

        # поиск значений прокси
        proxies = []
        for i in td:
            proxies.append(i.text.strip())

        # поиск значений портов
        ports = []
        for i in soup.findAll('td', class_='port'):
            ports.append(i.text.strip())

        # слияние ip и портов
        for i in range(len(proxies)):
            proxies[i] = proxies[i] + ":" + str(ports[i])
            # print(proxies[i])
    picked_proxy = choice(proxies)
    print("Выбранный новый прокси : ", picked_proxy)
    print()
    return picked_proxy


def get_user_agents(proxy):
    """Возвращает список юзер агентов"""
    print("Получение списка агентов для маскировки....")
    html = get_html('https://ru.myip.ms/browse/comp_browseragents/1', proxy=proxy)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='comp_browseragents_tbl')
    tds = table.findAll('td', class_='row_name')

    user_agents = []

    for i in tds:
        user_agents.append(i.find('a').text.strip())

    # for i in range(len(user_agents)):
    #     print(user_agents[i])
    return user_agents


def get_my_ip_and_user_agent(proxy, useragent):
    """для проверки своего агента и ip"""
    html = get_html('http://sitespy.ru/my-ip', useragent, proxy)
    soup = BeautifulSoup(html, 'html.parser')
    ip = soup.find('span', class_='ip').text.strip()
    user_agent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()

    print('my ip: ', ip)
    print(user_agent)
    print('Соединение успешно.')
    return ip, user_agent


def pick_user_agent(proxy):
    """Вызывает функцию получения списков агентов и возвращает одного из них.
     В случае если нет подключения, пробует новый прокси"""
    # global picked_agent, picked_proxy
    try:
        print("Попытка получить user agent....")
        picked_agent = choice(get_user_agents(proxy=proxy))
        print('Выбранный User Agent: ', picked_agent)
        print()
    except:
        a = uniform(2, 5)
        print("Попытка не удалась. Ждем ", a, "секунд.....")
        sleep(a)
        picked_proxy = pick_proxy()
        print('Новый прокси: ', picked_proxy, '.....')
        pick_user_agent(picked_proxy)
    return picked_agent


def connection_check(proxy, useragent):
    """Функция проверки статуса соединения. Если нет соединения, меняет прокси и агент"""
    print('Проверка свойств соединения....')
    try:
        get_my_ip_and_user_agent(proxy=proxy, useragent=useragent)
    except:
        print('Соединение не удалось. Reconnect.....')
        print('Смена прокси....')
        sleep(uniform(2, 4))
        proxy = pick_proxy()
        useragent = pick_user_agent(proxy)
        connection_check(proxy, useragent)


def get(url):
    """Основаная функция подключения"""
    picked_proxy = pick_proxy()
    picked_agent = pick_user_agent(picked_proxy)
    connection_check(picked_proxy, picked_agent)
    html = get_html(url, proxy=picked_proxy, useragent=picked_agent)
    return html


if __name__ == '__main__':
    url_outer = 'http://rambler.ru'
    html_outer = get(url_outer)

# 'http://sitespy.ru/my-ip'
