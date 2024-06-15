import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    if '#' in url:
        info = soup.find(name = 'div', attrs = {
            'id' : url.split('#')[-1],
        })
        if info != None:
            res += info.text
    else:
        info = soup.find(name = 'section', attrs = {
            'id' : 'security-fix',
        })
        if info == None:
            info = soup.find(name = 'div', attrs = {
                'id' : 'security-fix',
            })
        if info != None:
            res += info.text
    
    return res


if __name__ == '__main__':
    url = 'https://docs.saltstack.com/en/latest/topics/releases/2015.8.4.html'
    res = scrapy(url)
    print(res)