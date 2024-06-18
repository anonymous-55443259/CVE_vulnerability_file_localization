import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    if url in ['http://seclists.org/bugtraq/2016/Mar/90']:
        return res

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'h1', attrs = {
        'class' : 'm-title',
    })
    if info != None:
        # print(info.text)
        res += 'Title:\n' + info.text + '\n\n'

    info = soup.find(name = 'pre', attrs = {
        'style' : 'margin: 0em;',
    })
    if info != None:
        # print(info.text)
        res += 'Content:\n' + info.text + '\n\n'

    info = soup.find(name = 'ul', attrs = {
        'class' : 'thread',
    })
    if info != None:
        # print(info.text)
        res += 'Current thread:' + info.text + '\n\n'
    
    return res

if __name__ == '__main__':
    url = 'https://seclists.org/bugtraq/2019/Jun/26'
    res = scrapy(url)
    print(res)