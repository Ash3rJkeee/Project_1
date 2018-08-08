from tkinter import *
import YaParser
import datetime
import gismeteo_parser
import Meteoinfo_parser
import WeatherCom_parser
import smart_request
import exel_export

"""Модуль с основным интерфейсом. Он же основной управляющий модуль"""


def click_connection_check():
    smart_request.smart_get_html('http://rambler.ru')
    # lbl_check_proxy_data.configure(text=smart_request.picked_proxy)
    if smart_request.checked == True:
        lbl_check_proxy_data.configure(text="функционирует", bg="green")
    else:
        lbl_check_proxy_data.configure(text="не функционирует", bg="red")
    lbl_check_ip_data.configure(text=smart_request.my_ip)
    btn_check.configure(state="disabled")


def click_exel_export():
    try:
        exel_export.export()
        lbl_export.configure(text='Готово!', bg="green")
    except:
        lbl_export.configure(text='Ошибка', bg="red")
    btn_export.configure(state="disabled")


def do_all():
    frame1.click_ya()
    frame2.click_gismeteo()
    frame3.click_meteoinfo()
    frame4.click_weathercom()
    click_exel_export()
    btn_do_all.configure(state="disabled")


class FrameParser(Frame):
    """Класс блока с парсером"""
    def __init__(self, master, text, row, column):
        super(FrameParser, self).__init__(master, bd=5, relief=RIDGE)
        self.grid(row=row, column=column, ipadx=10, ipady=6, padx=10, pady=10)
        self.btn = Button(self, text=text, font='Ubuntu 12', pady=10, relief=RAISED, bd=3,
                          activebackground=activebackground)
        self.btn.pack()
        self.lbl = [0, 1, 2]
        forecast_label_text = ['Завтра', 'Послезавтра', 'Через 2 дня']

        # создание меток
        for i in [0, 1, 2]:
            self.lbl[i] = Label(self, font='Ubuntu 12', text=(str(forecast_label_text[i])), width=50)
            self.lbl[i].pack(expand=True)

    def click_ya(self):
        YaParser.yaParser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=YaParser.info[i])
        frame1.btn.configure(state="disabled")

    def click_gismeteo(self):
        gismeteo_parser.gismeteo_parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=gismeteo_parser.info[i])
        frame2.btn.configure(state="disabled")

    def click_meteoinfo(self):
        Meteoinfo_parser.parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=Meteoinfo_parser.info[i])
        frame3.btn.configure(state="disabled")

    def click_weathercom(self):
        WeatherCom_parser.parser()
        for i in [0, 1, 2]:
            self.lbl[i].configure(text=WeatherCom_parser.info[i])
        frame4.btn.configure(state="disabled")


root = Tk()
root.geometry('1050x680+500+200')
# root.resizable(width=False, height=False)
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


frame_status = Frame(main_frame, bd=5, relief=RIDGE)
frame_status.grid(row=2, column=0, columnspan=2)

frame_status_1 = Frame(frame_status)
frame_status_2 = Frame(frame_status)
frame_status_3 = Frame(frame_status)


frame_status_1.grid(row=0, column=0, padx=50)
frame_status_2.grid(row=0, column=1, padx=0)
frame_status_3.grid(row=0, column=2, padx=10)


frame_export = Frame(main_frame)
frame_export.grid(row=3, column=0, columnspan=2)


btn_check = Button(frame_status_1, text='Проверить соединение', font='Ubuntu 12', command=click_connection_check, bd=3,
                   activebackground=activebackground)
btn_check.grid(row=0, column=0, sticky="w", pady=25)

lbl_check_proxy = Label(frame_status_2, font='Ubuntu 12', text="Используемый прокси: ", height=2, bd=3)
lbl_check_proxy.pack(padx=10)

lbl_check_ip = Label(frame_status_2, font='Ubuntu 12', text="Видимый IP: ", height=2, bd=3)
lbl_check_ip.pack(padx=10)

lbl_check_proxy_data = Label(frame_status_3, font='Ubuntu 12', text="--------------------", height=2, bd=3)
lbl_check_proxy_data.pack(padx=10)

lbl_check_ip_data = Label(frame_status_3, font='Ubuntu 12', text="--------------------", height=2, bd=3)
lbl_check_ip_data.pack(padx=10)

btn_export = Button(frame_export, text='Записать в файл', font='Ubuntu 16', command=click_exel_export, width=40,
                    bd=3, activebackground=activebackground)
btn_export.pack(side=LEFT, pady=20, padx=50)

lbl_export = Label(frame_export, font='Ubuntu 16', text="", height=2, bd=5)
lbl_export.pack(side=RIGHT, pady=20, padx=50)


root.mainloop()
