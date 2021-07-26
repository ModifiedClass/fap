from sqlalchemy.sql.expression import false
from .base import db
import pymysql

class ExecuteSql:
    __sql=''
    __params={}
    __type=False

    def __init__(self,sql,params,type=False):
        self.__sql=sql
        self.__params=params
        self.__type=type

    def exec(self):
        cursor = db.session.execute(self.__sql,self.__params)
        try:
            if self.__type:
                db.session.commit()
                return {}
            else:
                return cursor.fetchall()
        except Exception as e:
            raise e
    
# 查询
#cursor = db.session.execute('select * from users')
#result = cursor.fetchall()

# 添加
#cursor = db.session.execute('insert into users(name) values(:value)', params={"value": 'abc'})
#db.session.commit()
#print(cursor.lastrowid)

class OriginExecuteSql:
    __conn={}


    def __init__(self, db, host='127.0.0.1', port='3306', user='root', password='123456', charset='utf8'):
        self.__conn = pymysql.connect(host = host, port = port, user = user, password = password, db = db, charset = charset)


    def exec(self,sql,params,type=False,):
        cursor = self.__conn.cursor()
        try:
            if type:
                cursor.execute(sql, params)
                self.__conn.commit()
                return {}
            else:
                return cursor.fetchall()
        except Exception as e:
            self.__conn.rollback()
            raise e
        finally:
            cursor.close()
            self.__conn.close()

# sql = "INSERT INTO trade (name, account, saving) VALUES ( '%s', '%s', %.2f )"
# data = ('雷军', '13512345678', 10000)
# cursor.execute(sql,data)