import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    
    res = ''

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'class' : 'col-10',
    })
    if info != None:
        # print(info.text)
        res += 'Title:' + info.text + '\n'

    info = soup.find(name = 'div', attrs = {
        'class' : 'email-body',
    })
    flag = False
    if info != None:
        # print(info.text)
        if len(info.text) < 50000:
            flag = True
            res += 'Content:' + info.text
    if not flag:
        res = ''

    return res

if __name__ == '__main__':
    url = 'https://lists.opensuse.org/archives/list/security-announce@lists.opensuse.org/message/VOAHRKDA7W6T2DPZV7YKHMSWYSGQCJCW/'
    res = scrapy(url)
    print(res)
