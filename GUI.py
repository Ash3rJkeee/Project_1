from tkinter import *
import YaParser
import datetime
import gismeteo_parser

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


root = Tk()
root.geometry('400x400')
root.title("парсер Яндекс.Погоды")



frame1 = Frame(root, bd=5)
frame2 = Frame(root, bd=5)


lbl_1 = Label(frame1, font='Ubuntu 12')
lbl_2 = Label(frame1, font='Ubuntu 12')
lbl_3 = Label(frame1, font='Ubuntu 12')


lbl_4 = Label(frame2, font='Ubuntu 12')
lbl_5 = Label(frame2, font='Ubuntu 12')

lbl_today = Label(root, font='Ubuntu 12', text="Сегодня: " + str(datetime.date.today()))

btn_1 = Button(frame1, text='Спарсить Яндекс.Погода', font='Ubuntu 12', command=click_ya)
btn_2 = Button(frame2, text='Спарсить GISMETEO', font='Ubuntu 12', command=click_gismeteo)



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


root.mainloop()

