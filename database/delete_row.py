from config.mysqlop import Mysqlop

a = Mysqlop()
a.delete_Data(2238,2238)
# a.delete_databytime("JUNE , 2024")
# a.delete_databytime("JUNE 2, 2024")
# a.delete_databytime("JULY 1, 2024")
# latest_time = a.select_latest_time()
# print(latest_time)
# rowcount = a.get_row_count()
# print(rowcount)
# latest_time_str = a.getData(rowcount - 1, 1, 'time')
# if latest_time_str:
#     # 解析 "JULY 01, 2024" 格式的日期
#     latest_time = datetime.strptime(latest_time_str, "%B %d, %Y")
#     yesterday = datetime.now() - timedelta(days=0)
#     # 检查最后一条数据的日期是否是今天
#     if latest_time.date() == yesterday.date():
#         print("相同")
#     else:
#         print("不同")