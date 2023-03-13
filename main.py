from tkinter import *
from tkinter import ttk
import tkinter
from city_url import GetCityUrl, pro_change
from weather_get import weather_today, weather_15days
from PIL import Image, ImageTk
from pic_get import pic_get, bg_choose
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_img(file, width, height):
    # 用于制作窗口背景图片的函数
    im = Image.open(file).resize((width, height))
    im = ImageTk.PhotoImage(im)
    return im


def main():
    # 创建窗口，主界面
    window = Tk()
    window.title('天气查询系统')
    window.geometry('800x600+300+150')
    canvas_window = Canvas(window, width=800, height=600)
    im_window = get_img('image_bg/main_bg.jpg', 800, 600)
    canvas_window.create_image(400, 300, image=im_window)
    canvas_window.pack()  # 设置背景
    Label(window, text='请输入省份').place(x=160, y=280, width=80, height=40)
    Label(window, text='欢迎您使用本天气查询系统，祝您拥有好天气和好心情!', font='楷体')\
        .place(x=400,  y=50, anchor='n', width=500, height=50)  # 设置欢迎词
    enter = Entry(window)  # 输入框
    enter.place(x=240, y=280, width=400, height=40)
    enter.delete(0, END)
    enter.insert(0, '重庆')  # 设置默认城市为重庆

    def city_choose():
        province = enter.get()  # 得到输入的省份名称
        province_name = pro_change(province)
        window.destroy()
        root = Tk()  # 填写省份之后，会打开城市选择的窗口
        root.title('城市选择')
        root.geometry('400x300+200+20')
        canvas_root = Canvas(root, width=400, height=300)
        im_root = get_img('image_bg/city_choose_bg.jpg', 400, 300)
        canvas_root.create_image(200, 150, image=im_root)
        canvas_root.pack()
        get_cities = GetCityUrl(province_name)  # 得到这个省的所有具体城市的天气查询链接
        get_cities.get_data()
        city = tkinter.StringVar(master=root)  # 设置一个具体城市的下拉菜单,注意此时必须要初始化master=root！！！
        con = ttk.Combobox(root, textvariable=city)  # 设置一个具体城市的下拉菜单
        con.place(x=120, y=90, width=160, height=30)
        Label(root, text='请下拉选择您要查询天气的城市或景点').place(x=90, y=60, width=220, height=30)
        con['value'] = get_cities.city_name_list  # 以用户输入的省份内的所有城市为元素，做一个下拉菜单

        def show_page(event):
            city_name = con.get()
            url1 = get_cities.city_data[con.get()]
            url = url1
            root.destroy()
            show_p = Tk()  # 展示天气状况的副窗口
            show_p.geometry('800x600')  # 修改窗口大小
            show_p.title('今日城市天气状况播报')  # 今日天气窗口标题
            wea_dict = weather_today(url1)
            wea = wea_dict['天气']
            temp_max = wea_dict['最高气温']
            temp_min = wea_dict['最低气温']
            air = wea_dict['空气质量']
            canvas_show_p = Canvas(show_p, width=800, height=600)
            im_show_p = get_img(bg_choose(wea), 800, 600)
            canvas_show_p.create_image(400, 300, image=im_show_p)
            canvas_show_p.pack()
            Label(show_p, text=f"今天{city_name}的天气简要信息如下：", font='楷体').place(x=150, y=40, width=500, height=30)
            Label(show_p, text=f"今日天气：{wea}", font='华文新魏').place(x=295, y=80, width=210, height=30)
            Label(show_p, text=f"今日最高温度：{temp_max}度", font='华文新魏').place(x=295, y=120, width=210, height=30)
            Label(show_p, text=f"今日最低温度：{temp_min}度", font='华文新魏').place(x=295, y=160, width=210, height=30)
            Label(show_p, text=f"今日空气质量：{air}", font='华文新魏').place(x=295, y=200, width=210, height=30)
            Label(show_p, text=f"今日风况：{wea_dict['风况']}", font='华文新魏').place(x=300, y=240, width=200, height=30)
            Label(show_p, text=f"今日{wea_dict['湿度']}", font='华文新魏').place(x=330, y=280, width=140, height=30)
            Label(show_p, text=f"今日天气提示：{wea_dict['提示']}", font='华文新魏').place(x=150, y=320, width=500, height=30)

            def life_tip():
                wea_dict = weather_today(url)
                life_page = Tk()
                life_page.geometry('800x500')
                life_page.title('今日生活提示')
                life_page.configure(bg='gray')
                tip = wea_dict['生活指南']
                Label(life_page, text=f"{city_name}今日生活指南").place(x=270, y=10, width=260, height=50)
                Label(life_page, text=f"运动：{tip['运动']}", font='华文新魏').place(x=110, y=80, width=140, height=30)
                Label(life_page, text=f"洗车：{tip['洗车']}", font='华文新魏').place(x=330, y=80, width=140, height=30)
                Label(life_page, text=f"化妆：{tip['化妆']}", font='华文新魏').place(x=540, y=80, width=140, height=30)
                Label(life_page, text=f"穿衣：{tip['穿衣']}", font='华文新魏').place(x=110, y=140, width=140, height=30)
                Label(life_page, text=f"中暑：{tip['中暑']}", font='华文新魏').place(x=330, y=140, width=140, height=30)
                Label(life_page, text=f"交通：{tip['交通']}", font='华文新魏').place(x=540, y=140, width=140, height=30)
                Label(life_page, text=f"钓鱼：{tip['钓鱼']}", font='华文新魏').place(x=110, y=200, width=140, height=30)
                Label(life_page, text=f"划船：{tip['划船']}", font='华文新魏').place(x=330, y=200, width=140, height=30)
                Label(life_page, text=f"晨练：{tip['晨练']}", font='华文新魏').place(x=540, y=200, width=140, height=30)
                Label(life_page, text=f"旅游：{tip['旅游']}", font='华文新魏').place(x=110, y=260, width=140, height=30)
                Label(life_page, text=f"晾晒：{tip['晾晒']}", font='华文新魏').place(x=330, y=260, width=140, height=30)
                Label(life_page, text=f"约会：{tip['约会']}", font='华文新魏').place(x=540, y=260, width=140, height=30)
                Label(life_page, text="今日穿衣提醒").place(x=340, y=320, width=120, height=40)
                Label(life_page, text=f"{wea_dict['穿衣提醒']}").place(x=150, y=370, width=500, height=40)
                life_page.mainloop()

            def show_15days():  # 展示该城市15日内天气情况的页面

                show_p15 = Tk()
                show_p15.title('城市15日天气情况播报')
                show_p15.geometry('1450x400')
                show_p15.configure(bg='gray')
                wea_15 = weather_15days(url)
                temp_max = wea_15['每日最高气温']
                temp_min = wea_15['每日最低气温']
                wea_list = wea_15['每日天气']
                date, week = wea_15['日期'], wea_15['星期']
                Label(show_p15, text=f"{city_name}15天的天气情况如下", font='楷体').pack(side=TOP)
                for i in range(15):  # 将每一天的数据放入列表中
                    LANGS = [(date[i], '日期'),
                             (week[i], '星期'),
                             (temp_max[i], '最高温'),
                             (temp_min[i], '最低温'),
                             (wea_list[i], '天气')]
                    group = LabelFrame(show_p15, text='天气状况', padx=0, pady=0)  # 框架
                    group.pack(padx=11, pady=0, side=LEFT)  # 放置框架
                    for lang, value in LANGS:  # 将数据放入框架中
                        c = Label(group, text=value + ': ' + lang)
                        c.pack(anchor=W)
                file_pic = pic_get(url, city_name)

                def pic():
                    root = Tk()#创建用来展示15天内气温变化趋势的新窗口
                    root.title('当地15日气温变化趋势')
                    root.geometry('800x600+300+150')
                    canvas = FigureCanvasTkAgg(file_pic, master=root)
                    canvas.draw()
                    canvas.get_tk_widget().place(relx=0, rely=0, width=800, height=600)

                b = Button(show_p15, text="点击查看气温变化趋势", width=20, height=2, command=pic)
                b.place(relx=0.43, rely=0.73, width=160, height=30)

            b = Button(show_p, text="点击查看当地十五日预报", width=20, height=2, command=show_15days)
            c = tkinter.Button(show_p, text="点击查看城市的生活提示", width=15, height=2, command=life_tip)
            b.place(x=330, rely=0.7, width=140, height=40)
            c.place(x=330, rely=0.8, width=140, height=40)

            show_p.mainloop()

        con.bind('<<ComboboxSelected>>', show_page)
        root.mainloop()

    flag = 1
    Button(window, text="确认", width=10, comman=city_choose).place(relx=0.25, rely=0.75, width=80, height=40)
    # 设置确认按钮，点击后执行到城市选择的界面
    Button(window, text='退出', width=10, command=window.quit).place(relx=0.62, rely=0.75, width=80, height=40)

    if flag == 1:
        window.mainloop()


if __name__ == '__main__':
    main()
