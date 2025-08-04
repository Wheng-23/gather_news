import re
def split_string(s):
    # 使用正则表达式分割字符串，分隔符为 / 和 &
    return re.split(r'[\/&]', s)

print(split_string(' '))
