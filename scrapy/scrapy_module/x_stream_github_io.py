import requests
from bs4 import BeautifulSoup, element


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'id' : 'content',
    })
    if info != None:
        if '#' in url:
            for i, item in enumerate(info):
                if 153 <= i <= 169:
                    res += item.text
        else:
            if info != None:
                res += info.text

    return res


if __name__ == '__main__':
    url = 'https://x-stream.github.io/CVE-2020-26217.html'
    res = scrapy(url)
    print(res)