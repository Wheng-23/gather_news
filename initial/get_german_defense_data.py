from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config.mysqlop import Mysqlop
#
id = 452
a = Mysqlop()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.bmvg.de/de/presse/alle-pressetermine-pressemitteilungen-bmvg")#
driver.maximize_window()

time.sleep(3)
driver.find_element(By.CSS_SELECTOR,".result-list__more-btn").click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR,".result-list__more-btn").click()
time.sleep(3)
newslist = driver.find_elements(By.XPATH,'//*[@id="r-main"]/section[3]/div[2]/div[2]/div/div/ol/li/article/a')
link_list = []
for article in newslist:
    link_list.append(article.get_attribute('href'))
print(link_list)

for link in link_list:
    driver.get(link)
    try:
        newstime = driver.find_element(By.XPATH, '//*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/span[2]/span/span[2]').text
        print(type(newstime))
        print(newstime)
        # 转换为日期对象
        date_obj = datetime.strptime(newstime, "%d.%m.%Y")
        # 转换为所需格式
        newstime = date_obj.strftime("%B %d, %Y").upper()
        print(newstime)
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        print(datetime)

        source = 'German Federal Ministry of Defence'
        print(type(source))
        print(source)

        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1/text()
        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div[2]/div[1]/article/div[2]/h3/a
        # //*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1
        title = driver.find_element(By.XPATH, '//*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/h1').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        text = driver.find_element(By.XPATH, '//*[@id="r-main"]/section[3]/div/div/div/div/div').text
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


# for i in range(3):
#     driver.get("https://www.defense.gouv.fr/actualites?page=%d"%(i+1))
#     time.sleep(3)
#     # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div[1]/article/div[1]/div/h3/a
#     # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div[2]/article/div[1]/div/h3/a
#
#     newslist2 = driver.find_elements(By.XPATH,
#                                      '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div/article/div[1]/div/h3/a')
#     link_list2 = []
#     for article in newslist2:
#         link_list2.append(article.get_attribute('href'))
#
#     for link in link_list2:
#         driver.get(link)
#         try:
#             # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]
#             newstime = driver.find_element(By.XPATH,
#                                            '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]').text
#             print(type(newstime))
#             print(newstime)
#             newstime = convert_date(newstime)
#             print(newstime)
#             datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
#
#             source = 'French Ministry of Defence'
#             print(type(source))
#             print(source)
#
#             title = driver.find_element(By.XPATH,
#                                         '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/h1').text
#             print(type(title))
#             print(title)
#             title = title.replace("'", "''")
#
#             text = driver.find_element(By.XPATH,
#                                        '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[2]/div').text
#             print(type(text))
#             print(text)
#             text = text.replace("'", "''")
#
#             result = a.saveData(id, source, newstime, title, text,datetime)
#             if result:
#                 id = id + 1
#             else:
#                 print("id不增加")
#         except Exception as e:
#             print(f"An error occurred while processing the link {link}: {e}")

driver.quit()
# input()