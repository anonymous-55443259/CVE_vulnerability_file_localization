from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapy(url: str):

    res = ''
    if any(item in url for item in ['2730', 'docId=emr_na-c05184351', 'emr_na-hpesbhf03750en_us', 'emr_na-c05398322', 'emr_na-hpesbhf03836en_us']):
        return res

    driver = webdriver.Chrome()
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'IE8'))
    )

    # content = driver.page_source
    # with open('./test/test.html', 'w') as f:
    #     print(content, file=f)

    info = driver.find_element(By.CLASS_NAME, 'IE8')

    trs = info.find_elements(By.TAG_NAME, 'div')
    flag = True
    for item in trs[6:-6]:
        class_name = item.get_attribute('class')
        # print(class_name)
        if class_name == 'background.text':
            flag = False
        if class_name == 'resolution' and 'c05349499' not in url:
            flag = True
        if flag:
            res += item.text
    driver.quit()

    return res

if __name__ == '__main__':
    url = 'https://h20566.www2.hpe.com/portal/site/hpsc/public/kb/docDisplay?docId=emr_na-c05390722'
    res = scrapy(url)
    print(res)