# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests
import re

class Proxies(object):

    """docstring for Proxies"""

    def __init__(self, page=10, url='https://www.baidu.com'):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.url = url
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies_nn()
        data5u = [
            # "http://www.data5u.com/", 
            # "http://www.data5u.com/free/index.html", 
            # "http://www.data5u.com/free/gnpt/index.shtml",
            # "http://www.data5u.com/free/gwpt/index.shtml"
            "http://www.data5u.com/free/gngn/index.shtml",
            "http://www.data5u.com/free/gwgn/index.shtml",
            ]
        for url in data5u:
            self.get_proxies_data5u(url)

    def get_proxies(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.headers, proxies={'http':'http://122.242.89.145:8010'}).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            try:
                for odd in ip_list.find_all(class_='odd'):
                    protocol = odd.find_all('td')[5].get_text().lower() + '://'
                    self.proxies.append(
                        protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            except Exception:
                break
            page += 1

    def get_proxies_nn(self): #高匿
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            html = requests.get(url, headers=self.headers, proxies={'http':'http://122.242.89.145:8010'}).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            try:
                for odd in ip_list.find_all(class_='odd'):
                    protocol = odd.find_all('td')[5].get_text().lower() + '://'
                    self.proxies.append(
                        protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            except Exception:
                pass
            page += 1
            time.sleep(1)

    def get_proxies_data5u(self, url):
        html = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(html, 'lxml')
        ip_list = soup.find_all('ul', class_='l2')
        try:
            for line in ip_list:
                protocol = line.find_all(class_='href', string=re.compile('http'))[0].text
                ip = line.li.text
                port = line.find(class_='port').text
                self.proxies.append("%s://%s:%s" % (protocol, ip, port))
        except Exception as e:
            print(e)

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy,
                                 args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:
                break
            #protocol = 'https' if 'https' in proxy else 'http'
            proxies = {'http': proxy, 'https': proxy}
            try:
                if requests.get(self.url, proxies=proxies, timeout=15).status_code == 200:
                    print('success %s' % proxy)
                    new_queue.put(proxy)
            except Exception as e:
                pass


if __name__ == '__main__':
    a = Proxies()
    a.verify_proxies()
    print(a.proxies)
    proxie = a.proxies
    with open('proxies.txt', 'a') as f:
        for proxy in proxie:
            f.write(proxy + '\n')
