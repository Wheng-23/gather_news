import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config.mysqlop import Mysqlop
#
id = 260
a = Mysqlop()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.defense.gouv.fr/actualites")#0
# https://www.defense.gouv.fr/actualites?page=1
driver.maximize_window()
# //*[@id="js-results"]/div/ul/li[1]/div/a
# //*[@id="js-results"]/div/ul/li[2]/div/a
# //*[@id="block-open-theme-contenudelapageprincipale"]/article/section/div/div/div[1]/article/div[1]/div/h3/a
# //*[@id="block-open-theme-contenudelapageprincipale"]/article/section/div/div/div[2]/article/div[1]/div/h3/a
# //*[@id="block-open-theme-contenudelapageprincipale"]/article/section/div/div/div[3]/article/div[1]/div/h3/a
# //*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div[1]/article/div[1]/div/h3/a
newslist1 = driver.find_elements(By.XPATH,'//*[@id="block-open-theme-contenudelapageprincipale"]/article/section/div/div/div/article/div[1]/div/h3/a')
link_list1 = []
for article in newslist1:
    link_list1.append(article.get_attribute('href'))
print(link_list1)

newslist2 = driver.find_elements(By.XPATH,
                                     '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div/article/div[1]/div/h3/a')
link_list2 = []
for article in newslist2:
    link_list2.append(article.get_attribute('href'))
print(link_list2)
# 法语月份映射
FRENCH_MONTHS = {
    'janvier': 'January',
    'février': 'February',
    'mars': 'March',
    'avril': 'April',
    'mai': 'May',
    'juin': 'June',
    'juillet': 'July',
    'août': 'August',
    'septembre': 'September',
    'octobre': 'October',
    'novembre': 'November',
    'décembre': 'December'
}
def convert_date(date_str):
    # 使用正则表达式提取日期部分
    pattern = r"le : (\d{2} \w+ \d{4})"
    match = re.search(pattern, date_str)
    if match:
        date_part = match.group(1)
    else:
        raise ValueError("Date not found in the input string.")

    # 替换法语月份为英语月份
    for french_month, english_month in FRENCH_MONTHS.items():
        date_part = date_part.replace(french_month, english_month)

    # 解析日期部分为 datetime 对象
    date_obj = datetime.strptime(date_part, "%d %B %Y")

    # 格式化日期为指定格式
    formatted_date = date_obj.strftime("%B %d, %Y").upper()

    return formatted_date

for link in link_list1:
    driver.get(link)
    try:
        # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]
        newstime = driver.find_element(By.XPATH, '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]').text
        print(type(newstime))
        print(newstime)
        newstime = convert_date(newstime)
        print(newstime)
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

        source = 'French Ministry of Defence'
        print(type(source))
        print(source)

        title = driver.find_element(By.XPATH, '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/h1').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        text = driver.find_element(By.XPATH, '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[2]/div').text
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

for link in link_list2:
    driver.get(link)
    try:
        # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]
        newstime = driver.find_element(By.XPATH,
                                       '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]').text
        print(type(newstime))
        print(newstime)
        newstime = convert_date(newstime)
        print(newstime)
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

        source = 'French Ministry of Defence'
        print(type(source))
        print(source)

        title = driver.find_element(By.XPATH,
                                    '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/h1').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        text = driver.find_element(By.XPATH,
                                   '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[2]/div').text
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

#
for i in range(3):
    driver.get("https://www.defense.gouv.fr/actualites?page=%d"%(i+1))
    time.sleep(3)
    # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div[1]/article/div[1]/div/h3/a
    # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div[2]/article/div[1]/div/h3/a

    newslist2 = driver.find_elements(By.XPATH,
                                     '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div[2]/div/div/article/div[1]/div/h3/a')
    link_list2 = []
    for article in newslist2:
        link_list2.append(article.get_attribute('href'))

    for link in link_list2:
        driver.get(link)
        try:
            # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]
            newstime = driver.find_element(By.XPATH,
                                           '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]').text
            print(type(newstime))
            print(newstime)
            newstime = convert_date(newstime)
            print(newstime)
            datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

            source = 'French Ministry of Defence'
            print(type(source))
            print(source)

            title = driver.find_element(By.XPATH,
                                        '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/h1').text
            print(type(title))
            print(title)
            title = title.replace("'", "''")

            text = driver.find_element(By.XPATH,
                                       '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[2]/div').text
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