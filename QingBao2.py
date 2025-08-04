from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
# 引入uvicorn，用于启动服务器
import uvicorn
import re
from config.mysqlop import Mysqlop
from collections import Counter
from dateutil.relativedelta import relativedelta
import jieba.analyse
from similarities import Similarity
# import config
# 创建Fastapi应用的实例，名为app
# app = FastAPI()
app = APIRouter()

# origins = ["*"]
a = Mysqlop()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# # 定义数据结构，包括日期、来源、关键词
class DataInput(BaseModel):
    startDate: Optional[str] = Field(None, example="")
    endDate: Optional[str] = Field(None, example="")
    source: Optional[str] = Field(None, example="")
    text: Optional[str] = Field(None, example="")

def select_source(source):
    if source == "白宫":
        return "THE WHITE HOUSE"
    elif source == "美国国防部":
        return "U.S. Department of Defense"
    elif source == "北约":
        return "North Atlantic Treaty Organization"
    elif source == "韩国国防部":
        return "Ministry of National Defense of South Korea"
    elif source == "英国国防部":
        return "British Ministry of Defence"
    elif source == "法国国防部":
        return "French Ministry of Defence"
    elif source == "意大利国防部":
        return "Italian Ministry of Defence"
    elif source == "德国联邦国防部":
        return "German Federal Ministry of Defence"
    else:
        return source

def split_and_enumerate(s):
    # 首先根据 & 分割
    parts = s.split('&')
    # 去除多余的空格
    parts = [part.strip() for part in parts]

    # 递归生成组合的函数
    def generate_combinations(parts):
        if not parts:
            return ['']
        first, rest = parts[0], parts[1:]
        # 对第一个部分根据 / 分割
        options = first.split('/')
        combinations = generate_combinations(rest)
        result = []
        for option in options:
            for combination in combinations:
                if combination:  # Avoid adding an extra comma at the end
                    result.append(option + ',' + combination)
                else:
                    result.append(option)
        return result

    # 调用生成组合的函数
    combinations = generate_combinations(parts)
    # 去重
    unique_combinations = list(set(combinations))
    return unique_combinations

def split_string(s):
    # 使用正则表达式分割字符串，分隔符为 / 和 &
    return re.split(r'[\/&]', s)

@app.post('/ZiXunYiTuQingXiang/data2')
# 接收返回前端传来的情报配置参数，表达格式的数据，包括日期、来源、关键词
# 返回值包括筛选出来的所有新闻，每条新闻包括新闻标题，热度值，摘要，来源，地点
async def DataIuput(data: DataInput):
    a = Mysqlop()

    received_data = data.dict()
    print(received_data)
    global inputtags
    inputtags = split_string(data.text)
    print(inputtags)

    start_date = data.startDate if data.startDate else None
    end_date = data.endDate if data.endDate else None
    source = select_source(data.source) if data.source else None
    # keywords = data.text if data.text else None
    print(data.text)
    keywords_list = split_and_enumerate(data.text) if data.text else None
    print(keywords_list)

    # 初始化news为一个空列表
    news = []
    news_ids = set()
    data = a.select_country()
    # 转换成列表
    result = [item[0] for item in data if item[0] is not None]

    if keywords_list:
        for keywords in keywords_list:
            if start_date and end_date and source:
                formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
                formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
                if source in ["一级", "二级", "三级"]:
                    fetched_news = a.selectnews_by_date_level_keywords(source, formatted_start_date, formatted_end_date,
                                                                       keywords)
                elif source in result:
                    fetched_news = a.selectnews_by_date_country_keywords(source, formatted_start_date,
                                                                         formatted_end_date,
                                                                         keywords)
                else:
                    fetched_news = a.selectnews_by_date_source_keywords(source, formatted_start_date,
                                                                        formatted_end_date, keywords)
            elif source:
                if source in ["一级", "二级", "三级"]:
                    fetched_news = a.selectnews_by_level_and_keywords(source, keywords)
                elif source in result:
                    fetched_news = a.selectnews_by_country_and_keywords(source, keywords)
                else:
                    fetched_news = a.selectnews_by_source_and_keywords(source, keywords)
            elif start_date and end_date:
                formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                    "%B %d, %Y").upper()
                formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
                fetched_news = a.selectnews_by_date_and_keywords(formatted_start_date, formatted_end_date, keywords)
            else:
                fetched_news = a.selectnews_by_keywords(keywords)
            for news_item in fetched_news:
                if news_item[0] not in news_ids:
                    news_ids.add(news_item[0])
                    news.append(news_item)
    else:
        if start_date and end_date and source:
            formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
            formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
            if source in ["一级", "二级", "三级"]:
                news = a.selectnews_by_date_and_level(source, formatted_start_date, formatted_end_date)
            elif source in result:
                news = a.selectnews_by_date_and_country(source, formatted_start_date, formatted_end_date)
            else:
                news = a.selectnews_by_date_and_source(source, formatted_start_date, formatted_end_date)
        elif start_date and end_date:
            formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%B %d, %Y").upper()
            formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%B %d, %Y").upper()
            news = a.selectnews_by_date(formatted_start_date, formatted_end_date)
        elif source:
            if source in {"一级", "二级", "三级"}:
                news = a.selectnews_by_level(source)
            elif source in result:
                news = a.selectnews_by_country(source)
            else:
                news = a.selectnews_by_source(source)
        else:
            return {"message": "至少需要一个参数进行搜索", "status": "error"}
    # 调数据库，根据接收的数据从表中筛选出符合条件的新闻，

    '''
    自己写一个查数据表的方法，返回筛选后的数据

    '''
    respons_data = []  # 初始化响应数据列表
    for news_item in news:
        summary = news_item[6] if news_item[6] else ("根据相关法律法规，该内容信息可能涉及国家安全的信息、"
                                                     "涉及政治与宗教类的信息、"
                                                     "涉及暴力与恐怖主义的信息、涉及黄赌毒类的信息、涉及不文明的信息。我们会继续遵循相关法规法律的要求，"
                                                     "共创一个健康和谐网络环境，谢谢您的理解")
        # 创建字典，存储新闻的相关信息
        news_dict = {
            "id": news_item[0],
            "title": news_item[16],
            "heat": news_item[8],
            "summary": summary,
            "sources": news_item[1],
            "date": news_item[2],
            "yitu":news_item[7]
        }
        respons_data.append(news_dict)

    return respons_data

def source_ch(source):
    if source == "THE WHITE HOUSE":
        return "白宫"
    elif source == "U.S. Department of Defense":
        return "美国国防部"
    elif source == "North Atlantic Treaty Organization":
        return "北约"
    elif source == "Ministry of National Defense of South Korea":
        return "韩国国防部"
    elif source == "British Ministry of Defence":
        return "英国国防部"
    elif source == "French Ministry of Defence":
        return "法国国防部"
    elif source == "Italian Ministry of Defence":
        return "意大利国防部"
    elif source == "German Federal Ministry of Defence":
        return "德国联邦国防部"
    else:
        return "Unknown Source"

def keyword_extract(extracted_sentences,inputtags):
    topKtags=jieba.analyse.extract_tags(extracted_sentences, topK=5, withWeight=False, allowPOS=())
    totaltags=list(set(topKtags+inputtags))
    return totaltags
def keyword_match(texts, keywords):
    # 计算关键词列表长度的三分之一作为阈值
    threshold = len(keywords) / 3

    # 符合条件的文本信息列表
    matched_texts = []

    # 遍历每条文本信息
    for text in texts:
        # text是每条新闻，text[16]是中文新闻标题
        # 使用 jieba 进行分词
        words = jieba.lcut(str(text[16]))
        word_count = Counter(words)

        # 统计匹配的关键词个数
        match_count = sum((word_count[keyword] > 0) for keyword in keywords)

        # 判断匹配关键词个数是否大于或等于阈值,大于阈值的话添加该新闻的id
        if match_count >= threshold:
            matched_texts.append(text)

    return matched_texts
def semantic_match(sentences, corpus):
    # model = Similarity(model_name_or_path="shibing624/text2vec-base-chinese")
    model = Similarity(model_name_or_path="text2vec-base-chinese")

    print(model)

    dict1 = dict()
    result=[]
    id_result=[]


    # 按照相似度分数从高到低排序
    # corpu是每条新闻，corpu[16]是中文新闻标题
    for corpu in corpus:
        similarity_scores = model.similarity(sentences, corpu[16])
        print(similarity_scores)
        if similarity_scores.item() > 0.5:
            dict1[corpu[0]] = similarity_scores.item()
            id_result.append(corpu[0])
        model.add_corpus(corpu[16])
    print(id_result)
    print(dict1)
    for corpu in corpus:
        print(corpu[0])
        if corpu[0] in id_result:
            result.append(corpu)


    print(result)
    return result
# 接口2，用户在前端点击显示路径按钮后，将点击新闻的序号传给后端，后端根据序号确定新闻，提取该新闻标题中的关键词组合，根据关键词组合，检索历史新闻数据库中的新闻内容一列，找到相关度高的历史新闻；
# 按照发布时间，降序排列，返回给前端显示
class NewsID(BaseModel):
    id: int

# @app.post('/QingBaoYiTuQingXiang/disppath')
# async def DataIuput(news_id: NewsID):
#     print(news_id)
#     new = a.selectnewsbyid(news_id.id)
#     print(new)
#     print(new[3])
#     data_str = new[3]
#     spacy_nlp = spacy.load("en_core_web_lg")
#     # spacy_nlp = spacy.load()
#
#     spacy_nlp.add_pipe("textrank")
#     doc = spacy_nlp(data_str)
#
#     words = []
#     # examine the top-ranked phrases in the document
#     for phrase in doc._.phrases:
#         # print(phrase.rank, phrase.count)
#         # print(phrase.chunks[0])
#         words.append(phrase.chunks[0])
#
#     print(words[0])
#     # print(words[1])
#     # print(words[2])
#     news = a.select_path(words[0])
#     respons_data = []  # 初始化响应数据列表
#     for news_item in news:
#         summary = news_item[6] if news_item[6] else ("根据相关法律法规，该内容信息可能涉及国家安全的信息、"
#                                                      "涉及政治与宗教类的信息、"
#                                                      "涉及暴力与恐怖主义的信息、涉及黄赌毒类的信息、涉及不文明的信息。我们会继续遵循相关法规法律的要求，"
#                                                      "共创一个健康和谐网络环境，谢谢您的理解")
#         # 创建字典，存储新闻的相关信息
#         news_dict = {
#             "title": news_item[16],
#             "summary": summary,
#             "sources": source_ch(news_item[1]),
#             "date": datetime.strptime(news_item[2], "%B %d, %Y").strftime("%Y年%m月%d日"),
#         }
#         respons_data.append(news_dict)
#
#     return respons_data
@app.post('/ZiXunYiTuQingXiang/disppath')
async def DataIuput(news_id: NewsID):
    a = Mysqlop()
    print(news_id)
    new = a.selectnewsbyid(news_id.id)
    print(new[16])
    data_str = new[16]
    # 提取中文关键词,和之前用户的关键词汇总,函数输入的第二个变量inputtags是用户输入的关键词列表，可以在前面global一下，然后这个里面用，我这里暂时是空白的
    '''
        我刚才type看了一下，你之前的news是元组，可用_add_方法添加元素
        我直接指定了list，然后append添加,最好把元组都转为列表
    '''
    # total_keyword=keyword_extract(data_str, [])
    total_keyword=keyword_extract(data_str, inputtags)

    # news是当前日期前三个月的新闻列表
    formatted_end_date = str(new[2])
    date = datetime.strptime(formatted_end_date, "%B %d, %Y")
    two_months_ago = date - relativedelta(months=2)
    one_day_ago = date - relativedelta(days=1)
    formatted_start_date = two_months_ago.strftime("%B %d, %Y")
    formatted_end_date = one_day_ago.strftime("%B %d, %Y")
    news = a.selectnews_by_date(formatted_start_date, formatted_end_date)
    list(news)
    # 关键词匹配
    listB = keyword_match(news, total_keyword)
    # 语义匹配
    listC = semantic_match(new[16], listB)
    # 返回结果
    respons_data = []  # 初始化响应数据列表
    for news_item in listC:
        summary = news_item[6] if news_item[6] else ("根据相关法律法规，该内容信息可能涉及国家安全的信息、"
                                                     "涉及政治与宗教类的信息、"
                                                     "涉及暴力与恐怖主义的信息、涉及黄赌毒类的信息、涉及不文明的信息。我们会继续遵循相关法规法律的要求，"
                                                     "共创一个健康和谐网络环境，谢谢您的理解")
        # 创建字典，存储新闻的相关信息
        news_dict = {
            "title": news_item[16],
            "summary": summary,
            "sources": source_ch(news_item[1]),
            "date": datetime.strptime(news_item[2], "%B %d, %Y").strftime("%Y年%m月%d日"),
        }
        respons_data.append(news_dict)

    return respons_data

@app.get('/ZiXunYiTuQingXiang/selectsource')
async def update_select_source():
    a = Mysqlop()
    data = {
        '白宫': a.get_levelandcountry_bysource('THE WHITE HOUSE'),
        '美国国防部': a.get_levelandcountry_bysource('U.S. Department of Defense'),
        '韩国国防部': a.get_levelandcountry_bysource(
            'Ministry of National Defense of South Korea'),
        '北约': a.get_levelandcountry_bysource('North Atlantic Treaty Organization'),
        '意大利国防部': a.get_levelandcountry_bysource('Italian Ministry of Defence'),
        '英国国防部': a.get_levelandcountry_bysource('British Ministry of Defence'),
        '法国国防部': a.get_levelandcountry_bysource('French Ministry of Defence'),
        '德国联邦国防部': a.get_levelandcountry_bysource('German Federal Ministry of Defence'),
    }
    return data

@app.get('/ZiXunYiTuQingXiang/latestnews')
async def put_latest_news():
    a = Mysqlop()
    global inputtags
    inputtags = []
    print(inputtags)
    news_white = a.select_news_by_latest_time_by_source('THE WHITE HOUSE', 'THE WHITE HOUSE')
    news_dod = a.select_news_by_latest_time_by_source('U.S. Department of Defense', 'U.S. Department of Defense')
    news_korea = a.select_news_by_latest_time_by_source('Ministry of National Defense of South Korea',
                                                      'Ministry of National Defense of South Korea')
    news_nato = a.select_news_by_latest_time_by_source('North Atlantic Treaty Organization',
                                                      'North Atlantic Treaty Organization')
    news_italy = a.select_news_by_latest_time_by_source('Italian Ministry of Defence', 'Italian Ministry of Defence')
    news_british = a.select_news_by_latest_time_by_source('British Ministry of Defence', 'British Ministry of Defence')
    news_french = a.select_news_by_latest_time_by_source('French Ministry of Defence', 'French Ministry of Defence')
    news_german = a.select_news_by_latest_time_by_source('German Federal Ministry of Defence',
                                                         'German Federal Ministry of Defence')
    news = news_white + news_dod + news_korea + news_nato + news_italy + news_british + news_french + news_german
    respons_data = []  # 初始化响应数据列表
    for news_item in news:
        summary = news_item[6] if news_item[6] else ("根据相关法律法规，该内容信息可能涉及国家安全的信息、"
                                                     "涉及政治与宗教类的信息、"
                                                     "涉及暴力与恐怖主义的信息、涉及黄赌毒类的信息、涉及不文明的信息。我们会继续遵循相关法规法律的要求，"
                                                     "共创一个健康和谐网络环境，谢谢您的理解")
        # 创建字典，存储新闻的相关信息
        news_dict = {
            "id": news_item[0],
            "title": news_item[16],
            "heat": news_item[8],
            "summary": summary,
            "sources": news_item[1],
            "date": news_item[2],
            "yitu":news_item[7]
        }
        respons_data.append(news_dict)

    return respons_data


if __name__ == "__main__":


    uvicorn.run(app="QingBao2:app", host="127.0.0.1", port=8080, reload=True)