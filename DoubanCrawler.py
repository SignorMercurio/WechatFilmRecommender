# -*- coding:utf-8 -*-
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

film_ctg = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语',
                  '欧美', '韩国', '日本', '动作', '喜剧', '爱情', '科幻', '悬疑',
                  '恐怖']
film_heat = []
film_time = []
film_rating = []
command_cache = []
film_detail = []


class Crawler(object):
    # download latest movie info from douban
    def __init__(self):
        self.driver = webdriver.Chrome("E:\Python\Scripts\chromedriver.exe")  # modify this to your own path
        self.douban_url_base = 'https://movie.douban.com/'
        self.url_category = ''
        self.url_picture = ''
        self.url_film_detail = []

    def cmd2ctg(self, cmd):
        """
        url_category: https://movie.douban.com/explore
        can also be extended to books, music, etc.
        :param cmd:
        :return:
        """
        if ('电影' in cmd):
            self.url_category = self.douban_url_base + 'explore'

    def browser_hotopen(self):
        """
        hotopen chrome before sender type in any words
        :return:
        """
        self.driver.get(self.douban_url_base)

    def browser_action_general_info(self, type_cmd):
        """
        chrome browser acts to crawl the general info to users (movie name & rating)
        :param type_cmd:
        :return:
        """
        self.driver.get(self.url_category)
        sleep(1)
        for i in range(0, len(film_ctg)):
            if type_cmd == film_ctg[i]:
                self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]'
                                                  '/form/div[1]/div[1]/label[{}]'.format(i+1)).click()
        sleep(1)
        self.browser_crawl_general_info()
        return film_heat + film_time + film_rating

    def browser_crawl_general_info(self):
        """
        crawl the general info from douban
        :return:
        """
        # delete film_xx for next search
        del film_heat[:]
        del film_time[:]
        del film_rating[:]
        for i in range(1, 4):
            # click in order
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div'
                                              '[1]/form/div[3]/div[1]/label[{}]/input'.format(i)).click()
            sleep(1)
            # constructing three lists of top 10 films
            for cnt in range(1, 11):
                if i == 1:
                    film_heat.append(self.get_film_general_info(cnt))
                elif i == 2:
                    film_time.append(self.get_film_general_info(cnt))
                elif i == 3:
                    film_rating.append(self.get_film_general_info(cnt))
                else:
                    pass
        self.format_info()

    def get_film_general_info(self, cnt):
        """
        Using xpath to get the info of the selected film
        :param cnt:
        :return:
        """
        ret = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]'
                                                '/div/div[4]/div/a[{}]/p'.format(cnt)).text
        return ret

    @staticmethod
    def format_info():
        """
        beautify the general info collected
        :return:
        """
        for i in range(0, len(film_heat)):
            film_heat[i] = film_heat[i].replace(' ', ':  ')
            film_time[i] = film_time[i].replace(' ', ':  ')
            film_rating[i] = film_rating[i].replace(' ', ':  ')
            film_heat[i] = str(i+1) + '.' + film_heat[i] + '分'
            film_time[i] = str(i+1) + '.' + film_time[i] + '分'
            film_rating[i] = str(i+1) + '.' + film_rating[i] + '分'

    def browser_action_detail_info(self, cnt, film_name):
        """
        chrome browser acts to crawl the detail info for users
        :param cnt:
        :param film_name:
        :return:
        """
        film_click = 0
        # click the type of movie
        for i in range(0, len(film_ctg)):
            if command_cache[0] == film_ctg[i]:
                self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]'
                                                  '/form/div[1]/div[1]/label[{}]'.format(i+1)).click()
        sleep(1)
        # click the type of order
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div'
                                          '[1]/form/div[3]/div[1]/label[{}]/input'.format(cnt)).click()
        sleep(1)
        if cnt == 1:
            for x in range(0, len(film_heat)):
                if film_name in film_heat[x]:
                    film_click = x + 1
        elif cnt == 2:
            for x in range(0, len(film_time)):
                if film_name in film_time[x]:
                    film_click = x + 1
        else:
            for x in range(0, len(film_rating)):
                if film_name in film_rating[x]:
                    film_click = x + 1
        # click film name for detail info
        film_detail_url = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div/a[{}]'
                                                             .format(film_click)).get_attribute('href')
        return film_detail_url

    @staticmethod
    def parse_detail_info(html_result):
        """
        parse the html downloaded
        :param html_result:
        :return:
        """
        del film_detail[:]

        film_name = ''
        actors = '主演: '
        director = '导演: '
        film_type = '类型: '
        date = '上映日期: '
        duration = '片长: '
        soup = BeautifulSoup(html_result, 'lxml')

        film_name += soup.find('span', property='v:itemreviewed').string.strip()\
            + soup.find('span', class_='year').string.strip()
        director += soup.find('a', rel='v:directedBy').string.strip()
        for x in soup.find_all('a', rel='v:starring'):
            actors += x.string.strip() + '  '
        for x in soup.find_all('span', property='v:genre'):
            film_type += x.string.strip() + '  '
        for x in soup.find_all('span', property='v:initialReleaseDate'):
            date += x.string.strip() + '  '
            duration += soup.find('span', property='v:runtime').string.strip()

        film_detail.append(film_name)
        film_detail.append(director)
        film_detail.append(actors)
        film_detail.append(film_type)
        film_detail.append(date)
        film_detail.append(duration)

    @staticmethod
    def download_detail_info_html(url_target):
        """
        download the target html
        :param url_target:
        :return:
        """
        try:
            response = urllib.request.Request(url_target, headers=headers)
            result = urllib.request.urlopen(response)
            html = result.read().decode('utf-8')
            return html
        except urllib.error.HTTPError as e:
            if hasattr(e, 'code'):
                print('Error code: ' + e.code)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Error reason: ' + e.reason)


if __name__ == '__main__':
    douban_crawler = Crawler()
    douban_crawler.url_category = 'https://movie.douban.com/explore'


