from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from config.mysqlop import Mysqlop
#
id = 201
a = Mysqlop()
driver = webdriver.Chrome()
driver.implicitly_wait(30)#最多等三十秒
driver.get("https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?handle=dema0003&siteId=mnd&id=mnd_020101000000")
# https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?siteId=mnd&pageIndex=2&categoryCode=dema0003&id=mnd_020101000000
driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR,".more-trapezoid-wh").click()
# 模拟鼠标点击确认按钮
# button = driver.find_element(By.XPATH,'//*[@id="blYgG5"]/div/label/span[1]')
# actions = ActionChains(driver)
# actions.move_to_element(button).click().perform()
# //*[@id="container"]/main/div[2]/div/article[1]/a
# //*[@id="container"]/main/div[2]/div/article[2]/a
# //*[@id="form_list"]/div/ul/li[1]
# //*[@id="form_list"]/div/ul/li[2]
# //*[@id="form_list"]/div/ul/li[10]
# //*[@id="form_list"]/div/ul/li[1]/div[2]/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[2]/div[2]/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[2]/div[2]/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[3]/div[2]/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[8]/div/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[9]/div/div[1]/div/a
# //*[@id="form_list"]/div/ul/li[10]/div[2]/div[1]/div/a
for i in range(1,11):
    # try:
    #     path = '//*[@id="form_list"]/div/ul/li[%d]/div[2]/div[1]/div/a'%i
    #     article = driver.find_element(By.XPATH,path)
    # except:
    #     path = '//*[@id="form_list"]/div/ul/li[%d]/div/div[1]/div/a' % i
    #     article = driver.find_element(By.XPATH, path)
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
    source = 'Ministry of National Defense of South Korea'
    print(type(source))
    print(source)
    # //*[@id="content"]/section/div/div/div[2]/p[3]/font
    # //*[@id="content"]/section/div/div/div[2]/p[3]/font/text()[1]
    # //*[@id="content"]/section/div/div/div[2]/p[3]/font/text()[2]
    text = driver.find_element(By.CSS_SELECTOR, '.post_content').text
    print(type(text))
    print(text)
    # //*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]/dd
    # //*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]
    newstime = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]/dd').text
    print(type(newstime))
    print(newstime)
    # 将字符串转换为日期对象
    date_obj = datetime.strptime(newstime, '%Y.%m.%d')

    # 将日期对象格式化为所需的字符串格式
    newstime = date_obj.strftime('%B %d, %Y').upper()
    datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
    result = a.saveData(id, source, newstime, title, text,datetime)
    if result:
        id = id + 1
    else:
        print("id不增加")

    driver.back()

for i in range(5):
    driver.get("https://www.mnd.go.kr/cop/kookbang/kookbangIlboList.do?siteId=mnd&pageIndex=%d&categoryCode=dema0003&id=mnd_020101000000"%(i+2))
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
        source = 'Ministry of National Defense of South Korea'
        print(type(source))
        print(source)
        text = driver.find_element(By.CSS_SELECTOR, '.post_content').text
        print(type(text))
        print(text)
        newstime = driver.find_element(By.XPATH, '//*[@id="content"]/section/div/div/div[1]/div[2]/dl[2]/dd').text
        print(type(newstime))
        print(newstime)
        # 将字符串转换为日期对象
        date_obj = datetime.strptime(newstime, '%Y.%m.%d')

        # 将日期对象格式化为所需的字符串格式
        newstime = date_obj.strftime('%B %d, %Y').upper()
        datetime = datetime.strptime(newstime, "%B %d, %Y")  # 将字符串转换为datetime对象
        result = a.saveData(id, source, newstime, title, text,datetime)
        if result:
            id = id + 1
        else:
            print("id不增加")
        driver.back()
# 关闭浏览器
driver.quit()
