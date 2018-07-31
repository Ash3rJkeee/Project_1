from tkinter import *
import YaParser
import datetime
import gismeteo_parser
import Meteoinfo_parser
import WeatherCom_parser
import smart_request
import exel_export

"""Модуль с основным интерфейсом. Он же основной управляющий модуль"""

# todo Добавить графическое подтверждение, что все прошло успешно

def click_connection_check():
    smart_request.smart_get_html('http://rambler.ru')
    lbl_check.configure(text='Используется рабочий Proxy:        ' + smart_request.picked_proxy)


def click_exel_export():
    exel_export.export()

def do_all():
    frame1.click_ya()
    frame2.click_gismeteo()
    frame3.click_meteoinfo()
    frame4.click_weathercom()
    click_exel_export()



class FrameParser(Frame):
    """Класс блока с парсером"""
    def __init__(self, master, text, row, column):
        super(FrameParser, self).__init__(master, bd=5, relief=RIDGE, height='100', width='500')
        self.grid(row=row, column=column, ipadx=10, ipady=6, padx=10, pady=10)
        self.btn = Button(self, text=text, font='Ubuntu 12', pady=10, relief=RAISED, bd=3,
                          activebackground=activebackground)
        self.btn.pack()
        self.lbl = [0, 1, 2]
        forecast_label_text = ['Завтра', 'Послезавтра', 'Через 2 дня']

        # создание меток
        for i in [0, 1, 2]:
            self.lbl[i] = Label(self, font='Ubuntu 12', text=( str(forecast_label_text[i]) ), width=50)
            self.lbl[i].pack(expand=True)

    def click_ya(self):
        YaParser.yaParser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=YaParser.info[i])

    def click_gismeteo(self):
        gismeteo_parser.gismeteo_parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=gismeteo_parser.info[i])

    def click_meteoinfo(self):
        Meteoinfo_parser.parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=Meteoinfo_parser.info[i])

    def click_weathercom(self):
        WeatherCom_parser.parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=WeatherCom_parser.info[i])


root = Tk()
root.geometry('1050x600+500+200')
root.resizable(width=False, height=False)
root.title("Погодный обозреватель")


# Немного изменить тему
activebackground='#F08080'

lbl_today = Label(root, font='Ubuntu 16', text="Сегодня: " + str(datetime.date.today()))
lbl_today.pack(side=TOP)

btn_do_all = Button(root, text='Просто сделать все автоматом', font='Ubuntu 16', width=50, command=do_all, bd=3,
                    activebackground=activebackground)
btn_do_all.pack(pady=20)

main_frame = Frame(root, relief=RIDGE)
main_frame.pack()

frame1 = FrameParser(main_frame, 'Опросить Яндекс', row=0, column=0)
frame1.btn.configure(command=frame1.click_ya)

frame2 = FrameParser(main_frame, 'Опросить Гисметео', row=1, column=0)
frame2.btn.configure(command=frame2.click_gismeteo)

frame3 = FrameParser(main_frame, 'Опросить Метеоинфо', row=0, column=1)
frame3.btn.configure(command=frame3.click_meteoinfo)

frame4 = FrameParser(main_frame, 'Опросить Weather.com', row=1, column=1)
frame4.btn.configure(command=frame4.click_weathercom)

btn_check = Button(main_frame, text='Проверить соединение', font='Ubuntu 12', command=click_connection_check, bd=3,
                   activebackground=activebackground)
btn_check.grid(row=3, column=0)

lbl_check = Label(main_frame, font='Ubuntu 12', text="статус соединения: ", height='2', relief=RIDGE, bd=3)
lbl_check.grid(row=3, column=1)


btn_export = Button(root, text='Записать в файл', font='Ubuntu 16', command=click_exel_export, width=50, height=300,
                    bd=3, activebackground=activebackground)
btn_export.pack(side=BOTTOM, pady=20)


root.mainloop()
