import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    
    id = url.split('#')[-1]

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'section', attrs = {
        'id' : id,
    })
    if info != None:
        res += info.text

    return res


if __name__ == '__main__':
    url = 'http://borgbackup.readthedocs.io/en/stable/changes.html#version-1-1-3-2017-11-27'
    res = scrapy(url)
    print(res)