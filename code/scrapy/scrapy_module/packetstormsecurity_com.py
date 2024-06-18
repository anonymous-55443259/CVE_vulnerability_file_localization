import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    try:
        info = soup.dl.dt
        if info != None:
            # print(info.text)
            res += 'Title:\n' + info.text + '\n\n'

        info = soup.find(name = 'dd', attrs = {
            'class' : 'detail',
        })
        if info != None:
            # print(info.text)
            res += 'Description:\n' + info.text + '\n\n'

        info = soup.find(name = 'div', attrs = {
            'class' : 'src',
        })
        if info != None:
            # print(info.text)
            res += 'Code:' + info.text
    except Exception:
        pass

    if '157080' in url:
        l = res.find('@osf_wrapper_start')
        r = res.find('@cr_regex = /(')
        # print(l, r)
        res = res[:l] + res[r:]

    return res

if __name__ == '__main__':
    url = 'http://packetstormsecurity.com/files/157080/DotNetNuke-Cookie-Deserialization-Remote-Code-Execution.html'
    res = scrapy(url)
    print(res)