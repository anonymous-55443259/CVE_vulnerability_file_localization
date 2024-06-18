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
    url = 'https://mitogen.networkgenomics.com/changelog.html#v0-2-8-2019-08-18'
    res = scrapy(url)
    print(res)