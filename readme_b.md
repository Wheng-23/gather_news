# infoanalysis基于文本挖掘情报分析后端代码
#项目介绍：

本项目实现了对8家网站进行情报搜集和分析，并设计了友好的情报分析检索界面。实现了对情报的所属国家和等级的设定，实现了情报的热度走势展示，实现了检索的情报的情报来源分布展示以及情报地域展示。设计了总结文章摘要算法，并呈现在界面上。设计了翻译算法，实现对文章标题和原文的翻译，设计了情报意图分析算法，并呈现在界面上。设计了路径检索算法，根据选定情报，检索相关的新闻历史数据。

#项目的运行环境：python==3.11.5    fastapi==0.111.0   uvicorn==0.30.1  requests==2.31.0   typing_extensions==4.12.1  spacy==3.7.5   numpy==1.26.4   snownlp==0.12.3  PyMySQL==1.1.1

torch==2.3.1+cu121   jieba==0.42.1

配置步骤：

1.项目中包含requirements.txt,执行pip install requirements.txt

2.切换到pip_whl目录，运行pip install en_core_web_lg-3.7.1-py3-none-any.whl和

pip install zh_core_web_sm-3.7.0-py3-none-any.whl

#运行main.py文件启动后端程序，运行地址和端口为：http://127.0.0.1:8080

注意事项：

1.当点击更新数据库后，会进行网站的数据爬取，当开始爬取意大利国防部网站和德国联邦国防部网站时请点击接受Cookies，分别为Accetto tutto和Alle Cookies akzeptieren

2.爬虫技术采用的是selenium,当点击更新数据库时，会打开chrome谷歌浏览器进行数据爬取，所以需要下载chrome浏览器和chromedriver浏览器驱动。并且两者版本需要匹配，浏览器驱动可以在网上进行下载，当解压完浏览器驱动文件后，需要将chromedriver.exe文件复制到chrome安装目录下替换掉原来的文件，由于浏览器的版本会持续更新，当程序报错时不能爬取时，也许是版本不匹配的原因，需要更新驱动版本。

项目后端结构目录：

1.config文件夹下的peizhi文件需要用户进行配置，其中包括星火和百度api以及数据库连接信息
2.database文件夹是操作数据库的底层文件

#后端接口文档

#情报信息概览

#向后端传递时间、来源以及关键词，向前端传递筛选出的新闻信息。
请求地址：  /ZiXunXinXiGaiLan/data
方法： post
请求参数：定义DataInput数据结构，包括开始日期、结束日期、来源、关键词

{

'startDate': '2024-07-10', 

'endDate': '2024-07-11', 

'source': '北约',

 'text': '拜登'

}

返回参数：
((id, source, time,title, text, translate_text,summary,emotion,heats,translate_text, country, level, release_time), ...)

#向前端传递筛选好的新闻的来源统计数据
请求地址： /ZiXunXinXiGaiLan/sourcepinlv
方法： get
请求参数：无
返回参数：pieChartData = [{"value": 1048, "name": '美国国防部'}, {"value": 735, "name": '英国国防部'}, {"value": 580, "name": '法国国防部'},...]

#向前端传递筛选好的新闻地域分布统计数据
请求地址：  /QingBaoXinXiGaiLan/diyu
方法： get
请求参数：无
返回参数： pieChartData2 = [{"value": 1048, "name": '美国'}, {"value": 735, "name": '英国'}, {"value": 580, "name": '法国'},]

#向后端传递选择的新闻对应的id，int类型的，对应的查询参数名称为news_id，向前端传递连续7天的热度值
请求地址： /ZiXunXinXiGaiLan/heat
方法： post
请求参数：定义NewsID数据结构，id为int型
返回参数：[1，2，3，4，5，6，7]

#向前端传递新闻来源对应的国家和等级
请求地址：  /ZiXunXinXiGaiLan/selectsource
方法： get
请求参数：无
返回参数：{'白宫': ('二级', '美国'), '美国国防部': ('一级', '美国'), '韩国国防部': ('三级', '韩国'), '北约': ('二级', '其他'), '意大利国防部': ('二级', '意大利'), '英国国防部': ('一级', '英国'), '法国国防部': ('三级', '法国'), '德国联邦国防部': ('一级', '德国')}

#向前端传递每个新闻来源最新的新闻
请求地址：  /ZiXunXinXiGaiLan/latestnews
方法： get
请求参数：无
返回参数：((id, source, time,title, text, translate_text,summary,emotion,heats,translate_text, country, level, release_time), ...)





#情报意图倾向

#向后端传递时间、来源以及关键词，向前端传递筛选出的新闻信息。
请求地址：  /ZiXunYiTuQingXiang/data2
方法： post
请求参数：无
返回参数：定义DataInput数据结构，包括开始日期、结束日期、来源、关键词

{

'startDate': '2024-07-10', 

'endDate': '2024-07-11', 

'source': '',

 'text': ''

}

返回参数：
((id, source, time,title, text, translate_text,summary,emotion,heats,translate_text, country, level, release_time), ...)

#向后端传递选择的新闻对应的id，int类型的，对应的查询参数名称为news_id，向前端传递与该新闻匹配的所有新闻
请求地址：  /ZiXunYiTuQingXiang/disppath
方法： post
请求参数：定义NewsID数据结构，id为int型
返回参数：((id, source, time,title, text, translate_text,summary,emotion,heats,translate_text, country, level, release_time), ...)

#向前端传递新闻来源对应的国家和等级
请求地址： /ZiXunYiTuQingXiang/selectsource
方法： get
请求参数：无
返回参数：{'白宫': ('二级', '美国'), '美国国防部': ('一级', '美国'), '韩国国防部': ('三级', '韩国'), '北约': ('二级', '其他'), '意大利国防部': ('二级', '意大利'), '英国国防部': ('一级', '英国'), '法国国防部': ('三级', '法国'), '德国联邦国防部': ('一级', '德国')}

#向前端传递每个新闻来源最新的新闻
请求地址：  /ZiXunYiTuQingXiang/latestnews
方法： get
请求参数：无
返回参数：((id, source, time,title, text, translate_text,summary,emotion,heats,translate_text, country, level, release_time), ...)







#信息源管理

#向后端传递更新数据库指令，并传递获取发文量及排名、篇均热度及排名指令
请求地址：  /XinXiYuanGuanLi/update
方法： post
请求参数：无

返回参数：
{"message": "数据库已更新，请明天再试", "status": "error"}

{"message": "数据库更新成功", "status": "success"，"data": updated_data}

updated_data = ["fawenliang": fawenliang, "reduzhi": reduzhi]



#向后端传递获取发文量及排名、篇均热度及排名指令
请求地址：  /XinXiYuanGuanLi/lastTwoColumns
方法： post
请求参数：定义NewsID数据结构，id为int型
返回参数：updated_data = ["fawenliang": fawenliang, "reduzhi": reduzhi]



#向后端传递信息源对应的国家和等级，更新信息源配置
请求地址：/XinXiYuanGuanLi/updateConfig
方法： get
请求参数：无
返回参数：{"message": "配置更新成功", "status": "success"}