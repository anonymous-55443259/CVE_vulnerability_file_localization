import requests
from bs4 import BeautifulSoup


def scrapy(url: str):

    res = ''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    info = soup.h1
    if info != None:
        res += 'Title:\n' + info.text + '\n\n'

    info = soup.find_all(name = 'pre', attrs = {
        'class' : 'message',
    })
    for item in info:
        l = item.text.find('Checksums-Sha1:')
        r = item.text.find('-----END PGP SIGNATURE-----')
        if l != -1 and r != -1:
            res += item.text[:l] + item.text[r:]
        else:
            res += item.text
    
    if '751417' in url:
        r = res.find('-- Package-specific info:')
        res = res[:r]
    elif '782515' in url or '770492' in url:
        r = res.find('** Kernel log:')
        res = res[:r]
    elif '766195' in url:
        r = res.find('which resulted')
        res = res[:r]
    elif '774155' in url or '823603' in url:
        r = res.find('-----BEGIN PGP SIGNED MESSAGE')
        res = res[:r]
    elif '654876' in url:
        r = res.find('** PCI devices:')
        res = res[:r]
        
    return res


if __name__ == '__main__':
    url = 'https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=911639'
    res = scrapy(url)
    print(res)
