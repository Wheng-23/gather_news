import urllib.parse

import spacy
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apidemo.TranslateDemo import createRequest
from config.mysqlop import Mysqlop
from selenium import webdriver
from selenium.webdriver.common.by import By

a = Mysqlop()
def extract_times_from_page():
    try:
        # 等待页面加载，并找到显示时间的元素
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//span[contains(text(),'天前') or contains(text(),'小时前') or contains(text(),'分钟前') or contains(text(),'前天') or contains(text(),'昨天')]"))
        )

        # 获取并打印所有符合条件的元素文本
        for element in elements:
            print(element.text)
            total_times.append(element.text)
    except Exception as e:
        print("Error:", e)
# for i in range(a.get_row_count()):
def count_time_ranges(arr):
    count = {
        "0天前": 0,
        "1天前": 0,
        "2天前": 0,
        "3天前": 0,
        "4天前": 0,
        "5天前": 0,
        "6天前": 0,
        "7天前": 0
    }

    for item in arr:
        if "小时前" in item:
            count["0天前"] += 1
        elif "昨天" in item:
            count["1天前"] += 1
        elif "前天" in item:
            count["2天前"] += 1
        elif "天前" in item:
            try:
                days_ago = int(item.split("天前")[0])
                if days_ago >= 0 and days_ago <= 7:
                    count[f"{days_ago}天前"] += 1
            except (ValueError, AttributeError):
                # Handle cases where the string does not start with a number
                print(f"Skipping invalid item: {item}")

    return count


for i in range(94,95):
    data_str = a.getData(i, 1, "title")
    # text = "Private investment firm Carlyle Group,which has a reputation for making well-timed and occasionally controversial plays in the defense industry, has quietly placed its bets on another part of the market."
    spacy_nlp = spacy.load("en_core_web_lg")
    # spacy_nlp = spacy.load()

    spacy_nlp.add_pipe("textrank")
    doc = spacy_nlp(data_str)

    total_times = []
    words = []
    # examine the top-ranked phrases in the document
    for phrase in doc._.phrases:
        # print(phrase.rank, phrase.count)
        # print(phrase.chunks[0])
        words.append(phrase.chunks[0])

    print(words[0])
    print(type(words[0]))
    translation = createRequest(words[0].text)
    query = urllib.parse.quote(translation)
    print(query)

# https://so.toutiao.com/search?dvpf=pc&keyword=%E7%AC%AC%E4%B8%80%E5%A4%AB%E4%BA%BA%E5%90%89%E5%B0%94%E6%8B%9C%E7%99%BB&filter_vendor=site&index_resource=site&filter_period=week&page_num=0
# https://so.toutiao.com/search?keyword=%E7%AC%AC%E4%B8%80%E5%A4%AB%E4%BA%BA%E5%90%89%E5%B0%94%E6%8B%9C%E7%99%BB&pd=information&source=aladdin&dvpf=pc&aid=4916&page_num=0
    # https://so.toutiao.com/search?dvpf=pc&keyword=%E7%AC%AC%E4%B8%80%E5%A4%AB%E4%BA%BA%E5%90%89%E5%B0%94%E6%8B%9C%E7%99%BB&filter_vendor=site&index_resource=site&filter_period=week&page_num=0
    website = "https://so.toutiao.com/search?dvpf=pc&keyword=%s&filter_vendor=site&index_resource=site&filter_period=week&page_num=0"%query
    print(website)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)#最多等三十秒
    driver.get(website)
    driver.maximize_window()
    # //*[@id="rso"]/div/div/div[1]/div/div/a/div/div[2]/div[4]
    # //*[@id="rso"]/div/div/div[2]/div/div/a/div/div[2]/div[4]
    no_times_count = 0
    extract_times_from_page()
    print(total_times)
    if not total_times:
        print(f"No times found on initial page for query {i}. Skipping current query.")
        result = count_time_ranges(total_times)
        print(result)
        for j in range(8):  # Assuming id values start from 1 and go up to the number of elements in arr
            column_name = f"{j}天前"
            count = result[column_name]
            a.updateHeat(column_name, count, i + 1)
        continue
    while True:
        # //*[@id="pnnext"]/span[2]
        try:
            # //*[@id="s-dom-02433780"]/div/div/a[12]
            # //*[@id="s-dom-2cfc9070"]/div/div/a[11]
            # //*[@id="s-dom-2cfc9070"]/div/div/a[11]/div
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='text-ellipsis' and text()='下一页']"))
            )
            next_button.click()
            # driver.implicitly_wait(30)
            extract_times_from_page()
            print(total_times)
        except NoSuchElementException:
            print("No more pages found.")
            break
        except Exception as e:
            print("Error during next page navigation:", e)
            break

    print(total_times)
    result = count_time_ranges(total_times)
    print(result)
    for j in range(8):  # Assuming id values start from 1 and go up to the number of elements in arr
        column_name = f"{j}天前"
        count = result[column_name]
        a.updateHeat(column_name, count, i+1)

    driver.quit()
# input()