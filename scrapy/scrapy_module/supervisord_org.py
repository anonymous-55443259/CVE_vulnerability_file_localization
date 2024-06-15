import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    id = url.split('#')[-1]
    info = soup.find(name = 'section', attrs = {
        'id' : id,
    })
    if info != None:
        res += info.text

    return res


if __name__ == '__main__':
    url = 'http://supervisord.org/configuration.html#inet-http-server-section-settings'
    res = scrapy(url)
    print(res)