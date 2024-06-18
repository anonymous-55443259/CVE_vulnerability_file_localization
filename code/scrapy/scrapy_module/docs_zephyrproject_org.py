import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    
    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    if '#' in url:
        id = url.split('#')[-1]
        info = soup.find(name = 'section', attrs = {
            'id' : id,
        })
        if info != None:
            res += info.text
    else:
        id_list = ['security-vulnerability-related', 'kernel', 'architectures']
        for id in id_list:
            info = soup.find(name = 'div', attrs = {
                'id' : id,
            })
            if info != None:
                res += info.text

    return res


if __name__ == '__main__':
    url = 'https://docs.zephyrproject.org/1.14.0/releases/release-notes-1.14.html'
    res = scrapy(url)
    print(res)