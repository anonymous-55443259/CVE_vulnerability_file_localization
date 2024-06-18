import requests
from bs4 import BeautifulSoup

def scrapy(url: str):
    if 'errata' in url:
        return scrapy_errata(url)
    else:
        from . import common
        return common.scrapy(url)

def scrapy_errata(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'id' : 'synpopsis',
    })
    if info != None:
        # print(info.text)
        res += info.text

    info = soup.find(name = 'div', attrs = {
        'id' : 'topic',
    })
    if info != None:
        # print(info.text)
        res += info.text

    info = soup.find(name = 'div', attrs = {
        'id' : 'description',
    })
    if info != None:
        # print(info.text)
        res += info.text

    info = soup.find(name = 'div', attrs = {
        'id' : 'affected_products',
    })
    if info != None:
        # print(info.text)
        res += info.text

    info = soup.find(name = 'div', attrs = {
        'id' : 'fixes',
    })
    if info != None:
        # print(info.text)
        res += info.text
    
    return res


if __name__ == '__main__':
    url = 'https://access.redhat.com/errata/RHSA-2017:2918'
    res = scrapy(url)
    print(res)