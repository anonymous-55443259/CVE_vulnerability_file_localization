import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    version = url.split('#')[-1]
    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.body
    if info:
        res += info.text
    if version == '1.10.2':
        l = res.find('1.10.2')
        r = res.find('1.10.3')
        res = res[l:r]
    elif version == '1.10.3':
        l = res.find('1.10.3')
        r = res.find('1.10.4')
        res = res[l:r]
    return res


if __name__ == '__main__':
    
    url = 'https://gstreamer.freedesktop.org/releases/1.10/#1.10.3'
    res = scrapy(url)
    print(len(res))