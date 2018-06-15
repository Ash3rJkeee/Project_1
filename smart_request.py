import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep

"""Модуль содержит функцию для анонимного подключения к сайтам парсинга"""


# todo Расписать запросы к сайту с прокси и фейковыми агентскими клиентами
# todo Расписать агентские клиенты
# todo Расписать список user agent'ов
# todo Разобраться с выводом User-Agenta


def get_html(url, useragent=None, proxy=None):
    """получение странички через прокси с маскировкой под юзер агента"""
    html = requests.get(url, headers={'User-Agent': useragent}, proxies={'http': 'http://' + proxy})
    print('Подключение через прокси: ', proxy)
    print('Статус запроса:', url, ': ', html.status_code)
    html = html.text
    return html


def get_proxies():
    """Возвращает обновленный список прокси"""
    print("Получение списка прокси.....")
    url = 'https://proxylist.me/?avalibity=90&protocol=&sort=-updated&filtrar=Filtrar&type=&city__state__country__name='
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    td = table.findAll('td', class_='ip')

    proxies = []
    for i in td:
        proxies.append(i.text.strip())

    ports = []
    for i in soup.findAll('td', class_='port'):
        ports.append(i.text.strip())

    for i in range(len(proxies)):
        proxies[i] = proxies[i] + ":" + str(ports[i])
        # print(proxies[i])
    return proxies


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
    return ip, user_agent


def pick_user_agent(proxy):
    """Вызывает функцию получения списков агентов и возвращает одного из них. В случае """
    global picked_agent, picked_proxy
    try:
        print("Попытка получить user agent....")
        picked_agent = choice(get_user_agents(proxy=proxy))
    except AttributeError:
        a = uniform(2, 5)
        print("прокси недоступен, ждем ", a, "секунд.....")
        sleep(a)
        picked_proxy = choice(get_proxies())
        print('Новый прокси: ', picked_proxy, '.....')
        pick_user_agent(picked_proxy)
    return picked_agent


def connection_check(proxy, useragent):
    # todo Разобраться в необходимости этой функции и обработки исключения
    """Функция проверки статуса соединения"""
    try:
        get_my_ip_and_user_agent(proxy=proxy, useragent=useragent)
    except AttributeError:
        sleep(uniform(2, 4))
        connection_check(proxy, useragent)


def smart_request():
    """Основаная функция подключения"""
    print('Выбор прокси для подключения....')
    picked_proxy = choice(get_proxies())
    print("Выбранный прокси: ", picked_proxy)
    print()

    picked_agent = pick_user_agent(picked_proxy)
    print('Выбранный User Agent: ', picked_agent)
    print()

    connection_check(picked_proxy, picked_agent)


smart_request()

# 'http://sitespy.ru/my-ip'
