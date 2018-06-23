import datetime

days = ['23 июня', '24', '25', '26', '27', '28', '29', '30', '1 июля', '2']

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
        # days[i] = days[i].text
        # days[i] = days[i].split('\n')[1].strip()
        if len(days[i].split(' ')) > 1:
            month = month_from_ru_to_eng(days[i].split(' ')[1])
            print(month)
            days[i] = days[i].split(' ')[0]
        days[i] = days[i] + ' ' + month
        print(days[i])
        days[i] = datetime.datetime.strptime(days[i], '%d %b')
        days[i] = days[i].replace(year=datetime.datetime.today().year)     # переприсвоение года
        days[i] = str(days[i].date())
    print(days)
    return days


date = transform_date(days)