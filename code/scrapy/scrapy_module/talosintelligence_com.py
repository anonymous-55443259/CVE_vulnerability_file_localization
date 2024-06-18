import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    cve = url.split('#')[-1].lower()
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.find(name = 'div', attrs = {
        'class' : 'col-12 report',
    })
    if info:
        try:
            res += info.h2.text + '\n'
            info = info.div
            
            flag = False
            count = 0
            for element in info:
                if element.name == 'h4':
                    element_id = element.get('id')
                    if element_id.startswith('cve-'):
                        r = element_id.find('---')
                        cve_id = element_id[:r].lower()
                        if cve_id != cve:
                            flag = True
                        else:
                            flag = False
                            count = 1
                if flag:
                    element.decompose()
                if count and element.name == 'pre':
                    if count == 2:
                        element.decompose()
                        count = 0
                    else:
                        count += 1
        except Exception as e:
            pass
        res += info.text
    return res


if __name__ == '__main__':
    url = 'https://talosintelligence.com/vulnerability_reports/TALOS-2021-1297#CVE-2021-21836'
    res = scrapy(url)
    print(len(res))