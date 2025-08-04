import re
from snownlp import SnowNLP
from config.mysqlop import Mysqlop
# 定义友好国家和不友好国家集合
friendly_countries = {"巴勒斯坦", "俄罗斯", "塞尔维亚", "中国", "北韩"}
unfriendly_countries = {"美国", "以色列", "欧盟", "韩国","北约"}



# 定义计算国家出现频次的函数
def calculate_country_frequencies(news_content, friendly_countries, unfriendly_countries):
    friendly_count = sum(news_content.count(country) for country in friendly_countries)
    unfriendly_count = sum(news_content.count(country) for country in unfriendly_countries)
    total_count = len(re.findall(r'\b\w+\b', news_content))

    P = friendly_count / total_count if total_count > 0 else 0
    Q = unfriendly_count / total_count if total_count > 0 else 0

    return P, Q


# 计算正负面度指标
def calculate_sentiment(news_content):
    s = SnowNLP(news_content)
    return s.sentiments


# 判定情报意图
def determine_intelligence_intent(P, Q, S, p, q, s1, s2):
    if (P > p and S > s1) or (Q > q and S < s2):
        return "积极"
    elif (P > p and S < s2) or (Q > q and S > s1):
        return "消极"
    else:
        return "中立"


# 设置阈值
p = 0.05
q = 0.05
s1 = 0.7
s2 = 0.3


def initial_tend(id):
    a = Mysqlop()
    for i in range(id, 512):
        news_content = a.getData(i - 1, 1, "summary")
        if not news_content:  # 检查新闻内容是否为空
            intent = "中立"
            print(f"情报意图: {intent}")
        else:
            # 计算频次占比
            P, Q = calculate_country_frequencies(news_content, friendly_countries, unfriendly_countries)
            # 计算正负面度指标
            S = calculate_sentiment(news_content)
            # 判定情报意图
            intent = determine_intelligence_intent(P, Q, S, p, q, s1, s2)
            # 打印结果
            print(f"友好国家出现频次占比 (P): {P:.2f}")
            print(f"不友好国家出现频次占比 (Q): {Q:.2f}")
            print(f"新闻正负面度指标 (S): {S:.2f}")
            print(f"情报意图: {intent}")
        a.updateEmotion('emotion', intent, i)




if __name__ == '__main__':
    initial_tend(1)

