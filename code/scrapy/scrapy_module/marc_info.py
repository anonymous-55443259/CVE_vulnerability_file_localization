import requests


def scrapy(url: str):

    res = ''
    if 'w=2' in url:
        url = url.replace('w=2', 'q=mbox')
    else:
        url += '&q=mbox'
    
    if '152023808817590' in url:
        res = requests.get(url).text[175:5912]
    elif '120428209704324' in url or '142804214608580' in url:
        pass
    else:
        res = requests.get(url).text
    
    return res


if __name__ == '__main__':
    url = 'https://marc.info/?l=linux-netdev&m=152023808817590&w=2'
    res = scrapy(url)
    print(res)