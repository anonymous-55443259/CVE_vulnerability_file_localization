import requests
from bs4 import BeautifulSoup


def scrapy(url: str):
    # 有个奇怪的问题，有时候开了代理反而访问不了，可能需要手动关掉代理
    
    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.h1
    if info != None:
        # print(info.text)
        res += 'Title:\n' + info.text + '\n\n'

    info = soup.pre
    if info != None:
        res += 'Post:\n' + info.text
        if any(item in url for item in ['1017', '1789', '1503']):
            r = res.find('Upgrade Instructions')
            if r == -1:
                r = res.find('Upgrade instructions')
            res = res[:r]
    else:
        res = ''

    if '2008/dsa-1479' in url or '2006/dsa-1018' in url:
        r = res.find('The following matrix')
        if r != -1:
            res = res[:r]
    elif '2009/dsa-1794' in url or '2009/dsa-1940' in url:
        r = res.find('Upgrade instructions')
        if r != -1:
            res = res[:r]
    elif '2010/dsa-1995' in url or '2010/dsa-1996' in url or '2007/dsa-1249' in url or '2010/dsa-2001' in url:
        r = res.find('For the ')
        if r != -1:
            res = res[:r]
    
    return res


if __name__ == '__main__':
    url = 'https://www.debian.org/security/2021/dsa-4918'
    res = scrapy(url)
    print(res)