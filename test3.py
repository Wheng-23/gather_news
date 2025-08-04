def get_elements(n1, n2, n3):
    elements = ["大安", "留连", "速喜", "赤口", "小吉", "空亡", "病符", "桃花", "天德"]

    # 从“大安”开始，获取对应的元素
    first_index = (n1 - 1) % len(elements)
    second_index = (n1 + n2 - 2) % len(elements)
    third_index = (n1 + n2 + n3 - 3) % len(elements)

    return elements[first_index], elements[second_index], elements[third_index]

# 示例调用
n1 = 9
n2 = 27
n3 = 6
result = get_elements(n1, n2, n3)
print(result)