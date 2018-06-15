def month_from_ru_to_eng(month):
    out = ''
    if month == 'января': out = 'jan'
    if month == 'декабря': out = 'dec'
    if month == 'февраля': out = 'feb'
    if month == 'марта': out = 'mar'
    if month == 'апреля': out = 'apr'
    if month == 'мая': out = 'may'
    if month == 'июня': out = 'jun'
    if month == 'июня': out = 'jul'
    if month == 'августа': out = 'aug'
    if month == 'сентябся': out = 'sep'
    if month =='октября': out = 'oct'
    if month == 'ноября': out = 'nov'
    if month == 'декабря': out = 'dec'
    return out


a = month_from_ru_to_eng('января')
print(a)


