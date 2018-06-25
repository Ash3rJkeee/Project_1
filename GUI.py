from tkinter import *
import YaParser
import datetime
import gismeteo_parser
import Meteoinfo_parser
import WeatherCom_parser
import smart_request
import exel_export

"""Модуль с основным интерфейсом. Он же основной управляющий модуль"""


def click_ya():
    YaParser.yaParser()
    lbl_1.configure(text=YaParser.info[0])
    lbl_2.configure(text=YaParser.info[1])
    lbl_3.configure(text=YaParser.info[2])


def click_gismeteo():
    gismeteo_parser.gismeteo_parser()
    lbl_4.configure(text=gismeteo_parser.info[0])
    lbl_5.configure(text=gismeteo_parser.info[1])
    lbl_6.configure(text=gismeteo_parser.info[2])


def click_meteoinfo():
    Meteoinfo_parser.parser()
    lbl_7.configure(text=Meteoinfo_parser.info[0])
    lbl_8.configure(text=Meteoinfo_parser.info[1])
    lbl_9.configure(text=Meteoinfo_parser.info[2])


def click_weathercom():
    WeatherCom_parser.parser()
    lbl_10.configure(text=WeatherCom_parser.info[0])
    lbl_11.configure(text=WeatherCom_parser.info[1])
    lbl_12.configure(text=WeatherCom_parser.info[2])


def click_connection_check():
    smart_request.smart_get_html('http://ya.ru')
    lbl_proxy.configure(text='Proxy: ' + smart_request.picked_proxy)


def click_exel_export():
    exel_export.export()


root = Tk()
root.geometry('400x660+500+200')
root.title("Погодный обозреватель")


frame1 = Frame(root, bd=5)
frame2 = Frame(root, bd=5)
frame3 = Frame(root, bd=5)
frame4 = Frame(root, bd=5)


lbl_1 = Label(frame1, font='Ubuntu 12')
lbl_2 = Label(frame1, font='Ubuntu 12')
lbl_3 = Label(frame1, font='Ubuntu 12')


lbl_4 = Label(frame2, font='Ubuntu 12')
lbl_5 = Label(frame2, font='Ubuntu 12')
lbl_6 = Label(frame2, font='Ubuntu 12')

lbl_7 = Label(frame3, font='Ubuntu 12')
lbl_8 = Label(frame3, font='Ubuntu 12')
lbl_9 = Label(frame3, font='Ubuntu 12')

lbl_10 = Label(frame4, font='Ubuntu 12')
lbl_11 = Label(frame4, font='Ubuntu 12')
lbl_12 = Label(frame4, font='Ubuntu 12')

lbl_today = Label(root, font='Ubuntu 12', text="Сегодня: " + str(datetime.date.today()))
lbl_proxy = Label(root, font='Ubuntu 12', text="Proxy: ", height='2')


btn_1 = Button(frame1, text='Спарсить Яндекс.Погода', font='Ubuntu 12', command=click_ya)
btn_2 = Button(frame2, text='Спарсить GISMETEO', font='Ubuntu 12', command=click_gismeteo)
btn_3 = Button(frame3, text='Спарсить meteoinfo.ru', font='Ubuntu 12', command=click_meteoinfo)
btn_4 = Button(frame4, text='Спарсить weather.com', font='Ubuntu 12', command=click_weathercom)
btn_check = Button(root, text='Проверить соединение', font='Ubuntu 12', command=click_connection_check)
btn_export = Button(root, text='Записать в файл', font='Ubuntu 12', command=click_exel_export)


lbl_today.pack()

btn_1.pack()
frame1.pack()
lbl_1.pack()
lbl_2.pack()
lbl_3.pack()

btn_2.pack()
frame2.pack()
lbl_4.pack()
lbl_5.pack()
lbl_6.pack()

btn_3.pack()
frame3.pack()
lbl_7.pack()
lbl_8.pack()
lbl_9.pack()

btn_4.pack()
frame4.pack()
lbl_10.pack()
lbl_11.pack()
lbl_12.pack()

btn_check.pack()
lbl_proxy.pack()

btn_export.pack()

root.mainloop()

