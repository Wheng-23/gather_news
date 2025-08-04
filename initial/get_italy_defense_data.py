from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from config.mysqlop import Mysqlop
#
id = 412
a = Mysqlop()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.difesa.it/primopiano/elenco/index.html#")
driver.maximize_window()



def convert_date(date_str):
    # 提取日期部分
    try:
        # 假设日期部分总是从第三个单词开始
        date_part = date_str.split()[-3:]
        date_part_str = ' '.join(date_part)
    except IndexError:
        print(f"Error processing date: {date_str}")
        return None

    # 定义月份的意大利语到英语的映射
    month_mapping = {
        'gen': 'JANUARY', 'feb': 'FEBRUARY', 'mar': 'MARCH', 'apr': 'APRIL',
        'mag': 'MAY', 'giu': 'JUNE', 'lug': 'JULY', 'ago': 'AUGUST',
        'set': 'SEPTEMBER', 'ott': 'OCTOBER', 'nov': 'NOVEMBER', 'dic': 'DECEMBER'
    }

    try:
        # 将月份部分从意大利语转换为英语
        date_parts = date_part_str.split()
        date_parts[1] = month_mapping[date_parts[1].lower()]

        # 重新组装日期字符串
        date_part_str = ' '.join(date_parts)

        # 将日期字符串转换为datetime对象
        date_obj = datetime.strptime(date_part_str, "%d %B %Y")

        # 格式化datetime对象为所需的字符串格式
        formatted_date = date_obj.strftime("%B %d, %Y").upper()

        return formatted_date
    except (KeyError, ValueError) as e:
        print(f"Error processing date: {date_str} - {e}")
        return None

for i in range(4):
    newslist = driver.find_elements(By.XPATH,'//*[@id="divelencocontent"]/div/div/div/div/div[2]/div/div/a')
    link_list = []
    for article in newslist:
        link_list.append(article.get_attribute('href'))
    print(link_list)

    for link in link_list:
        driver.get(link)
        try:
            newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div[2]/div[1]').text
            print(type(newstime))
            print(newstime)
            newstime = convert_date(newstime)
            print(newstime)
            datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

            source = 'Italian Ministry of Defence'
            print(type(source))
            print(source)

            # //*[@id="content"]/div[3]/div[1]/h3
            title = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/h3').text
            print(type(title))
            print(title)
            title = title.replace("'", "''")

            content = []
            text = driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/div[1]/p')
            for para in text:
                content.append(para.text)
            print(content)
            content_str = '\n'.join(content)
            content_str = content_str.replace("'", "''")
            print(content_str)

            result = a.saveData(id, source, newstime, title, content_str,datetime)
            if result:
                id = id + 1
            else:
                print("id不增加")
            driver.back()
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred while processing the link {link}: {e}")
    element = driver.find_element(By.ID, "btnNext")
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    time.sleep(6)



driver.quit()