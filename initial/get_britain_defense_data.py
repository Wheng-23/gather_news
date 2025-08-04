from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config.mysqlop import Mysqlop
#
id = 294
a = Mysqlop()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.gov.uk/search/news-and-communications?")
# https://www.gov.uk/search/news-and-communications?page=1
driver.maximize_window()
# //*[@id="js-results"]/div/ul/li[1]/div/a
# //*[@id="js-results"]/div/ul/li[2]/div/a
newslist = driver.find_elements(By.XPATH,'//*[@id="js-results"]/div/ul/li/div/a')
link_list = []
for article in newslist:
    link_list.append(article.get_attribute('href'))
print(link_list)

for link in link_list:
    driver.get(link)
    try:
        newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/dl/dd[2]').text
        print(type(newstime))
        print(newstime)
        # 将字符串解析为日期对象
        date_obj = datetime.strptime(newstime, "%d %B %Y")
        # 格式化日期对象为指定格式的字符串
        newstime = date_obj.strftime("%B %d, %Y").upper()
        # 输出结果
        print(newstime)
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

        source = 'British Ministry of Defence'
        print(type(source))
        print(source)

        title = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/h1').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        text = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div').text
        print(type(text))
        print(text)
        text = text.replace("'", "''")

        result = a.saveData(id, source, newstime, title, text,datetime)
        if result:
            id = id + 1
        else:
            print("id不增加")
    except Exception as e:
        print(f"An error occurred while processing the link {link}: {e}")

for i in range(5):
    driver.get("https://www.gov.uk/search/news-and-communications?page=%d"%(i+2))
    time.sleep(3)
    newslist = driver.find_elements(By.XPATH, '//*[@id="js-results"]/div/ul/li/div/a')
    link_list = []
    for article in newslist:
        link_list.append(article.get_attribute('href'))
    print(link_list)
    for link in link_list:
        driver.get(link)
        try:
            # //*[@id="content"]/div[2]/div/div[1]/div/dl/dd[2]
            # //*[@id="content"]/div[2]/div/div[1]/div/dl/dd[3]/text()
            newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/dl/dd[2]').text
            print(type(newstime))
            print(newstime)
            # 将字符串解析为日期对象
            date_obj = datetime.strptime(newstime, "%d %B %Y")
            # 格式化日期对象为指定格式的字符串
            newstime = date_obj.strftime("%B %d, %Y").upper()
            # 输出结果
            print(newstime)
            datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

            source = 'British Ministry of Defence'
            print(type(source))
            print(source)

            title = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/h1').text
            print(type(title))
            print(title)
            title = title.replace("'", "''")

            text = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div').text
            print(type(text))
            print(text)
            text = text.replace("'", "''")

            result = a.saveData(id, source, newstime, title, text,datetime)
            if result:
                id = id + 1
            else:
                print("id不增加")
        except Exception as e:
            print(f"An error occurred while processing the link {link}: {e}")

driver.quit()