import re
import requests
from bs4 import BeautifulSoup

def scrapy(url: str):

    res = ''
    if '456282' in url:
        return res
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'span', attrs = {
        'id' : 'short_desc_nonedit_display',
    })
    if info != None:
        # print(info.text)
        res += 'Title:\n' + info.text + '\n\n'

    info = soup.find(name = 'table', attrs = {
        'class' : 'edit_form',
    })
    if info != None:
        # print(re.sub(r'\n\s*\n', '\n', info.text))
        res += 'Attributes:' + re.sub(r'\n\s*\n', '\n', info.text) + '\n\n'

    info = soup.find(name = 'div', attrs = {
        'id' : 'comments',
    })
    if info != None:
        # print(re.sub(r'\n\s*\n', '\n', info.text))
        res += 'Comments:' + re.sub(r'\n\s*\n', '\n', info.text)
    
    if '1120843' in url:
        r = res.find('Comment 12')
        res = res[:r]
    elif '1105025' in url or '1069702' in url:
        r = res.find('Comment 7')
        res = res[:r]
    elif '972612' in url:
        r = res.find('Comment 17')
        res = res[:r]
    elif '1045327' in url:
        r = res.rfind('Kernel log message')
        res = res[:r]
    elif '1120386' in url:
        r = res.find('Comment 22')
        res = res[:r]
    elif '1106095' in url:
        r = res.find('Comment 1')
        res = res[:r]
    elif '1157304' in url:
        r = res.find('Comment 8')
        res = res[:r]
    elif '1106512' in url:
        r = res.find('Comment 32')
        res = res[:r]
    elif '1178372' in url:
        r = res.find('Comment 59')
        res = res[:r]
    elif '1157180' in url:
        r = res.find('Comment 15')
        res = res[:r]
    elif '1118152' in url:
        r = res.find('Comment 6')
        res = res[:r]
    elif '1094825' in url:
        r = res.find('Comment 2')
        res = res[:r]

    # save_text('tp', res)
    return res

if __name__ == '__main__':
    url = 'https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2019-10141'
    res = scrapy(url)
    print(res)