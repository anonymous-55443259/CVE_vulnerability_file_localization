from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapy(url: str):

    res = ''
    if any(invalid_url == url for invalid_url in [
        'https://huntr.dev/bounties/1-other-fiznool/body-parser-xml',
        'https://huntr.dev/bounties/006624e3-35ac-448f-aab9-7b5183f30e28',
        'https://huntr.dev/bounties/9-polonel/trudesk',
        'https://huntr.dev/bounties/d9c17308-2c99-4f9f-a706-f7f72c24c273',
        'https://huntr.dev/bounties/1625557993985-unshiftio/url-parse',
        'https://huntr.dev/bounties/1625558772840-medialize/URI.js',
        'https://huntr.dev/bounties/8da19456-4d89-41ef-9781-a41efd6a1877',
        'https://huntr.dev/bounties/c958013b-1c09-4939-92ca-92f50aa169e8'
    ]):
        return res

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'meta-container'))
    )

    # content = driver.page_source
    # print(content)

    title = driver.find_element(By.ID, 'title').text
    res += title + '\n'

    content = driver.find_element(By.CLASS_NAME, 'markdown-body').text
    res += content + '\n\n'

    parameters = driver.find_element(By.ID, 'meta-container').text
    res += parameters + '\n\n'

    posts = driver.find_elements(By.ID, 'message-body')
    # print(len(posts))
    index = 1
    for post in posts:
        if post.text != "":
            res += 'Post' + f'{index}' + ':\n' + post.text + '\n'
            index += 1

    driver.quit()

    if '635d0abf-7680-47f6-a277-d9a91471c73f' in url:
        l = res.find('!DOCTYPE html')
        r = res.find('Impact')
        # print(l, r)
        res = res[:l] + res[r:]
    elif '9266' in url:
        l = res.find('POST DATA')
        r = res.rfind('%3E', 0) + 3
        res = res[:l] + res[r:]
    elif 'f5f3e468-663b-4df0-8340-a2d77e4cc75f' in url:
        l = res.find('Payload')
        r = res.find('Impact')
        res = res[:l] + res[r:]

    return res


if __name__ == '__main__':
    url = 'https://huntr.com/bounties/dcb37f19-ba53-4498-b953-d21999279266'
    res = scrapy(url)
    print(res)