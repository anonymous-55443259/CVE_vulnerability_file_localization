import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    info = soup.pre
    if info != None:
        # print(info.text)
        res += info.text
    
    l = res.find('BEGIN PGP SIGNATURE')
    r = res.rfind('END PGP SIGNATURE')
    if l != -1 and r != -1:
        res = res[:l] + res[r:]

    return res


if __name__ == '__main__':
    url = 'https://www.openwall.com/lists/oss-security/2021/12/23/2'
    res = scrapy(url)
    print(res)