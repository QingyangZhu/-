import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
from weather_get import weather_15days


def bg_choose(wea):
    flag, flag_r = 0, 0
    if '晴' in wea:
        flag = 1
        file = 'image_bg/sunny.jpg'
    elif '雨' in wea:
        flag_r = 1
        file = 'image_bg/rainy.jpg'
    elif '云' in wea or flag == flag_r:
        file = 'image_bg/cloudy.jpg'
    return file

def pic_get(url, name):

     wea_15 = weather_15days(url)
     temp_max = wea_15['每日最高气温']
     temp_min = wea_15['每日最低气温']
     wea_list = wea_15['每日天气']
     date, week = wea_15['日期'], wea_15['星期']
     pyl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
     pyl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

     f=plt.figure(figsize=(20, 8), dpi=100)
     x = range(1, 17)

     x_ticks_label = date
     y_ticks = range(46)
     h = list(map(float, temp_max))
     l = list(map(float, temp_min))
     pyl.title(f"{name}15日内气温变化趋势图", fontsize='20')
     pyl.xlabel('日期', fontsize='15')  # 刻度显示
     plt.xticks(x, x_ticks_label)
     plt.yticks(y_ticks[::2])
     # 添加网格显示
     plt.grid(True, linestyle="--", alpha=0.5)

     pyl.ylabel('温度℃', fontsize='15')
     plt.plot(x, h, color='r', marker='o', linestyle='--', label="每日最高温度")
     plt.plot(x, l, color='b', marker='o', linestyle='-', label="每日最低温度")

     plt.legend()
     pyl.xlim(0, 17)
     pyl.ylim(0, 46)
     #pyl.show()
     return f

