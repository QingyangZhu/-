import requests
from bs4 import BeautifulSoup


def weather_today(city_url):
    # 查询某城市的当前天气情况
    city_url_today = city_url.replace('forecast15', 'weather')
    city_url_today1 = city_url.replace('forecast15', 'today')
    res = requests.get(city_url).text
    soup = BeautifulSoup(res, 'html.parser')
    data = soup.find('div', attrs={'class': 'detail_weather clearfix'})
    res_today = requests.get(city_url_today).text
    res_today1 = requests.get(city_url_today1).text
    soup_today = BeautifulSoup(res_today, 'html.parser')
    soup_today1 = BeautifulSoup(res_today1, 'html.parser')
    data_air = soup_today.find('div', attrs={'class': "wea_alert clearfix"})#空气质量
    data_wind_wet = soup_today.find('div', attrs={'class': "wea_about clearfix"})#风向和湿度情况
    data_tip = soup_today.find('div', attrs={'class': "wea_tips clearfix"})#生活建议
    data_life = soup_today.find('div', attrs={'class': "live_index_grid"})
    data_c = soup_today1.find('div', attrs={'class': "detail_ware_title"})
    data_cloth = data_c.find('span')
    air = data_air.find('em').text
    wind = data_wind_wet.find('em').text
    wet = data_wind_wet.find('span').text
    tip = data_tip.find('em').text
    temps = []
    #存储当天最高和最低气温
    for d in data.find_all('em'):
        temp = d.text
        temps.append(temp)
    weather = data.span.text#天气情况
    whole = data_life.find_all('dl')

    clo_tip = data_cloth.text
    life_dic = {}#存放生活指南
    life_item = []#存放生活指南的标签，比如‘运动’
    life_value = []#存放生活指南的建议值，比如‘不适宜’
    i = 0
    for item in whole:
        # print(item.text)
        life_item.append(whole[i].find('dd').text)
        life_value.append(whole[i].find('dt').text)
        life_dic[life_item[i]] = life_value[i]
        i += 1
    return {'最高气温': max(temps), '最低气温': min(temps),
            '天气': weather, '空气质量': air,
            '风况': wind, '湿度': wet,
            '提示': tip,
            '生活指南': life_dic,
            '穿衣提醒': clo_tip}
    # 返回当天的最高/最低气温和天气情况和空气质量


def weather_15days(city_url):
    #查询某城市15天的天气情况
    res = requests.get(city_url).text
    soup = BeautifulSoup(res, 'html.parser')
    data = soup.find_all('ul', attrs={'class': 'clearfix'})
    days = data[0].find_all('li')
    temps_max = []#15天每天的最高温度
    temps_min = []#15天每天的最低温度
    wea_days = []#15天每天的天气情况
    date_days = []#15天的日期
    week_days = []#15天的星期
    i = 0
    for day in days:
        temp_max = day.find('b').text  # 存放最高温度的标签
        temp_min = day.find('strong').text  # 存放最低温度的标签
        wea_day = day.find('span', attrs={'class': 'wea'}).text  # 存放每日天气的标签
        spans = days[i].find_all('span')  # 读取每一天li标签下的span标签
        span_data = spans[5]  # 第六个span标签存放日期
        span_week = spans[0]  # 第一个span标签存放星期
        date_day = span_data.text
        week_day = span_week.text
        date_days.append(date_day)
        week_days.append(week_day)
        temps_max.append(temp_max[:-1])
        temps_min.append(temp_min[:-1])
        wea_days.append(wea_day)
        i += 1

    return {'每日最高气温': temps_max,
            '每日最低气温': temps_min,
            '每日天气': wea_days,
            '日期': date_days,
            '星期': week_days}
