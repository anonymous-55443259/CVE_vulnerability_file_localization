from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapy(url: str):

    res = ''

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'searchresults'))
    )

    # content = driver.page_source
    # with open('./test/test.html', 'w') as f:
    #     print(content, file=f)

    title = driver.find_element(By.CLASS_NAME, 'reportid').text
    # print(title)
    res += 'Title:\n' + title + '\n\n'

    detail1 = driver.find_element(By.CLASS_NAME, 'detailsline').text
    detail2 = driver.find_element(By.CLASS_NAME, 'description').text
    # print(detail1)
    # print(detail2)
    res += 'Detail:\n' + detail1 + '\n' + detail2 + '\n\n'

    titles = ['Consequences:\n', 'Remedy:\n', 'Parameters:\n']
    info = driver.find_elements(By.CLASS_NAME, 'detailssubsection')
    # print(len(info))
    for index, item in enumerate(info):
        # print(item.text)
        res += titles[index] + item.text + '\n\n'

    driver.quit()

    return res

if __name__ == '__main__':
    url = 'https://exchange.xforce.ibmcloud.com/vulnerabilities/83347'
    res = scrapy(url)
    print(res)