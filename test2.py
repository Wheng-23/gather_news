from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime as dt
import time

def update_german_data():
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.bmvg.de/de/presse/alle-pressetermine-pressemitteilungen-bmvg")
    # /html/body/div[3]/div/div/div[2]/button[3]/span
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/button[3]').click()
    driver.maximize_window()

    # time.sleep(3)
    # driver.find_element(By.CSS_SELECTOR, ".result-list__more-btn").click()
    # time.sleep(3)
    # driver.find_element(By.CSS_SELECTOR, ".result-list__more-btn").click()
    # time.sleep(3)
    newslist = driver.find_elements(By.XPATH, '//*[@id="r-main"]/section[3]/div[2]/div[2]/div/div/ol/li/article/a')
    link_list = []
    for article in newslist:
        link_list.append(article.get_attribute('href'))
    print(link_list)
    for link in link_list:
        driver.get(link)
        newstime = driver.find_element(By.XPATH,
                                       '//*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/span[2]/span/span[2]').text
        print(type(newstime))
        print(newstime)
        # 转换为日期对象
        date_obj = dt.strptime(newstime, "%d.%m.%Y")
        # 转换为所需格式
        newstime = date_obj.strftime("%B %d, %Y").upper()
        print(newstime)
        datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        print(datetime)

        source = 'German Federal Ministry of Defence'
        print(type(source))
        print(source)

        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1/text()
        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div[2]/div[1]/article/div[2]/h3/a
        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1
        title = driver.find_element(By.XPATH,
                                    '//*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        text = driver.find_element(By.XPATH, '//*[@id="r-main"]/section[3]/div/div/div/div/div').text
        print(type(text))
        print(text)
        text = text.replace("'", "''")

    driver.quit()


if __name__ == '__main__':
    update_german_data()