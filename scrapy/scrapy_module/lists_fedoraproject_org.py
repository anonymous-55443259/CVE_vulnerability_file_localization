import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    if 'archives' in url:
        return scrapy_archives(url)
    else:
        from . import common
        return common.scrapy(url)


def scrapy_archives(url: str):
    
    res = ''
    if 'Z4UHHIGISO3FVRF4CQNJS4IKA25ATSFU' in url:
        return res

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'class' : 'col-tn-10',
    })
    if info != None:
        # print(info.text)
        res += 'Title:\n' + info.text + '\n'

    info = soup.find(name = 'div', attrs = {
        'class' : 'email-body',
    })
    if info != None:
        # print(info.text)
        res += 'Post:' + info.text

    return res

if __name__ == '__main__':
    url = 'https://lists.fedoraproject.org/archives/list/package-announce%40lists.fedoraproject.org/message/TXRVXNRFHJSQWFHPRJQRI5UPMZ63B544/'
    res = scrapy(url)
    print(res)