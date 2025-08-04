from config.mysqlop import Mysqlop
from config.baiduapi import translation_baidu


def update_title_ch_baidu(id):
    a = Mysqlop()
    for i in range(id, a.get_row_count() + 1):
    # for i in range(id, 2048):
        data_str = a.getData(i - 1, 1, "title")
        translation = translation_baidu(data_str)
        print(translation)
        a.updateSummary('translate_title', translation, i)


if __name__ == "__main__":
    update_title_ch_baidu(2132)