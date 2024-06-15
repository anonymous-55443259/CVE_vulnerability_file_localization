import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    # id = url.split('#')[-1]

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'article', attrs = {
        'class' : 'md-content__inner md-typeset',
    })
    if info != None:
        # print(len(info))
        for i, item in enumerate(info):
            if 1226 < i < 1245:
                res += item.text
            # if isinstance(item, element.Tag):
            #     print(item.get('id'))

    return res


if __name__ == '__main__':
    url = 'https://nokogiri.org/CHANGELOG.html#154-2012-06-12'
    res = scrapy(url)
    print(res)