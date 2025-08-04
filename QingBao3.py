from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,timedelta
# 引入uvicorn，用于启动服务器
import uvicorn
from config.mysqlop import Mysqlop
from update.update_data import update
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

@app.post('/XinXiYuanGuanLi/update')
async def gengxin():
    # 接受更新数据库指令，进行更新
    latest_time = await get_latest_time()
    yesterday = datetime.now() - timedelta(days=1)
    print(yesterday.date())
    # 检查最后一条数据的日期是否是今天
    if latest_time == yesterday.date():
        return {"message": "数据库已更新，请明天再试", "status": "error"}
    update()

    updated_data = await update_rank()
    return {"message": "数据库更新成功", "status": "success", "data": updated_data}


async def update_rank():
    a = Mysqlop()
    entities = [
        'U.S. Department of Defense',
        'THE WHITE HOUSE',
        'Ministry of National Defense of South Korea',
        'British Ministry of Defence',
        'Italian Ministry of Defence',
        'French Ministry of Defence',
        'German Federal Ministry of Defence',
        'North Atlantic Treaty Organization'
    ]

    # Retrieve heat values for each entity
    heat_values = {entity: a.select_avg_nextday(entity) for entity in entities}

    # Sort heat values and assign ranks
    sorted_heats = sorted(heat_values.values(), reverse=True)
    ranked_heats = {heat: rank + 1 for rank, heat in enumerate(sorted_heats)}

    # Function to get heat value and rank for an entity
    def get_heat_rank(entity):
        if entity in heat_values:
            heat = heat_values[entity]
            return f"{heat}/{ranked_heats[heat]}"
        return "Entity not found"

    # Get yesterday's date
    week_ago = datetime.now() - timedelta(days=7)
    # formatted_date_str = yesterday.date().strftime('%B %d, %Y').upper()
    # print(formatted_date_str)
    # Retrieve and rank paper counts for each entity
    # papers = a.select_num_papers(formatted_date_str)
    papers = a.select_num_papers(week_ago)
    papers_dict = {item[0]: item[1] for item in papers}
    sorted_papers = sorted(papers_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_papers_dict = {key: f"{value}/{rank + 1}" for rank, (key, value) in enumerate(sorted_papers)}

    # Create updated data with both heat rank and paper count rank
    updated_data = []
    for entity in entities:
        fawenliang = ranked_papers_dict.get(entity, "0/8")
        reduzhi = get_heat_rank(entity)
        updated_data.append({"fawenliang": fawenliang, "reduzhi": reduzhi})

    return updated_data


async def get_latest_time():
    a = Mysqlop()
    latest_time_str_white = a.select_latest_time_by_source('THE WHITE HOUSE')
    print(latest_time_str_white)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_white = datetime.strptime(latest_time_str_white, "%B %d, %Y")
    print(latest_time_white.date())
    days_ago_white = latest_time_white.date()

    latest_time_str_us_defense = a.select_latest_time_by_source('U.S. Department of Defense')
    print(latest_time_str_us_defense)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_us_defense = datetime.strptime(latest_time_str_us_defense, "%B %d, %Y")
    print(latest_time_us_defense.date())
    days_ago_us_defense = latest_time_us_defense.date()

    latest_time_str_korea = a.select_latest_time_by_source('Ministry of National Defense of South Korea')
    print(latest_time_str_korea)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_korea = datetime.strptime(latest_time_str_korea, "%B %d, %Y")
    print(latest_time_korea.date())
    days_ago_korea = latest_time_korea.date()

    latest_time_str_british = a.select_latest_time_by_source('British Ministry of Defence')
    print(latest_time_str_british)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_british = datetime.strptime(latest_time_str_british, "%B %d, %Y")
    print(latest_time_british.date())
    days_ago_british = latest_time_british.date()

    latest_time_str_french = a.select_latest_time_by_source('French Ministry of Defence')
    print(latest_time_str_french)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_french = datetime.strptime(latest_time_str_french, "%B %d, %Y")
    print(latest_time_french.date())
    days_ago_french = latest_time_french.date()


    latest_time_str_NATO = a.select_latest_time_by_source('North Atlantic Treaty Organization')
    print(latest_time_str_NATO)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_NATO = datetime.strptime(latest_time_str_NATO, "%B %d, %Y")
    print(latest_time_NATO.date())
    days_ago_NATO = latest_time_NATO.date()

    latest_time_str_italy = a.select_latest_time_by_source('Italian Ministry of Defence')
    print(latest_time_str_italy)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_italy = datetime.strptime(latest_time_str_italy, "%B %d, %Y")
    print(latest_time_italy.date())
    days_ago_italy = latest_time_italy.date()

    latest_time_str_german = a.select_latest_time_by_source('German Federal Ministry of Defence')
    print(latest_time_str_german)
    # 解析 "JULY 01, 2024" 格式的日期
    latest_time_str_german = datetime.strptime(latest_time_str_german, "%B %d, %Y")
    print(latest_time_str_german.date())
    days_ago_german = latest_time_str_german.date()

    # 比较日期对象，找到最小日期
    min_date = min(days_ago_white, days_ago_us_defense, days_ago_korea,
                   days_ago_british, days_ago_french, days_ago_NATO,days_ago_german,days_ago_italy)
    return min_date


# # 定义数据结构，包括日期、来源、关键词
class DataInput(BaseModel):
    title: Optional[str] = Field(None, example="")
    country: Optional[str] = Field(None, example="")
    level: Optional[str] = Field(None, example="")


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
        return "Unknown Source"
# # 模拟的最后两列数据
# last_two_columns = [
#     {"fawenliang": "50/1", "reduzhi": "15/2"},
#     {"fawenliang": "46/2", "reduzhi": "19/1"},
#     {"fawenliang": "52/3", "reduzhi": "14/3"},
#     {"fawenliang": "42/5", "reduzhi": "16/5"},
#     {"fawenliang": "48/4", "reduzhi": "18/4"},
#     {"fawenliang": "47/6", "reduzhi": "17/6"},
#     {"fawenliang": "45/7", "reduzhi": "20/7"},
#     {"fawenliang": "51/8", "reduzhi": "13/8"},
# ]

# 路由：获取最后两列数据
@app.get('/XinXiYuanGuanLi/lastTwoColumns')
async def get_last_two_columns():
    updated_data = await update_rank()
    return updated_data

def update_country_level(data_list: list[dict]):
    # 在这里处理数据库更新逻辑，这里简化为打印出接收到的数据
    for data in data_list:
        print(f"Updating data: {data}")
        source = data.get('title')
        source = select_source(source)
        print(source)
        country = data.get('country')
        print(country)
        level = data.get('level')
        print(level)
        a = Mysqlop()
        a.updateCountry('country', country, source)
        a.updateLevel('level', level, source)


@app.post('/XinXiYuanGuanLi/updateConfig')
# 接收返回前端传来的情报配置参数，表达格式的数据，包括日期、来源、关键词
# 返回值包括筛选出来的所有新闻，每条新闻包括新闻标题，热度值，摘要，来源，地点
async def update_config(data_list: list[DataInput]):
    try:
        # 这里可以添加更新配置的具体逻辑
        update_country_level([data.dict() for data in data_list])
        # 模拟更新配置成功，不做任何数据库操作
        return {"message": "配置更新成功", "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}

@app.get('/XinXiYuanGuanLi/selectsource')
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

if __name__ == "__main__":


    # uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
    uvicorn.run(app="QingBao3:app", host="127.0.0.1", port=8084, reload=True)
