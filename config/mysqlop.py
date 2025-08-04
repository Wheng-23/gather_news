from config import peizhi
from database.MySQLOperation import Mysql

class Mysqlop(object):
    def __init__(self):
        self.TableName = peizhi.table_name
        # self.helper = Mysql('114.55.113.248', 33067, 'news', 'news', 'News_Xw_20400987', 'utf8')#host, port, [database, user, password]这三个改成自己的其他不用改, charset
        db_config = peizhi.DB_CONFIG
        self.helper = Mysql(db_config['host'], db_config['port'], db_config['database'],
                            db_config['user'], db_config['password'], db_config['charset'])
        self.helper.open()

    def saveData(self,id,source, newstime, title, text,datetime):
        #执行存入操作
    	# sql = "INSERT INTO news (source, time, title, text) VALUES ('%s', '%s','%s', '%s')" % (source, time, title, text)
        sql = "insert into news (id,source,time,title,text,release_time) values ('%d','%s','%s','%s','%s','%s')"%(id,source,newstime,title,text,datetime)
        # sql = "INSERT INTO news  VALUES (source, time, title, text)"
        if self.helper.cud(sql):
            print("数据插入成功。")
            return True  # 插入成功
        else:
            print("由于插入失败，ID 不会增加。")
            return False  # 插入失败


    def closeFile(self):
        self.helper.close()

    def clearData(self):
        sql_del = "delete from news"
        print(sql_del)
        self.helper.cud(sql_del)
    def getData(self,startrow,rownumber,column):
        sql_get = "select %s"%column + " from news limit %d,%d"%(startrow,rownumber)
        print(sql_get)
        nested_tuple = self.helper.specific(sql_get)
        print(nested_tuple)
        print(nested_tuple[0][0])
        return nested_tuple[0][0]

    def updateHeat(self,column,heat,id):
        sql_update = "update news set %s = %d where id=%d"%(column,heat,id)
        print(sql_update)
        self.helper.cud(sql_update)

    def updateSummary(self,column,summary,id):
        # sql_update = "update student set %s = %s where id=%d"%(column,summary,id)
        sql_update = "UPDATE news SET %s = '%s' WHERE id=%d" % (column, summary, id)
        print(sql_update)
        self.helper.cud(sql_update)

    def updateEmotion(self,column,emotion,id):
        # sql_update = "update student set %s = %s where id=%d"%(column,summary,id)
        sql_update = "UPDATE news SET %s = '%s' WHERE id=%d" % (column, emotion, id)
        print(sql_update)
        self.helper.cud(sql_update)

    def updateCountry(self,column,country,source):
        # sql_update = "update student set %s = %s where id=%d"%(column,summary,id)
        sql_update = "UPDATE news SET %s = '%s' WHERE source='%s'" % (column, country, source)
        print(sql_update)
        self.helper.cud(sql_update)

    def updateLevel(self,column,level,source):
        # sql_update = "update student set %s = %s where id=%d"%(column,summary,id)
        sql_update = "UPDATE news SET %s = '%s' WHERE source='%s'" % (column, level, source)
        print(sql_update)
        self.helper.cud(sql_update)


    def selectnews_by_date_source_keywords(self,source,start_time,end_time,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and source="%s" and time >= "%s" and time <= "%s"'%(source,start_time,end_time)
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date_level_keywords(self,source,start_time,end_time,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and level="%s" and time >= "%s" and time <= "%s"'%(source,start_time,end_time)
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date_country_keywords(self,source,start_time,end_time,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and country="%s" and time >= "%s" and time <= "%s"'%(source,start_time,end_time)
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple


    def selectnews_by_date_and_source(self,source,start_time,end_time):
        sql_select = 'select * from news where source="%s" and time >= "%s" and time <= "%s"' % (source, start_time,end_time)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date_and_level(self,source,start_time,end_time):
        sql_select = 'select * from news where level="%s" and time >= "%s" and time <= "%s"' % (source, start_time,end_time)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date_and_country(self,source,start_time,end_time):
        sql_select = 'select * from news where country="%s" and time >= "%s" and time <= "%s"' % (source, start_time,end_time)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple


    def selectnews_by_source_and_keywords(self,source,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and source="%s"'%(source)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_level_and_keywords(self,source,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and level="%s"'%(source)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_country_and_keywords(self,source,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and country="%s"'%(source)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date_and_keywords(self,start_time,end_time,keywords):

        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)
        sql_select = sql_select + 'and time >= "%s" and time <= "%s"'%(start_time,end_time)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_date(self,start_time,end_time):
        sql_select = 'select * from news where time >= "%s" and time <= "%s"'%(start_time,end_time)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_source(self,source):
        sql_select = 'select * from news where source="%s"'%(source)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_keywords(self,keywords):
        # 假设 keywords 是一个由逗号分隔的关键词字符串
        # 清洗关键词并分割成列表
        keyword_list = [keyword.strip() for keyword in keywords.split(',')]
        # 使用 AND 连接所有关键词的条件
        conditions = [f"summary LIKE '%{keyword}%'" for keyword in keyword_list]
        sql_select = "SELECT * FROM news WHERE " + " AND ".join(conditions)

        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_country(self,country):
        sql_select = 'select * from news where country="%s"'%(country)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnews_by_level(self,level):
        sql_select = 'select * from news where level="%s"'%(level)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def selectnewsbyid(self,id):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT * FROM news WHERE id = %d"%id
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple[0]

    def get_row_count(self):
        sql_row_count = "select count(*) from news"
        print(sql_row_count)
        count = self.helper.specific(sql_row_count)
        print(count)
        return count[0][0]

    def select_path(self,keywords):
        sql_select_path = f"SELECT * FROM news WHERE title LIKE '%{keywords}%'"
        print(sql_select_path)
        nested_tuple = self.helper.specific(sql_select_path)
        print(nested_tuple)
        return nested_tuple

    def select_country(self):
        sql_select_country = "select DISTINCT country FROM news"
        print(sql_select_country)
        nested_tuple = self.helper.specific(sql_select_country)
        print(nested_tuple)
        return nested_tuple

    def delete_Data(self,row1,row2):
        sql_del = "delete from news where id between %d and %d"%(row1,row2)
        print(sql_del)
        self.helper.cud(sql_del)

    def update_Time(self,time,id):
        sql_del = 'update news set time = "%s" where id = %d'%(time,id)
        print(sql_del)
        self.helper.cud(sql_del)

    def delete_databytime(self,time):
        sql_del = 'delete from news where time = "%s"' % time
        print(sql_del)
        self.helper.cud(sql_del)

    def select_latest_time(self):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT time FROM news ORDER BY STR_TO_DATE(time, '%M %d, %Y') DESC LIMIT 1"
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple[0][0]

    def select_latest_time_by_source(self,source):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT time FROM news where source = '%s' ORDER BY STR_TO_DATE(time, '%%M %%d, %%Y') DESC LIMIT 1"%source
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple[0][0]

    def select_news_by_latest_time_by_source(self,source1,source2):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT * FROM news where source = '%s' and STR_TO_DATE(time, '%%M %%d, %%Y') =(SELECT MAX(STR_TO_DATE(time, '%%M %%d, %%Y')) from news where source = '%s')"%(source1,source2)
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def select_avg_nextday(self,source):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT avg(下一天) FROM news where source = '%s'"%source
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple[0][0]

    def select_num_papers(self,time):
        # 格式化日期时间对象为字符串，适合 SQL 查询
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT source,count(*) as count FROM news where release_time >= '%s' group by source"%formatted_time
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple

    def get_levelandcountry_bysource(self,source):
        # SELECT * FROM records WHERE source = 'THE WHITE HOUSE' AND time = 'JUNE 13, 2024';
        sql_select = "SELECT level,country from news where source = '%s' order by id limit 1"%source
        print(sql_select)
        nested_tuple = self.helper.specific(sql_select)
        print(nested_tuple)
        return nested_tuple[0]

# class Mysqlop(object):
#     def __init__(self):
#         self.TableName = 'test.defensenews'
#         self.helper = Mysql('localhost', 3306, 'test', 'root', '839993492', 'utf8')#host, port, [database, user, password]这三个改成自己的其他不用改, charset
#         self.helper.open()
#
#     def saveData(self,source, newstime, title, text):
#         #执行存入操作
#     	# sql = "INSERT INTO news (source, time, title, text) VALUES ('%s', '%s','%s', '%s')" % (source, time, title, text)
#         sql = "insert into defensenews (source,time,title,text) values ('%s','%s','%s','%s')"%(source,newstime,title,text)
#         # sql = "INSERT INTO news  VALUES (source, time, title, text)"
#         print(sql)
#         self.helper.cud(sql)
#     def closeFile(self):
#         self.helper.close()
#
#     def clearData(self):
#         sql_del = "delete from defensenews"
#         print(sql_del)
#         self.helper.cud(sql_del)
#     def getData(self,startrow,rownumber,column):
#         sql_get = "select %s"%column + " from defensenews limit %d,%d"%(startrow,rownumber)
#         print(sql_get)
#         nested_tuple = self.helper.specific(sql_get)
#         print(nested_tuple)
#         print(nested_tuple[0][0])
#         return nested_tuple[0][0]
