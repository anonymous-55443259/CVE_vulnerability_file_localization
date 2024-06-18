from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapy(url: str):

    res = ''

    if any(item in url for item in ['r14a', '940b4', 'r107c', 'rd0e9', 'dbsvg', 'r489886fe72a98768e', 'r059b042bca47be5']):
        return res

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'chatty_body'))
    )

    # content = driver.page_source
    # print(content)

    title = driver.find_element(By.CLASS_NAME, 'chatty_title').text
    content = driver.find_elements(By.CLASS_NAME, 'chatty_body')
    # print(type(content))        # list，每个元素是帖子内容
    # print(len(content))
    
    res += 'Title:\n' + f'{title}\n\n' + 'Post:\n'
    flag = False
    for index, post in enumerate(content):
        # print(index)
        if len(post.text) < 50000:
            res += 'Post' + f'{index + 1}' + ':\n' + post.text + '\n'
            flag = True
    driver.quit()
    
    if not flag:
        res = ''
    return res

if __name__ == '__main__':
    url = 'https://www.php.net/releases/5_2_3.php'
    res = scrapy(url)
    print(res)