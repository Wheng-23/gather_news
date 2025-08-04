from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
# 引入uvicorn，用于启动服务器
import uvicorn
import spacy
from config.mysqlop import Mysqlop
from collections import Counter

# 创建Fastapi应用的实例，名为app
# app = FastAPI()
app = APIRouter()

# origins = ["*"]

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

# 关键词分割，输入是前端传来的关键词字符串，输出是分割后的关键词列表
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

@app.post('/ZiXunXinXiGaiLan/data')
# 接收返回前端传来的情报配置参数，表达格式的数据，包括日期、来源、关键词
# 返回值包括筛选出来的所有新闻，每条新闻包括新闻标题，热度值，摘要，来源，地点
async def DataIuput(data: DataInput):
    a = Mysqlop()
    # 接收前端传来的数据
    # 调数据库，根据接收的数据从表中筛选出符合条件的新闻，
    received_data = data.dict()
    print(received_data)

    start_date = data.startDate if data.startDate else None
    end_date = data.endDate if data.endDate else None
    source = select_source(data.source) if data.source else None
    # keywords = data.text if data.text else None
    keywords_list = split_and_enumerate(data.text) if data.text else None

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
                    fetched_news = a.selectnews_by_date_country_keywords(source, formatted_start_date, formatted_end_date,
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
    '''
    自己写一个查数据表的方法，返回筛选后的数据
    '''
    global respons_data
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
            "translate_text":news_item[5]
        }
        respons_data.append(news_dict)
    # 按照 heat 的大小从大到小排序
    respons_data.sort(key=lambda x: x['heat'], reverse=True)
    return respons_data

# 用于统计统计筛选出的新闻中，不同来源的新闻数量，
@app.get('/ZiXunXinXiGaiLan/sourcepinlv')
async def sourcepinlv():

    # 测试示例
    sources = []
    for item in respons_data:
        sources.append(item["sources"])
    source_counts = Counter(sources)
    result = [{"value": count, "name": source_ch(source)} for source, count in source_counts.items()]
    # 测试示例
    # pieChartData = [{"value": 1048, "name": '美国国防部'}, {"value": 735, "name": '英国国防部'}, {"value": 580, "name": '法国国防部'},]
    pieChartData = result
    return pieChartData

# # 统计筛选出的新闻中，不同地域的新闻数量
# @app.get('/QingBaoXinXiGaiLan/diyu')
# async def diyu():
#
#     replace_dict = {
#         'U.S. Department of Defense': '美国',
#         'Ministry of National Defense of South Korea': '韩国',
#         'THE WHITE HOUSE': '美国',
#         'North Atlantic Treaty Organization': '北约',
#         'Italian Ministry of Defence': '意大利',
#         'British Ministry of Defence': '英国',
#         'French Ministry of Defence': '法国',
#         'German Federal Ministry of Defence': '德国',
#
#     }
#     locations = []
#     for item in respons_data:
#         locations.append(item["sources"])
#     new_location = [replace_dict.get(location, location) for location in locations]
#
#     print(locations)
#     print(new_location)
#     location_counts = Counter(new_location)
#     result = [{"value": count, "name": location} for location, count in location_counts.items()]
#     # 测试示例
#     # pieChartData2 = [{"value": 1048, "name": '美国'}, {"value": 735, "name": '英国'}, {"value": 580, "name": '法国'},]
#     pieChartData2 = result
#     return pieChartData2

# 示例地名列表（可以替换为更完整的地名数据库）
valid_locations = {
    '阿富汗', '阿尔巴尼亚', '阿尔及利亚', '安道尔', '安哥拉', '安提瓜和巴布达', '阿根廷', '亚美尼亚', '澳大利亚', '奥地利',
    '阿塞拜疆', '巴哈马', '巴林', '孟加拉国', '巴巴多斯', '白俄罗斯', '比利时', '伯利兹', '贝宁', '不丹',
    '玻利维亚', '波黑', '博茨瓦纳', '巴西', '文莱', '保加利亚', '布基纳法索', '布隆迪', '佛得角', '柬埔寨',
    '喀麦隆', '加拿大', '中非共和国', '乍得', '智利', '中国', '哥伦比亚', '科摩罗', '刚果民主共和国', '刚果共和国',
    '哥斯达黎加', '科特迪瓦', '克罗地亚', '古巴', '塞浦路斯', '捷克', '丹麦', '吉布提', '多米尼克', '多米尼加',
    '厄瓜多尔', '埃及', '萨尔瓦多', '赤道几内亚', '厄立特里亚', '爱沙尼亚', '埃斯瓦蒂尼', '埃塞俄比亚', '斐济', '芬兰',
    '法国', '加蓬', '冈比亚', '格鲁吉亚', '德国', '加纳', '希腊', '格林纳达', '危地马拉', '几内亚',
    '几内亚比绍', '圭亚那', '海地', '洪都拉斯', '匈牙利', '冰岛', '印度', '印度尼西亚', '伊朗', '伊拉克',
    '爱尔兰', '以色列', '意大利', '牙买加', '日本', '约旦', '哈萨克斯坦', '肯尼亚', '基里巴斯', '朝鲜',
    '韩国', '科威特', '吉尔吉斯斯坦', '老挝', '拉脱维亚', '黎巴嫩', '莱索托', '利比里亚', '利比亚', '列支敦士登',
    '立陶宛', '卢森堡', '马达加斯加', '马拉维', '马来西亚', '马尔代夫', '马里', '马耳他', '马绍尔群岛', '毛里塔尼亚',
    '毛里求斯', '墨西哥', '密克罗尼西亚', '摩尔多瓦', '摩纳哥', '蒙古', '黑山', '摩洛哥', '莫桑比克', '缅甸',
    '纳米比亚', '瑙鲁', '尼泊尔', '荷兰', '新西兰', '尼加拉瓜', '尼日尔', '尼日利亚', '北马其顿', '挪威',
    '阿曼', '巴基斯坦', '帕劳', '巴勒斯坦', '巴拿马', '巴布亚新几内亚', '巴拉圭', '秘鲁', '菲律宾', '波兰',
    '葡萄牙', '卡塔尔', '罗马尼亚', '俄罗斯', '卢旺达', '圣基茨和尼维斯', '圣卢西亚', '圣文森特和格林纳丁斯', '萨摩亚', '圣马力诺',
    '圣多美和普林西比', '沙特阿拉伯', '塞内加尔', '塞尔维亚', '塞舌尔', '塞拉利昂', '新加坡', '斯洛伐克', '斯洛文尼亚', '所罗门群岛',
    '索马里', '南非', '南苏丹', '西班牙', '斯里兰卡', '苏丹', '苏里南', '瑞典', '瑞士', '叙利亚',
    '塔吉克斯坦', '坦桑尼亚', '泰国', '东帝汶', '多哥', '汤加', '特立尼达和多巴哥', '突尼斯', '土耳其', '土库曼斯坦',
    '图瓦卢', '乌干达', '乌克兰', '阿联酋', '英国', '美国', '乌拉圭', '乌兹别克斯坦', '瓦努阿图', '梵蒂冈',
    '委内瑞拉', '越南', '也门', '赞比亚', '津巴布韦'
}

nlp = spacy.load("zh_core_web_sm")
def keyword_split(text):
    if text is None:
        text = ''

    result = []
    # 使用模型处理文本
    doc = nlp(text)

    # 提取国家
    countries = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    # 过滤有效的地名
    filtered_countries = [country for country in countries if country in valid_locations]
    string_counts = Counter(filtered_countries)
    # string_counts = Counter(countries)

    sorted_counts = sorted(string_counts.items(), key=lambda x: x[1], reverse=True)
    # 打印结果


    result= [(string, count) for string, count in sorted_counts]

    return result

# 统计筛选出的新闻中，不同地域的新闻数量
@app.get('/ZiXunXinXiGaiLan/diyu')
async def diyu():
    all_countries = []
    # for item in respons_data:
    #     text = item.get('translate_text', '')
    #     print(text)
    #     countries = keyword_split(text)
    #     print(countries)
    #     all_countries.extend([country for country, _ in countries])
    with ThreadPoolExecutor() as executor:
        countries_list = list(executor.map(keyword_split, [item.get('translate_text', '') for item in respons_data]))

    for countries in countries_list:
        all_countries.extend([country for country, _ in countries])
    country_counts = Counter(all_countries)
    result = [{"value": count, "name": country} for country, count in country_counts.items()]
    print(result)
    # 按照 value 值降序排序
    sorted_data = sorted(result, key=lambda x: x['value'], reverse=True)
    # 取前 10 项
    result = sorted_data[:10]

    return result


class NewsID(BaseModel):
    id: int


@app.post('/ZiXunXinXiGaiLan/heat')
async def heat(news_id: NewsID):
    # 示例，根据传递的id选择对应的新闻，然后获取该新闻的连续热度值，再进行输出
    print(news_id)
    '''
        自己写一个根据选择的新闻，输出连续几天的热度值的函数，返回数据的格式如下

    '''
    # news=news_data[news_id.id]
    a = Mysqlop()
    new = a.selectnewsbyid(news_id.id)
    print(new)
    heat = []
    # for i in range(8, 15):
    #     heat.append(new[i])
    heat.append(new[13])#T-5天
    heat.append(new[12])
    heat.append(new[11])
    heat.append(new[10])
    heat.append(new[9])
    heat.append(new[8])#T天
    heat.append(new[15])#T+1天
    return heat


@app.get('/ZiXunXinXiGaiLan/selectsource')
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
    print(data)
    return data

@app.get('/ZiXunXinXiGaiLan/latestnews')
async def put_latest_news():
    a = Mysqlop()
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
    global respons_data
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
            "translate_text": news_item[5]
        }
        respons_data.append(news_dict)
    # 按照 heat 的大小从大到小排序
    respons_data.sort(key=lambda x: x['heat'], reverse=True)

    return respons_data


if __name__ == "__main__":


    # uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
    uvicorn.run(app="QingBao:app", host="0.0.0.0", port=8000, reload=True)
