import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    id = url.split('#')[-1]
    info = soup.find(name = 'div', attrs = {
        'id' : id,
    })
    if info != None:
        res += info.text

    return res


if __name__ == '__main__':
    url = 'https://docs.pylonsproject.org/projects/waitress/en/latest/#security-fixes'
    res = scrapy(url)
    print(res)