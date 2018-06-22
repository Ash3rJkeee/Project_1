import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep

"""Модуль содержит функцию для анонимного подключения к сайтам парсинга"""


# todo Написать обработку слишком долгого соединения. Как вариант использовать второй поток, считающий время
# todo Добавить хранящиеся в файле юзер агенты для маскировки при выборе прокси

def read_file_agents():
    """Считать список агентов из сохраненного файла"""
    global user_agents
    file = open('agents.txt', 'r')
    user_agents = file.readlines()
    print('Из файла загружено ', len(user_agents), 'агентов')
    # print(user_agents)
    for i in range(len(user_agents)):
        user_agents[i] = user_agents[i].strip()
    file.close()


def rewrite_file_agents():
    """Записывает список агентов для следующего запуска программы"""
    global user_agents
    file = open('agents.txt', 'w')
    for i in range(len(user_agents)):
        file.write(user_agents[i] + '\n')
    file.close()


def get_html(url_get, useragent=None, proxy=None):
    """получение странички через прокси с маскировкой под юзер агента.
    Так же выводит статус подключения к сайту"""

    global picked_agent

    if 'picked_agent' not in globals():
        if 'picked_proxy' not in globals():
            got_html = requests.get(url_get, timeout=10)
        else:
            got_html = requests.get(url_get, proxies={'http': 'http://' + picked_proxy}, timeout=10)
        # got_html = requests.get(url_get, proxies={'http': 'http://' + picked_proxy}, timeout=10)
    else:
        if 'picked_proxy' not in globals():
            got_html = requests.get(url_get, headers={'User-Agent': picked_agent}, timeout=10)
        else:
            got_html = requests.get(url_get, headers={'User-Agent': picked_agent}, proxies={'http': 'http://' + picked_proxy}, timeout=10)

    print('Подключение через прокси: ', proxy)
    print('Статус запроса:', url_get, ': ', got_html.status_code)
    got_html = got_html.text
    return got_html


def delete_proxie(proxy):
    """Удаление прокси из списка, чтобы больше он
    не учавтсвовал в выборе"""
    global proxies
    proxies.remove(proxy)


def pick_proxy():
    """Получает обновленный список прокси и возвращает один любой из них"""
    global picked_proxy, proxies, picked_agent

    print('--------------------------------------------------------------------------------------')
    print('Выбор прокси для подключения....')

    if 'picked_proxy' not in globals():
        print("Получение списка прокси.....")
        url_proxy_site = 'https://proxylist.me/?avalibity=90&protocol=&sort=-updated&filtrar=Filtrar&type=&city' \
                         '__state__country__name='

        html = get_html(url_proxy_site)
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
        print('получено ', len(proxies), 'адресов прокси')
    picked_proxy = choice(proxies)
    delete_proxie(picked_proxy)
    print("Использованный новый прокси : ", picked_proxy)
    print()
    return picked_proxy


def get_user_agents(proxy):
    """Возвращает список юзер агентов"""
    global user_agents
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
    print('получено ', len(user_agents), 'агентов')
    rewrite_file_agents()
    return user_agents


def pick_user_agent(proxy):
    """Вызывает функцию получения списков агентов и возвращает одного из них.
     В случае если нет подключения, пробует новый прокси"""
    global picked_agent, picked_proxy, user_agents
    if 'picked_agent' not in globals():                             # на случай, если файл с агентами пустой
        try:
            picked_agent = choice(get_user_agents(picked_proxy))
            print('Использованный User Agent: ', picked_agent)
            print()
        except:
            a = uniform(2, 5)
            print("Попытка не удалась. Ждем ", a, "секунд.....")
            sleep(a)
            picked_proxy = pick_proxy()
            print('Новый прокси: ', picked_proxy, '.....')
            picked_agent = pick_user_agent(picked_proxy)
    picked_agent = choice(user_agents)
    print('Использованный User Agent: ', picked_agent)
    return picked_agent


def get_my_ip_and_user_agent(proxy, useragent):
    """для проверки своего агента и ip"""
    html = get_html('http://sitespy.ru/my-ip', useragent, proxy)
    soup = BeautifulSoup(html, 'html.parser')
    my_ip = soup.find('span', class_='ip').text.strip()
    user_agent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()

    print('my ip: ', my_ip)
    print(user_agent)
    print('Соединение успешно.')
    return my_ip


def connection_check(proxy, useragent):
    """Функция проверки статуса соединения. Если нет соединения, меняет прокси и агент"""
    global picked_agent, picked_proxy, user_agents
    print('Проверка свойств соединения....')
    my_ip = ''
    try:
        my_ip = get_my_ip_and_user_agent(proxy=proxy, useragent=useragent)
    except:
        print('Соединение не удалось. Reconnect.....')
        sleep(uniform(2, 4))
        print('Смена прокси....')
        picked_proxy = pick_proxy()
        print('Смена агента....')
        picked_agent = pick_user_agent(picked_proxy)
        connection_check(picked_proxy, picked_agent)
        print()
    if my_ip == '193.104.149.162':
        print('Некачественный пррокси. Reconnect.....')
        sleep(uniform(2, 4))
        print('Смена прокси....')
        picked_proxy = pick_proxy()
        print('Смена агента....')
        picked_agent = pick_user_agent(picked_proxy)
        connection_check(picked_proxy, picked_agent)
        print()


def smart_get_html(url):
    """Основаная функция подключения"""
    global picked_agent, picked_proxy, user_agents
    read_file_agents()
    if user_agents != []:
        picked_agent = choice(user_agents)
    picked_proxy = pick_proxy()
    picked_agent = pick_user_agent(picked_proxy)
    connection_check(picked_proxy, picked_agent)
    html = get_html(url, proxy=picked_proxy, useragent=picked_agent)
    return html


if __name__ == '__main__':
    url_outer = 'http://ya.ru'
    html_outer = smart_get_html(url_outer)

# 'http://sitespy.ru/my-ip'
