import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime as dt

from update.baidu_title_chinese_update import update_title_ch_baidu
from config.lite_update_summary import update_summary
from config.mysqlop import Mysqlop
from config.lite_text_chinese_update import update_text_ch
from update.predict import predict_heat
from update.update_tend import update_tend
from update.update_heats_toutiao import update_heats_toutiao


#
# 自定义异常类
class StopCrawlingException(Exception):
    """Exception raised to stop the crawling process."""
    pass
# 设置日期格式和比较逻辑
def parse_date(date_str):
    return dt.strptime(date_str, '%B %d, %Y').date()  # 假设日期格式为"June 27, 2024"
def update_data(id,days_ago):
    # a.clearData()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)#最多等三十秒
    driver.get("https://www.whitehouse.gov/")
    driver.maximize_window()
    driver.find_element(By.LINK_TEXT,"Briefing Room").click()
    time.sleep(3)
    try:
        newslist = driver.find_elements(By.XPATH,'//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article/h2/a')

        link_list = []
        for article in newslist:
            link_list.append(article.get_attribute('href'))

        for link in link_list:
            driver.get(link)
            newstime = driver.find_element(By.CSS_SELECTOR, ".posted-on").text
            print(type(newstime))
            print(newstime)
            newstime_new = parse_date(newstime)
            if newstime_new <= days_ago:
                raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
            datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

            update_title_ch_baidu(id)
            update_text_ch(id)
            update_summary(id)
            update_tend(id)
            # update_emo(id)
            time.sleep(3)
            # update_heats(id)
            update_heats_toutiao(id)
            predict_heat(id)

            if result:
                id = id + 1
            else:
                print("id不增加")

        for i in range(49):
            driver.get("https://www.whitehouse.gov/briefing-room/page/%d/"%(i+2))
            time.sleep(3)
            newslist = driver.find_elements(By.XPATH, '//*[@id="content"]/section[1]/div/div/div[1]/div[2]/article/h2/a')
            link_list = []
            for article in newslist:
                # print(article.text)
                link_list.append(article.get_attribute('href'))
            for link in link_list:
                driver.get(link)
                newstime = driver.find_element(By.CSS_SELECTOR, ".posted-on").text
                print(type(newstime))
                print(newstime)
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()

def convert_month_abbreviation(month):
    month_abbr = {
        'JAN': 'JANUARY', 'FEB': 'FEBRURAY', 'MAR': 'MARCH', 'APR': 'APRIL',
        'MAY': 'MAY', 'JUN': 'JUNE', 'JUL': 'JULY', 'AUG': 'AUGUST',
        'SEPT': 'SEPTEMBER', 'OCT': 'OCTOBER', 'NOV': 'NOVEMBER', 'DEC': 'DECEMBER'
    }
    return month_abbr.get(month.upper(), month)

def update_defense_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.defense.gov/News/News-Stories/")
    driver.maximize_window()
    try:
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
            match = re.match(r"(\w+\.?)\s(\d{1,2}),\s(\d{4})", newstime)
            if match:
                month, day, year = match.groups()
                month = month.replace('.', '')  # Remove period if present
                month = convert_month_abbreviation(month)
                # 将day格式化为两位数
                formatted_day = f"{int(day):02d}"
                # 返回格式化后的日期字符串
                newstime = f"{month} {formatted_day}, {year}"
            else:
                newstime = newstime
            print(newstime)
            newstime_new = parse_date(newstime)
            if newstime_new <= days_ago:
                raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
            datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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
            result = a.saveData(id,source, newstime, title, text,datetime)

            update_title_ch_baidu(id)
            update_text_ch(id)
            update_summary(id)
            update_tend(id)
            # update_emo(id)
            time.sleep(3)
            # update_heats(id)
            update_heats_toutiao(id)
            predict_heat(id)

            if result:
                id = id + 1
            else:
                print("id不增加")

        for i in range(49):
            #  https://www.defense.gov/News/News-Stories/?Page=2
            # driver.get("https://www.whitehouse.gov/briefing-room/page/%d/"%(i+2))
            driver.get("https://www.defense.gov/News/News-Stories/?Page=%d" % (i + 2))
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
                match = re.match(r"(\w+\.?)\s(\d{1,2}),\s(\d{4})", newstime)
                if match:
                    month, day, year = match.groups()
                    month = month.replace('.', '')  # Remove period if present
                    month = convert_month_abbreviation(month)
                    # 将day格式化为两位数
                    formatted_day = f"{int(day):02d}"
                    # 返回格式化后的日期字符串
                    newstime = f"{month} {formatted_day}, {year}"
                else:
                    newstime = newstime
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()


def update_north_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.nato.int/cps/en/natohq/news.htm")
    driver.maximize_window()
    try:
        newslist = driver.find_elements(By.XPATH, '/html/body/div[1]/div/article/div/div/div/table/tbody/tr/td[3]/p/a')
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
            date = dt.strptime(newstime, '%d %b. %Y')
            newstime = date.strftime('%B %d, %Y').upper()
            newstime_new = parse_date(newstime)
            if newstime_new <= days_ago:
                raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
            datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

            update_title_ch_baidu(id)
            update_text_ch(id)
            update_summary(id)
            update_tend(id)
            # update_emo(id)
            time.sleep(3)
            # update_heats(id)
            update_heats_toutiao(id)
            predict_heat(id)

            if result:
                id = id + 1
            else:
                print("id不增加")
        for i in range(49):
            driver.get("https://www.nato.int/cps/en/natohq/news.htm?&chunk=%d" % (i + 2))
            time.sleep(3)
            newslist = driver.find_elements(By.XPATH, '/html/body/div[1]/div/article/div/div/div/table/tbody/tr/td[3]/p/a')
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
                date = dt.strptime(newstime, '%d %b. %Y')
                newstime = date.strftime('%B %d, %Y').upper()
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()


def update_korea_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?handle=dema0003&siteId=mnd&id=mnd_020101000000")
    # https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?siteId=mnd&pageIndex=2&categoryCode=dema0003&id=mnd_020101000000
    driver.maximize_window()
    try:
        for i in range(1, 11):
            path = f'//*[@id="form_list"]/div/ul/li[{i}]/div[2]/div[1]/div/a | //*[@id="form_list"]/div/ul/li[{i}]/div/div[1]/div/a'
            article = driver.find_element(By.XPATH, path)
            js_function = article.get_attribute('href')
            # 从 'javascript:jf_view('dema0003','39476');' 中提取函数和参数
            function_name = js_function.split(':')[1].split('(')[0]
            params = js_function.split('(')[1].split(')')[0].split(',')
            params = [param.strip().strip("'") for param in params]

            # 构建 JavaScript 执行语句
            js_code = f"{function_name}('{params[0]}', '{params[1]}');"
            # 执行 JavaScript 代码
            driver.execute_script(js_code)

            # 等待并获取标题'//*[@id="content"]/section/div/div/div[1]/div[1]'
            title = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[1]').text
            print(type(title))
            print(title)
            title = title.replace("'", "''")
            source = 'Ministry of National Defense of South Korea'
            print(type(source))
            print(source)
            text = driver.find_element(By.CSS_SELECTOR, '.post_content').text
            print(type(text))
            print(text)
            text = text.replace("'", "''")
            newstime = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]/dd').text
            print(type(newstime))
            print(newstime)
            # 将字符串转换为日期对象
            date_obj = dt.strptime(newstime, '%Y.%m.%d')

            # 将日期对象格式化为所需的字符串格式
            newstime = date_obj.strftime('%B %d, %Y').upper()
            newstime_new = parse_date(newstime)
            if newstime_new <= days_ago:
                raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
            datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
            result = a.saveData(id, source, newstime, title, text,datetime)

            update_title_ch_baidu(id)
            update_text_ch(id)
            update_summary(id)
            update_tend(id)
            # update_emo(id)
            time.sleep(3)
            # update_heats(id)
            update_heats_toutiao(id)
            predict_heat(id)

            if result:
                id = id + 1
            else:
                print("id不增加")

            driver.back()
        for i in range(5):
            driver.get(
                "https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?siteId=mnd&pageIndex=%d&categoryCode=dema0003&id=mnd_020101000000" % (
                            i + 2))
            # https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?siteId=mnd&pageIndex=2&categoryCode=dema0003&id=mnd_020101000000
            driver.maximize_window()
            for i in range(1, 11):
                path = f'//*[@id="form_list"]/div/ul/li[{i}]/div[2]/div[1]/div/a | //*[@id="form_list"]/div/ul/li[{i}]/div/div[1]/div/a'
                article = driver.find_element(By.XPATH, path)
                js_function = article.get_attribute('href')
                # 从 'javascript:jf_view('dema0003','39476');' 中提取函数和参数
                function_name = js_function.split(':')[1].split('(')[0]
                params = js_function.split('(')[1].split(')')[0].split(',')
                params = [param.strip().strip("'") for param in params]

                # 构建 JavaScript 执行语句
                js_code = f"{function_name}('{params[0]}', '{params[1]}');"
                # 执行 JavaScript 代码
                driver.execute_script(js_code)

                # 等待并获取标题'//*[@id="content"]/section/div/div/div[1]/div[1]'
                title = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[1]').text
                print(type(title))
                print(title)
                title = title.replace("'", "''")
                source = 'Ministry of National Defense of South Korea'
                print(type(source))
                print(source)
                text = driver.find_element(By.CSS_SELECTOR, '.post_content').text
                print(type(text))
                print(text)
                text = text.replace("'", "''")
                newstime = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]/dd').text
                print(type(newstime))
                print(newstime)
                # 将字符串转换为日期对象
                date_obj = dt.strptime(newstime, '%Y.%m.%d')

                # 将日期对象格式化为所需的字符串格式
                newstime = date_obj.strftime('%B %d, %Y').upper()
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
                result = a.saveData(id, source, newstime, title, text,datetime)

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
                driver.back()
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()


def update_britain_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.gov.uk/search/news-and-communications?")
    # https://www.gov.uk/search/news-and-communications?page=1
    driver.maximize_window()
    try:
        newslist = driver.find_elements(By.XPATH, '//*[@id="js-results"]/div/ul/li/div/a')
        link_list = []
        for article in newslist:
            link_list.append(article.get_attribute('href'))
        for link in link_list:
            driver.get(link)
            try:
                newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/dl/dd[2]').text
                print(type(newstime))
                print(newstime)
                # 将字符串解析为日期对象
                date_obj = dt.strptime(newstime, "%d %B %Y")
                # 格式化日期对象为指定格式的字符串
                newstime = date_obj.strftime("%B %d, %Y").upper()
                # 输出结果
                print(newstime)
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
            except StopCrawlingException as sce:
                print(f"An error occurred while processing the link {link}: {sce}")
                raise  # 重新引发异常以退出主循环
            except Exception as e:
                print(f"An error occurred while processing the link {link}: {e}")
        for i in range(49):
            driver.get("https://www.gov.uk/search/news-and-communications?page=%d" % (i + 2))
            time.sleep(3)
            newslist = driver.find_elements(By.XPATH, '//*[@id="js-results"]/div/ul/li/div/a')
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
                    date_obj = dt.strptime(newstime, "%d %B %Y")
                    # 格式化日期对象为指定格式的字符串
                    newstime = date_obj.strftime("%B %d, %Y").upper()
                    # 输出结果
                    print(newstime)
                    newstime_new = parse_date(newstime)
                    if newstime_new <= days_ago:
                        raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                    datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
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

                    update_title_ch_baidu(id)
                    update_text_ch(id)
                    update_summary(id)
                    update_tend(id)
                    # update_emo(id)
                    time.sleep(3)
                    # update_heats(id)
                    update_heats_toutiao(id)
                    predict_heat(id)

                    if result:
                        id = id + 1
                    else:
                        print("id不增加")
                except StopCrawlingException as sce:
                    print(f"An error occurred while processing the link {link}: {sce}")
                    raise  # 重新引发异常以退出主循环
                except Exception as e:
                    print(f"An error occurred while processing the link {link}: {e}")
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()

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

def convert_date_france(date_str):
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
    date_obj = dt.strptime(date_part, "%d %B %Y")

    # 格式化日期为指定格式
    formatted_date = date_obj.strftime("%B %d, %Y").upper()

    return formatted_date

def update_france_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.defense.gouv.fr/actualites")  # 0
    # https://www.defense.gouv.fr/actualites?page=1
    driver.maximize_window()
    try:
        newslist1 = driver.find_elements(By.XPATH,
                                         '//*[@id="block-open-theme-contenudelapageprincipale"]/article/section/div/div/div/article/div[1]/div/h3/a')
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
        for link in link_list1:
            driver.get(link)
            try:
                # //*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]
                newstime = driver.find_element(By.XPATH,
                                               '//*[@id="block-open-theme-contenudelapageprincipale"]/article/div/div[1]/div[1]/div[1]').text
                print(type(newstime))
                print(newstime)
                newstime = convert_date_france(newstime)
                print(newstime)
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
            except StopCrawlingException as sce:
                print(f"An error occurred while processing the link {link}: {sce}")
                raise  # 重新引发异常以退出主循环
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
                newstime = convert_date_france(newstime)
                print(newstime)
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

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

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
            except StopCrawlingException as sce:
                print(f"An error occurred while processing the link {link}: {sce}")
                raise  # 重新引发异常以退出主循环
            except Exception as e:
                print(f"An error occurred while processing the link {link}: {e}")
        for i in range(3):
            driver.get("https://www.defense.gouv.fr/actualites?page=%d" % (i + 1))
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
                    newstime = convert_date_france(newstime)
                    print(newstime)
                    newstime_new = parse_date(newstime)
                    if newstime_new <= days_ago:
                        raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                    datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

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

                    update_title_ch_baidu(id)
                    update_text_ch(id)
                    update_summary(id)
                    update_tend(id)
                    # update_emo(id)
                    time.sleep(3)
                    # update_heats(id)
                    update_heats_toutiao(id)
                    predict_heat(id)

                    if result:
                        id = id + 1
                    else:
                        print("id不增加")
                except StopCrawlingException as sce:
                    print(f"An error occurred while processing the link {link}: {sce}")
                    raise  # 重新引发异常以退出主循环
                except Exception as e:
                    print(f"An error occurred while processing the link {link}: {e}")
    except StopCrawlingException as e:
        print(str(e))
    finally:
        driver.quit()

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

def update_italy_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.difesa.it/primopiano/elenco/index.html#")
    driver.maximize_window()
    driver.find_element(By.XPATH, '/html/body/div[10]/div[3]/button[3]').click()
    try:
        for i in range(5):
            newslist = driver.find_elements(By.XPATH, '//*[@id="divelencocontent"]/div/div/div/div/div[2]/div/div/a')
            link_list = []
            for article in newslist:
                link_list.append(article.get_attribute('href'))
            print(link_list)

            for link in link_list:
                driver.get(link)
                try:
                    # newstime = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[1]/div[2]/div[1]').text
                    newstime = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div[2]/div[1]').text
                    print(type(newstime))
                    print(newstime)
                    newstime = convert_date_italy(newstime)
                    print(newstime)
                    newstime_new = parse_date(newstime)
                    if newstime_new <= days_ago:
                        raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
                    datetime = dt.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象

                    source = 'Italian Ministry of Defence'
                    print(type(source))
                    print(source)

                    # //*[@id="content"]/div[3]/div[1]/h3
                    # //*[@id="main"]/div/div[1]/h3
                    title = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/h3').text
                    print(type(title))
                    print(title)
                    title = title.replace("'", "''")

                    content = []
                    # //*[@id="main"]/div/div[1]/p[3]/em/text()
                    text = driver.find_elements(By.XPATH, '//*[@id="main"]/div/div[1]/p[3]')
                    for para in text:
                        content.append(para.text)
                    print(content)
                    content_str = '\n'.join(content)
                    content_str = content_str.replace("'", "''")
                    print(content_str)

                    result = a.saveData(id, source, newstime, title, content_str, datetime)

                    update_title_ch_baidu(id)
                    update_text_ch(id)
                    update_summary(id)
                    update_tend(id)
                    # update_emo(id)
                    time.sleep(3)
                    # update_heats(id)
                    update_heats_toutiao(id)
                    predict_heat(id)

                    if result:
                        id = id + 1
                    else:
                        print("id不增加")
                    driver.back()
                    time.sleep(3)
                except StopCrawlingException as e:
                    print(str(e))
                    return  # 退出整个函数
                except Exception as e:
                    print(f"An error occurred while processing the link {link}: {e}")
            element = driver.find_element(By.ID, "btnNext")
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            time.sleep(3)
    finally:
        driver.quit()


def update_german_data(days_ago):
    a = Mysqlop()
    id = a.get_row_count() + 1
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort不存在问题
    chrome_options.add_argument('--disable-dev-shm-usage')  # 共享内存不足的问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--remote-debugging-port=9222')  # 使用远程调试端口
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小（防止元素不可见）
    chrome_options.add_argument('--disable-setuid-sandbox')  # 禁用setuid沙箱

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)  # 最多等三十秒
    driver.get("https://www.bmvg.de/de/presse/alle-pressetermine-pressemitteilungen-bmvg")  #
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/button[3]').click()
    driver.maximize_window()

    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".result-list__more-btn").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".result-list__more-btn").click()
    time.sleep(3)
    try:
        newslist = driver.find_elements(By.XPATH, '//*[@id="r-main"]/section[3]/div[2]/div[2]/div/div/ol/li/article/a')
        link_list = []
        for article in newslist:
            link_list.append(article.get_attribute('href'))
        print(link_list)
        for link in link_list:
            driver.get(link)
            try:
                newstime = driver.find_element(By.XPATH,
                                               '//*[@id="r-main"]/section[2]/div/div/div/div/div/div/div/span[2]/span/span[2]').text
                print(type(newstime))
                print(newstime)
                # 转换为日期对象
                date_obj = dt.strptime(newstime, "%d.%m.%Y")
                # 转换为所需格式
                newstime = date_obj.strftime("%B %d, %Y").upper()
                print(newstime)
                newstime_new = parse_date(newstime)
                if newstime_new <= days_ago:
                    raise StopCrawlingException("Newstime is older than or equal to two days ago. Exiting program.")
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

                result = a.saveData(id, source, newstime, title, text, datetime)

                update_title_ch_baidu(id)
                update_text_ch(id)
                update_summary(id)
                update_tend(id)
                # update_emo(id)
                time.sleep(3)
                # update_heats(id)
                update_heats_toutiao(id)
                predict_heat(id)

                if result:
                    id = id + 1
                else:
                    print("id不增加")
            except StopCrawlingException as e:
                print(str(e))
                return  # 退出整个函数
            except Exception as e:
                print(f"An error occurred while processing the link {link}: {e}")
    finally:
        driver.quit()

def update():
    global a
    a = Mysqlop()
    id = a.get_row_count() + 1
    latest_time_str_white = a.select_latest_time_by_source('THE WHITE HOUSE')
    print(latest_time_str_white)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_white = dt.strptime(latest_time_str_white, "%B %d, %Y")
    print(latest_time_white.date())
    days_ago_white = latest_time_white.date()

    latest_time_str_us_defense = a.select_latest_time_by_source('U.S. Department of Defense')
    print(latest_time_str_us_defense)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_us_defense = dt.strptime(latest_time_str_us_defense, "%B %d, %Y")
    print(latest_time_us_defense.date())
    days_ago_us_defense = latest_time_us_defense.date()

    latest_time_str_korea = a.select_latest_time_by_source('Ministry of National Defense of South Korea')
    print(latest_time_str_korea)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_korea = dt.strptime(latest_time_str_korea, "%B %d, %Y")
    print(latest_time_korea.date())
    days_ago_korea = latest_time_korea.date()

    latest_time_str_british = a.select_latest_time_by_source('British Ministry of Defence')
    print(latest_time_str_british)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_british = dt.strptime(latest_time_str_british, "%B %d, %Y")
    print(latest_time_british.date())
    days_ago_british = latest_time_british.date()

    latest_time_str_french = a.select_latest_time_by_source('French Ministry of Defence')
    print(latest_time_str_french)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_french = dt.strptime(latest_time_str_french, "%B %d, %Y")
    print(latest_time_french.date())
    days_ago_french = latest_time_french.date()

    latest_time_str_NATO = a.select_latest_time_by_source('North Atlantic Treaty Organization')
    print(latest_time_str_NATO)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_NATO = dt.strptime(latest_time_str_NATO, "%B %d, %Y")
    print(latest_time_NATO.date())
    days_ago_NATO = latest_time_NATO.date()

    latest_time_str_italy = a.select_latest_time_by_source('Italian Ministry of Defence')
    print(latest_time_str_italy)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_italy = dt.strptime(latest_time_str_italy, "%B %d, %Y")
    print(latest_time_italy.date())
    days_ago_italy = latest_time_italy.date()

    latest_time_str_german = a.select_latest_time_by_source('German Federal Ministry of Defence')
    print(latest_time_str_german)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_str_german = dt.strptime(latest_time_str_german, "%B %d, %Y")
    print(latest_time_str_german.date())
    days_ago_german = latest_time_str_german.date()

    update_data(id,days_ago_white)
    update_defense_data(days_ago_us_defense)
    update_north_data(days_ago_NATO)
    update_korea_data(days_ago_korea)
    update_britain_data(days_ago_british)
    update_france_data(days_ago_french)
    update_italy_data(days_ago_italy)
    update_german_data(days_ago_german)
    # update_title_ch_baidu(id)
    # update_text_ch(id)
    # update_summary(id)
    # update_tend(id)
    # # update_emo(id)
    # time.sleep(3)
    # # update_heats(id)
    # update_heats_toutiao(id)
    # predict_heat(id)



if __name__ == '__main__':
    update()

