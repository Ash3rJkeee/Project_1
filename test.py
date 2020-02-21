import datetime

a = "29 feb"

a = datetime.datetime.strptime(a, '%d %b')
a = a.replace(year=datetime.datetime.today().year)     # переприсвоение года
a = str(a.date())

print(a)