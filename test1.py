from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime as dt
def convert_date_italy(date_str):
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
        date_obj = dt.strptime(date_part_str, "%d %B %Y")

        # 格式化datetime对象为所需的字符串格式
        formatted_date = date_obj.strftime("%B %d, %Y").upper()

        return formatted_date
    except (KeyError, ValueError) as e:
        print(f"Error processing date: {date_str} - {e}")
        return None

def parse_date(date_str):
    return dt.strptime(date_str, '%B %d, %Y').date()  # 假设日期格式为"June 27, 2024"

class StopCrawlingException(Exception):
    """Exception raised to stop the crawling process."""
    pass

def update_italy_data():
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.difesa.it/primopiano/elenco/index.html#")
    driver.maximize_window()
    #/html/body/div[10]/div[3]/button[3]
    driver.find_element(By.XPATH,'/html/body/div[10]/div[3]/button[3]').click()
    newslist = driver.find_elements(By.XPATH, '//*[@id="divelencocontent"]/div/div/div/div/div[2]/div/div/a')
    link_list = []
    for article in newslist:
        link_list.append(article.get_attribute('href'))
    print(link_list)

    for link in link_list:
        driver.get(link)
        # newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div[2]/div[1]').text
        newstime = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div[2]/div[1]').text
        print(type(newstime))
        print(newstime)
        newstime = convert_date_italy(newstime)
        print(newstime)
        datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        print(datetime)

        source = 'Italian Ministry of Defence'
        print(type(source))
        print(source)

        # //*[@id="content"]/div[3]/div[1]/h3
        # //*[@id="main"]/div/div[1]/h3
        # title = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/h3').text
        title = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/h3').text
        print(type(title))
        print(title)
        title = title.replace("'", "''")

        content = []
        # //*[@id="main"]/div/div[1]/p[3]/em/text()
        # //*[@id="main"]/div/div[1]/p[3]
        # //*[@id="main"]/div/div[1]/p[3]/em
        # text = driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/div[1]/p')
        text = driver.find_elements(By.XPATH, '//*[@id="main"]/div/div[1]/p[3]')
        for para in text:
            content.append(para.text)
        print(content)
        content_str = '\n'.join(content)
        content_str = content_str.replace("'", "''")
        print(content_str)
    driver.quit()

if __name__ == '__main__':
    update_italy_data()