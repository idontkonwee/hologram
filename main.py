from tkinter import *
from tkinter import filedialog
from PIL import Image
from func import plot, gen_hologram, re_hologram, plt, perfect_hologram, add_hologram
import numpy as np


pic_path = ""
pic_path1 = ""
data = {}


def upload_pic():
    global pic_path
    pic_path = filedialog.askopenfilename(initialdir='D:/code/PycharmProjects/作业/全息/样品图片')
    img = Image.open(pic_path)
    img_show = img.resize((200, 200))
    img_show.save('head.png')
    head = PhotoImage(file='head.png')
    head_button.config(image=head)
    head_button.image = head
    return img


def upload_pic1():
    global pic_path1
    print("1=" + pic_path1)
    pic_path1 = filedialog.askopenfilename(initialdir='D:/code/PycharmProjects/作业/全息/样品图片')
    img = Image.open(pic_path1)
    img_show = img.resize((200, 200))
    img_show.save('head1.png')
    head1 = PhotoImage(file='head1.png')
    head_button1.config(image=head1)
    head_button1.image = head1
    return img


win = Tk()
win.title("全息图转换")
win.geometry('500x500')

Label(text="波长").place(x=50, y=270)
wavelen = Entry(win, width=10)
wavelen.insert(0, "532")
wavelen.place(x=170, y=270)
Label(text="nm").place(x=250, y=270)

Label(text="记录距离").place(x=50, y=290)
l0 = Entry(win, width=10)
l0.insert(0, "0.2")
l0.place(x=170, y=290)
Label(text="m").place(x=250, y=290)

Label(text="CCD宽度").place(x=50, y=310)
m = Entry(win, width=10)
m.insert(0, "1024")
m.place(x=170, y=310)
Label(text="个").place(x=250, y=310)

Label(text="CCD高度").place(x=50, y=330)
n = Entry(win, width=10)
n.insert(0, "1024")
n.place(x=170, y=330)
Label(text="个").place(x=250, y=330)

Label(text="CCD像素尺寸").place(x=50, y=350)
d = Entry(win, width=10)
d.insert(0, "5.2")
d.place(x=170, y=350)
Label(text="um").place(x=250, y=350)


Label(text="物品宽度").place(x=50, y=370)
a = Entry(win, width=10)
a.insert(0, "1")
a.place(x=170, y=370)
Label(text="cm").place(x=250, y=370)


Label(text="物品高度").place(x=50, y=390)
b = Entry(win, width=10)
b.insert(0, "1")
b.place(x=170, y=390)
Label(text="cm").place(x=250, y=390)


Label(text="光垂直方向夹角").place(x=50, y=410)
alpha = Entry(win, width=10)
alpha.insert(0, "0")
alpha.place(x=170, y=410)
Label(text="度").place(x=250, y=410)


Label(text="光水平方向夹角").place(x=50, y=430)
beta = Entry(win, width=10)
beta.insert(0, "0")
beta.place(x=170, y=430)
Label(text="度").place(x=250, y=430)


Label(text="图片文件").place(x=100, y=20)
default_pic = PhotoImage(file='default_pic.png')
head_button = Button(image=default_pic, command=upload_pic)
head_button.place(x=50, y=60, width=200, height=200)

Label(text="合成全息图用文件").place(x=300, y=20)
head_button1 = Button(image=default_pic, command=upload_pic1)
head_button1.place(x=270, y=60, width=200, height=200)


def get_data():
    global data
    data = {
        "wavelen": float(wavelen.get()) * 10e-10,
        "l0": float(l0.get()),
        "d": float(d.get()) * 10e-7,
        "a": float(a.get()) * 0.01,
        "b": float(b.get()) * 0.01,
        "alpha": float(alpha.get()) * np.pi / 180,
        "beta": float(beta.get()) * np.pi / 180,
    }


def made():
    get_data()
    if pic_path:
        fig = plt.imread(pic_path)
        plot(gen_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"]))


button_made = Button(text="生成全息图", command=made)
button_made.place(x=300, y=300)


def re_made():
    get_data()
    if pic_path:
        fig = plt.imread(pic_path)
        plot(re_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"]))


button_re_made = Button(text="全息图再现", command=re_made)
button_re_made.place(x=300, y=350)


def made_good():
    get_data()
    if pic_path:
        fig = plt.imread(pic_path)
        hologram = gen_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"])
        hol_ = re_hologram(hologram, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"])
        plot(hologram, hol_, True)


button_change = Button(text="零级光消去(正)", command=made_good)
button_change.place(x=300, y=400)


def add():
    fig = plt.imread(pic_path)
    fig1 = plt.imread(pic_path1)
    plot(add_hologram(fig, fig1))


button_real = Button(text="全息图合成", command=add)
button_real.place(x=400, y=300)


def made_good_():
    get_data()
    if pic_path:
        fig = plt.imread(pic_path)
        hologram = gen_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"], 1)
        hol_ = re_hologram(hologram, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"])
        plot(hologram, hol_, True)


button_change1 = Button(text="消零级光(负)", command=made_good_)
button_change1.place(x=400, y=400)


def perfect():
    get_data()
    if pic_path:
        fig = plt.imread(pic_path)
        pic1 = gen_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"])
        pic = perfect_hologram(fig, data["alpha"], data["beta"], data["wavelen"], data["a"], data["b"], data["l0"], data["d"])
        plot(pic1, pic, True)


button_perfect = Button(text="完美再现图", command=perfect)
button_perfect.place(x=400, y=350)


def perfect():
    if pic_path and pic_path1:
        fig = plt.imread(pic_path)
        fig1 = plt.imread(pic_path1)


button_value = Button(text="导出参数", command=perfect)
button_value.place(x=300, y=450)

win.mainloop()

