import requests
from bs4 import BeautifulSoup
import json


def pro_change(name):
    with open('province.json', 'r', encoding='utf-8') as fp:
        data = json.loads(fp.read())
    return data[name]


class GetCityUrl:

    def __init__(self, province_name):
        self.province_name = province_name
        self.city_url_list = []#存放城市天气地址
        self.city_name_list = []#存放城市名称
        self.city_data = {}

    def get_data(self):
        url = f"https://tianqi.moji.com/forecast15/china/{self.province_name}"
        # 先在一个省级行政单位里进行精细的查询，得到具体城区的天气查询网址
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        self.data = soup.find_all('div', attrs={'class': 'city_hot'})
        self.data_li = self.data[0].find_all('li')
        for d in self.data_li:
            city_url = d.find('a')['href']
            city_name = d.find('a').string
            self.city_url_list.append(city_url)
            self.city_name_list.append(city_name)
        for i in range(len(self.city_name_list)):
            self.city_data[self.city_name_list[i]] = self.city_url_list[i]#制作下拉式菜单的数据


