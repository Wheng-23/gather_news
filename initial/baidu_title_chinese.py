from config.mysqlop import Mysqlop
from config.baiduapi import translation_baidu

a = Mysqlop()
for i in range(a.get_row_count()):
    data_str = a.getData(i, 1, "title")
    translation = translation_baidu(data_str)
    print(translation)
    a.updateSummary('translate_title', translation, i + 1)