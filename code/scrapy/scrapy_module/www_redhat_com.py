import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    if 'archives' in url:
        return scrapy_archives(url)
    else:
        return ''


def scrapy_archives(url: str):
    
    res = ''
    if '2009-June/msg01193' in url or '2009-May/msg01271' in url:
        return res

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    info = soup.h1
    if info != None:
        # print(info.text)
        res += 'Title:\n' + info.text + '\n\n'

    info = soup.pre
    if info != None:
        if any(item in url for item in ['232', '357', '784', '397', '256']):
            tp = info.text
            tp = tp[:tp.find('ChangeLog:')] + tp[tp.find('References:'):]
            res += tp[:tp.find('This update')]
        else:
            p = info.text.find('This update')
            res += 'Content:\n' + info.text[:p]

    return res


if __name__ == '__main__':
    url = 'https://www.redhat.com/archives/fedora-package-announce/2009-August/msg01256.html'
    res = scrapy(url)
    print(res)