import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep

"""Модуль содержит функцию для анонимного подключения к сайтам парсинга"""


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


def read_file_proxies():
    """Считать список прокси из сохраненного файла"""
    global proxies
    file = open('proxies.txt', 'r')
    proxies = file.readlines()
    print('Из файла загружено ', len(proxies), 'прокси')
    # print(proxies)
    for i in range(len(proxies)):
        proxies[i] = proxies[i].strip()
    file.close()


def rewrite_file_proxies():
    """Перезаписывает список прокси для следующего запуска программы"""
    global proxies
    file = open('proxies.txt', 'w')
    for i in range(len(proxies)):
        file.write(proxies[i] + '\n')
    file.close()


def get_html(url_get):
    """получение странички через прокси с маскировкой под юзер агента.
    Так же выводит статус подключения к сайту"""

    try:
        global picked_agent, picked_proxy

        if 'picked_agent' not in globals():
            if 'picked_proxy' not in globals():
                got_html = requests.get(url_get, timeout=10)
            else:
                print('\nПодключение через прокси: ', picked_proxy)
                got_html = requests.get(url_get, proxies={'socks5://': picked_proxy}, timeout=10)
            # got_html = requests.get(url_get, proxies={'http': 'http://' + picked_proxy}, timeout=10)
        else:
            if 'picked_proxy' not in globals():
                got_html = requests.get(url_get, headers={'User-Agent': picked_agent}, timeout=10)
            else:
                print('\nПодключение через прокси: ', picked_proxy)
                got_html = requests.get(url_get, headers={'User-Agent': picked_agent},
                                        proxies={'socks5://': picked_proxy}, timeout=10)
    except requests.exceptions.ReadTimeout:
        """На случай, если конкретный прокси забанен на конкретном сайте"""
        print('Превышено время ожидания ответа')
        # delete_proxie(picked_proxy)
        pick_proxy()
        got_html = get_html(url_get)
    print('Статус запроса:', url_get, ': ', got_html.status_code)

    got_html = got_html.text
    return got_html


def delete_proxie(proxy):
    """Удаление прокси из списка, чтобы больше он
    не учавтсвовал в выборе"""
    global proxies
    proxies.remove(proxy)
    rewrite_file_proxies()


def pick_proxy():
    """Получает обновленный список прокси и передает в picked_proxy первый элемент из него"""
    global picked_proxy, proxies, picked_agent

    print('--------------------------------------------------------------------------------------')
    print('Выбор прокси для подключения....')

    picked_proxy = proxies[0]
    print("Использованный новый прокси : ", picked_proxy)
    print()


def get_user_agents():
    """Возвращает список юзер агентов"""
    global user_agents
    print("Получение списка агентов для маскировки....")
    html = get_html('https://ru.myip.ms/browse/comp_browseragents/1')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='comp_browseragents_tbl')
    tds = table.findAll('td', class_='row_name')

    user_agents = []

    for i in tds:
        user_agents.append(i.find('a').text.strip())

    # for i in range(len(user_agents)):
    #     print(user_agents[i])
    rewrite_file_agents()
    print('получено и записано', len(user_agents), 'агентов')
    return user_agents


def pick_user_agent():
    """Вызывает функцию получения списков агентов и возвращает одного из них.
     В случае если нет подключения, пробует новый прокси"""
    global picked_agent, picked_proxy, user_agents
    if 'picked_agent' not in globals():                             # на случай, если файл с агентами пустой
        try:
            picked_agent = choice(get_user_agents())
            print('Использованный User Agent: ', picked_agent)
            print()
        except:
            a = uniform(2, 5)
            print("Попытка не удалась. Ждем ", a, "секунд.....")
            sleep(a)
            pick_proxy()
            print('Новый прокси: ', picked_proxy, '.....')
            picked_agent = pick_user_agent()
    picked_agent = choice(user_agents)
    print('Использованный User Agent: ', picked_agent)


def get_my_ip_and_user_agent():
    """для проверки своего агента и ip"""
    global picked_agent, picked_proxy, user_agents
    html = get_html('https://yandex.ru/internet/')
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.findAll("div", class_="list-info__renderer")
    my_ip = divs[0].text
    browser = divs[7].text

    print("ip: ", my_ip)
    print("Браузер: ", browser)
    return my_ip


def connection_check():
    """Функция проверки статуса соединения. Если нет соединения, меняет прокси и агент"""
    global picked_agent, picked_proxy, user_agents, checked, my_ip
    print('Проверка свойств соединения....')
    my_ip = ''
    # try:
    my_ip = get_my_ip_and_user_agent()
    print('Соединение успешно.')
    checked = True
    # except:
    #     print('Соединение не удалось. Reconnect.....')
    #     sleep(uniform(2, 4))
    #     # print('Смена прокси....')
    #     # delete_proxie(picked_proxy)
    #     pick_proxy()
    #     print('Смена агента....')
    #     pick_user_agent()
    #     connection_check()
    #     print()
    # if my_ip == '193.104.149.167':
    #     # Todo прописать проверку всей доменной зоны МОЭК 193.104.149.0-255
    #     print('Некачественный пррокси. Reconnect.....')
    #     sleep(uniform(2, 4))
    #     # print('Смена прокси....')
    #     # delete_proxie(picked_proxy)
    #     pick_proxy()
    #     print('Смена агента....')
    #     pick_user_agent()
    #     connection_check()
    #     print()


def smart_get_html(url):
    """Основаная функция подключения"""
    global picked_agent, picked_proxy, user_agents, checked

    if checked == False:
        read_file_agents()
        read_file_proxies()
        if user_agents != []:
            picked_agent = choice(user_agents)
            print('Используемый агент: ', picked_agent)
        else:
            pick_user_agent()
        pick_proxy()
        connection_check()
    html = get_html(url)
    return html


checked = False
picked_proxy = ''
my_ip = ''

if __name__ == '__main__':
    # сюда вбивать url для теста работы модуля изолированно от остальных
    url_outer = 'http://ya.ru'
    html_outer = smart_get_html(url_outer)


