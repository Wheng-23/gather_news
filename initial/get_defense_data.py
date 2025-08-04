from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from config.mysqlop import Mysqlop
#
a = Mysqlop()
a.clearData()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.defense.gov/")
driver.maximize_window()
driver.find_element(By.CSS_SELECTOR,".content-type-text").click()
# time.sleep(3)
# #//*[@id="content"]/section[1]/div/div/div[1]/div[2]
# #//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article[1]/h2/a
#  //*[@id="alist"]/div[2]/div/div[1]/div[1]/figure/div/a
#  //*[@id="alist"]/div[2]/div/div[1]/div[2]/figure/div/a
#  //*[@id="alist"]/div[2]/div/div[1]/div[3]/figure/div/a

#  //*[@id="content"]/section[1]/div/div/div[1]/div[2]/article[1]/h2/a
#  //*[@id="content"]/section[1]/div/div/div[1]/div[2]/article[2]/h2/a
link_list = []
for i in range(10):
    path = '//*[@id="alist"]/div[2]/div/div[1]/div[%d]/figure/div/a'%(i+1)
    newslist = driver.find_elements(By.XPATH,path)
    for article in newslist:
    # print(article.text)
        link_list.append(article.get_attribute('href'))
# # newslist.find_element(By.CSS_SELECTOR,".news-item__title").click()
# # print(driver.find_element(By.CSS_SELECTOR,".posted-on").text)
# # print(driver.find_element(By.CSS_SELECTOR,".desktop__logo").text)
# # print(driver.find_element(By.CSS_SELECTOR,".page-title").text)
# # print(driver.find_element(By.CSS_SELECTOR,".body-content .row").text)
# # driver.back()
# #//*[@id="content"]/section[1]/div/div/div[2]/ul/li[2]/a

for link in link_list:
    driver.get(link)

    newstime = (driver.find_element(By.CSS_SELECTOR, ".date").text).split('|')[0].strip()
    print(type(newstime))
    print(newstime.split('|')[0].strip())
    source = 'U.S. Department of Defense'
    print(type(source))
    print(source)
    title = driver.find_element(By.CSS_SELECTOR, ".maintitle").text
    print(type(title))
    print(title)
    text = driver.find_element(By.CSS_SELECTOR, ".body").text
    print(type(text))
    print(text)
    text = text.replace("'", "''")
    a.saveData(source,newstime,title,text)


for i in range(49):
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
        newstime = (driver.find_element(By.CSS_SELECTOR, ".date").text).split('|')[0].strip()
        print(type(newstime))
        print(newstime.split('|')[0].strip())
        source = 'U.S. Department of Defense'
        print(type(source))
        print(source)
        title = driver.find_element(By.CSS_SELECTOR, ".maintitle").text
        print(type(title))
        print(title)
        text = driver.find_element(By.CSS_SELECTOR, ".body").text
        print(type(text))
        print(text)
        text = text.replace("'", "''")
        a.saveData(source, newstime, title, text)
#
#
# print(link_list)
driver.quit()

# input()
