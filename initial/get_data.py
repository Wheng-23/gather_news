import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from config.mysqlop import Mysqlop
#
a = Mysqlop()
id = 1
a.clearData()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.whitehouse.gov/")
driver.maximize_window()
driver.find_element(By.LINK_TEXT,"Briefing Room").click()
time.sleep(3)
#//*[@id="content"]/section[1]/div/div/div[1]/div[2]
#//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article[1]/h2/a
newslist = driver.find_elements(By.XPATH,'//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article/h2/a')
# newslist.find_element(By.CSS_SELECTOR,".news-item__title").click()
# print(driver.find_element(By.CSS_SELECTOR,".posted-on").text)
# print(driver.find_element(By.CSS_SELECTOR,".desktop__logo").text)
# print(driver.find_element(By.CSS_SELECTOR,".page-title").text)
# print(driver.find_element(By.CSS_SELECTOR,".body-content .row").text)
# driver.back()
#//*[@id="content"]/section[1]/div/div/div[2]/ul/li[2]/a

link_list = []
for article in newslist:
    # print(article.text)
    link_list.append(article.get_attribute('href'))

for link in link_list:
    driver.get(link)
    # article.find_element(By.CSS_SELECTOR,".news-item .news-item__title").click()
    # print(driver.find_element(By.CSS_SELECTOR,".posted-on").text)
    # print(driver.find_element(By.CSS_SELECTOR,".desktop__logo").text)
    # print(driver.find_element(By.CSS_SELECTOR,".page-title").text)
    # print(driver.find_element(By.CSS_SELECTOR,".body-content .row").text)
    newstime = driver.find_element(By.CSS_SELECTOR, ".posted-on").text
    print(type(newstime))
    print(newstime)
    datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
    source = driver.find_element(By.CSS_SELECTOR, ".desktop__logo").text
    print(type(source))
    print(source)
    title = driver.find_element(By.CSS_SELECTOR, ".page-title").text
    print(type(title))
    print(title)
    title = title.replace("'", "''")
    text = driver.find_element(By.CSS_SELECTOR, ".body-content .row").text
    print(type(text))
    print(text)
    text = text.replace("'", "''")
    result = a.saveData(id, source, newstime, title, text,datetime)
    if result:
        id = id + 1
    else:
        print("id不增加")
    # time.sleep(3)source
# for article in newslist:
# time.sleep(3)

for i in range(9):
    driver.get("https://www.whitehouse.gov/briefing-room/page/%d/"%(i+2))
    time.sleep(3)
    newslist = driver.find_elements(By.XPATH, '//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article/h2/a')
    link_list = []
    for article in newslist:
        # print(article.text)
        link_list.append(article.get_attribute('href'))
    for link in link_list:
        driver.get(link)
        # article.find_element(By.CSS_SELECTOR,".news-item .news-item__title").click()
        # print(driver.find_element(By.CSS_SELECTOR,".posted-on").text)
        # print(driver.find_element(By.CSS_SELECTOR,".desktop__logo").text)
        # print(driver.find_element(By.CSS_SELECTOR,".page-title").text)
        # print(driver.find_element(By.CSS_SELECTOR,".body-content .row").text)
        newstime = driver.find_element(By.CSS_SELECTOR, ".posted-on").text
        print(type(newstime))
        print(newstime)
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        source = driver.find_element(By.CSS_SELECTOR, ".desktop__logo").text
        print(type(source))
        print(source)
        title = driver.find_element(By.CSS_SELECTOR, ".page-title").text
        print(type(title))
        print(title)
        title = title.replace("'", "''")
        text = driver.find_element(By.CSS_SELECTOR, ".body-content .row").text
        print(type(text))
        print(text)
        text = text.replace("'", "''")
        result = a.saveData(id, source, newstime, title, text,datetime)
        if result:
            id = id + 1
        else:
            print("id不增加")



driver.get("https://www.defense.gov/News/News-Stories/")
driver.maximize_window()
link_list = []
# //*[@id="alist"]/div[2]/div/div[1]/div[1]/figure/div/div/figcaption/h3/a
# //*[@id="alist"]/div[2]/div/div[1]/div[2]/figure/div/div/figcaption/h3/a
for i in range(10):
    path = '//*[@id="alist"]/div[2]/div/div[1]/div[%d]/figure/div/a'%(i+1)
    newslist = driver.find_elements(By.XPATH,path)
    for article in newslist:
    # print(article.text)
        link_list.append(article.get_attribute('href'))

for link in link_list:
    driver.get(link)

    newstime = (driver.find_element(By.CSS_SELECTOR, ".date").text).split('|')[0].strip().upper()
    print(type(newstime))
    print(newstime.split('|')[0].strip())
    match = re.match(r"(\w+)\s(\d{1,2}),\s(\d{4})", newstime)
    if match:
        month, day, year = match.groups()
        # 将day格式化为两位数
        formatted_day = f"{int(day):02d}"
        # 返回格式化后的日期字符串
        newstime =  f"{month} {formatted_day}, {year}"
    else:
        newstime = newstime
    datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
    source = 'U.S. Department of Defense'
    print(type(source))
    print(source)
    title = driver.find_element(By.CSS_SELECTOR, ".maintitle").text
    print(type(title))
    print(title)
    title = title.replace("'", "''")
    text = driver.find_element(By.CSS_SELECTOR, ".body").text
    print(type(text))
    print(text)
    text = text.replace("'", "''")
    result = a.saveData(id, source, newstime, title, text,datetime)
    if result:
        id = id + 1
    else:
        print("id不增加")


for i in range(5):
    #  https://www.defense.gov/News/News-Stories/?Page=2
    # driver.get("https://www.whitehouse.gov/briefing-room/page/%d/"%(i+2))
    driver.get("https://www.defense.gov/News/News-Stories/?Page=%d"%(i+2))
    time.sleep(3)
    link_list = []
    for i in range(10):
        path = '//*[@id="alist"]/div[2]/div/div[1]/div[%d]/figure/div/a' % (i + 1)
        newslist = driver.find_elements(By.XPATH, path)
        for article in newslist:
            # print(article.text)
            link_list.append(article.get_attribute('href'))
    for link in link_list:
        driver.get(link)
        newstime = (driver.find_element(By.CSS_SELECTOR, ".date").text).split('|')[0].strip().upper()
        print(type(newstime))
        print(newstime.split('|')[0].strip())
        match = re.match(r"(\w+)\s(\d{1,2}),\s(\d{4})", newstime)
        if match:
            month, day, year = match.groups()
            # 将day格式化为两位数
            formatted_day = f"{int(day):02d}"
            # 返回格式化后的日期字符串
            newstime = f"{month} {formatted_day}, {year}"
        else:
            newstime = newstime
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        source = 'U.S. Department of Defense'
        print(type(source))
        print(source)
        title = driver.find_element(By.CSS_SELECTOR, ".maintitle").text
        print(type(title))
        print(title)
        title = title.replace("'", "''")
        text = driver.find_element(By.CSS_SELECTOR, ".body").text
        print(type(text))
        print(text)
        text = text.replace("'", "''")
        result = a.saveData(id, source, newstime, title, text,datetime)
        if result:
            id = id + 1
        else:
            print("id不增加")

driver.get("https://www.nato.int/cps/en/natohq/news.htm")
driver.maximize_window()
newslist = driver.find_elements(By.XPATH,'/html/body/div[1]/div/article/div/div/div/table/tbody/tr/td[3]/p/a')
link_list = []
for article in newslist:
    link_list.append(article.get_attribute('href'))
for link in link_list:
    driver.get(link)
    newstime = driver.find_element(By.XPATH, '/html/body/div[1]/div/article/div/div[1]/div/ul[1]/li[1]').text
    print(type(newstime))
    print(newstime)
    newstime = newstime.strip(' -')
    # 检测是否包含两个日期
    if '-' in newstime:
        # 分割字符串并取最后一个日期部分
        newstime = newstime.split('-')[-1].strip()
    date = datetime.strptime(newstime, '%d %b. %Y')
    newstime = date.strftime('%B %d, %Y').upper()
    datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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
    result = a.saveData(id, source, newstime, title, text,datetime)
    if result:
        id = id + 1
    else:
        print("id不增加")
for i in range(5):
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
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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
        result = a.saveData(id, source, newstime, title, text,datetime)
        if result:
            id = id + 1
        else:
            print("id不增加")


driver.quit()

# input()
