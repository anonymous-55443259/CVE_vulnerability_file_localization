import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    info = soup.find(name = 'div', attrs = {
        'id' : 'content',
    })

    info.find(name = 'div', attrs = {
        'class' : 'text',
    }).decompose()

    info.find(name = 'div', attrs = {
        'class' : 'text',
    }).decompose()

    if '#' in url:
        cve = url.split('#')[-1]
        cve_p = info.text.find(cve)
        l = info.text.rfind('Fixed in Apache Tomcat', 0, cve_p)
        r = info.text.find('Fixed in Apache Tomcat', cve_p)
        res += info.text[l:r]
    else:
        res += info.text
    return res


if __name__ == '__main__':
    url = 'https://tomcat.apache.org/security-8.html'
    res = scrapy(url)
    print(res)