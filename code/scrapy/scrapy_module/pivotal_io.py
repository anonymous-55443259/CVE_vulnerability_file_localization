import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    if 'cve-2015-3189' in url or 'cve-2016-9877' in url:
        from . import tanzu_vmware_com
        return tanzu_vmware_com.scrapy(url)

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'class' : 'column content is-8',
    })
    if info != None:
        # print(info.text)
        res += info.text

    return res


if __name__ == '__main__':
    url = 'https://spring.io/security/cve-2019-3795'
    res = scrapy(url)
    print(res)