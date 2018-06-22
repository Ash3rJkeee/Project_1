

day = 'Воскресенье24 июня'


for i in range(len(day)):
    if day[i].isdigit():
        day = day[i:]
        break

print(day)