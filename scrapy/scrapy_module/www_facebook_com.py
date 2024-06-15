import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'class' : 'pal _rj1',
    })
    if info != None:
        # print(info.text)
        res += info.text

    return res


if __name__ == '__main__':
    url = 'https://www.facebook.com/security/advisories/cve-2019-3565'
    res = scrapy(url)
    print(res)