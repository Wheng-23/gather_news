from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

from config.mysqlop import Mysqlop
#
id = 159
a = Mysqlop()
# a.clearData()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.nato.int/cps/en/natohq/news.htm")
driver.maximize_window()
time.sleep(3)

# /html/body/div[1]/div/article/div/div/div/table/tbody/tr[1]/td[3]/p/a
# /html/body/div[1]/div/article/div/div/div/table/tbody/tr[2]/td[3]/p/a
newslist = driver.find_elements(By.XPATH,'/html/body/div[1]/div/article/div/div/div/table/tbody/tr/td[3]/p/a')
link_list = []
for article in newslist:
    link_list.append(article.get_attribute('href'))
# print(link_list)

for link in link_list:
    driver.get(link)
    newstime = driver.find_element(By.XPATH, '/html/body/div[1]/div/article/div/div[1]/div/ul[1]/li[1]').text
    print(type(newstime))
    print(newstime)
    # newstime = datetime.strptime(newstime, "%d %b. %Y -").strftime("%B %d, %Y").upper()
    # print(newstime)
    # 去除字符串末尾的横杠（如果有的话）
    newstime = newstime.strip(' -')
    # 检测是否包含两个日期
    if '-' in newstime:
        # 分割字符串并取最后一个日期部分
        newstime = newstime.split('-')[-1].strip()
    date = datetime.strptime(newstime, '%d %b. %Y')
    newstime = date.strftime('%B %d, %Y').upper()
    newstime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
    source = 'North Atlantic Treaty Organization'
    print(type(source))
    print(source)
    title = driver.find_element(By.CSS_SELECTOR, ".fs-huge").text
    print(type(title))
    print(title)
    title = title.replace("'", "''")
    text = driver.find_element(By.XPATH, '/html/body/div[1]/div/article/div/div[1]/div/section').text
    print(type(text))
    print(text)
    text = text.replace("'", "''")
    result = a.saveData(id, source, newstime, title, text)
    if result:
        id = id + 1
    else:
        print("id不增加")


for i in range(9):
    # driver.get("https://www.whitehouse.gov/briefing-room/page/%d/"%(i+2))
    driver.get("https://www.nato.int/cps/en/natohq/news.htm?&chunk=%d"%(i+2))
    time.sleep(3)
    newslist = driver.find_elements(By.XPATH,'/html/body/div[1]/div/article/div/div/div/table/tbody/tr/td[3]/p/a')
    link_list = []
    for article in newslist:
        link_list.append(article.get_attribute('href'))
    print(link_list)
    for link in link_list:
        driver.get(link)
        newstime = driver.find_element(By.XPATH, '/html/body/div[1]/div/article/div/div[1]/div/ul[1]/li[1]').text
        print(type(newstime))
        print(newstime)
        # 去除字符串末尾的横杠（如果有的话）
        newstime = newstime.strip(' -')
        # 检测是否包含两个日期
        if '-' in newstime:
            # 分割字符串并取最后一个日期部分
            newstime = newstime.split('-')[-1].strip()
        date = datetime.strptime(newstime, '%d %b. %Y')
        newstime = date.strftime('%B %d, %Y').upper()
        newstime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

        source = 'North Atlantic Treaty Organization'
        print(type(source))
        print(source)
        title = driver.find_element(By.CSS_SELECTOR, ".fs-huge").text
        print(type(title))
        print(title)
        title = title.replace("'", "''")
        text = driver.find_element(By.XPATH, '/html/body/div[1]/div/article/div/div[1]/div/section').text
        print(type(text))
        print(text)
        text = text.replace("'", "''")
        result = a.saveData(id, source, newstime, title, text)
        if result:
            id = id + 1
        else:
            print("id不增加")
# input()
driver.quit()