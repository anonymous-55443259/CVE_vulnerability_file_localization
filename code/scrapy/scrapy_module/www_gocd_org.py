import requests
from bs4 import BeautifulSoup, element


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'id' : 'tab-' + url.split('#')[-1]
    })
    if info != None:
        res += info.text
        
    return res


if __name__ == '__main__':
    url = 'https://www.gocd.org/releases/#22-1-0'
    res = scrapy(url)
    print(res)