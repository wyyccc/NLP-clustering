import pymysql

def read_data(n = 1000):
    db = pymysql.connect(
    host = '172.18.128.127', 
    port = 3306,
    user = 'root',
    password = 'tc123321',  
    database = 'cls_data',  
    charset = 'utf8'
    )
    cursor = db.cursor()
    sql = "SELECT content FROM news_realtime LIMIT " + str(n)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    data = [i[0] for i in data]
    return data