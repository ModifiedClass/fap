#安装cx_Oracle，并且需要安装Oracle Client
#https://www.oracle.com/database/technologies/instant-client/downloads.html
#https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html
#版本对应 例如cx_Oracle-5.2-11g.win32-py3.4 对应 python3.4 对应 instantclient-basic-win32-11.2.0.1.0 11G
'''
import cx_Oracle


class OriginExecuteSqlOne:
    __conn={}

    def __init__(self, conn="wbjkzy/his@192.168.100.120:1521/orcl"):
        self._conn = cx_Oracle.connect(conn)


    def exec(self,sql,params,type=False):
        cursor = self.__conn.cursor()
        try:
            if type:
                cursor.execute(sql, params)
                self.__conn.commit()
                return {}
            else:
                return cursor.fetchall()
        except Exception as e:
            self._conn.rollback()
            raise e
        finally:
            cursor.close()
            self.__conn.close()



class OriginExecuteSqlTwo:
    __conn={}

    def __init__(self, host,port,instance,user,password):
        # conn={'u':'zlhis','p':'z2ohis','host':'192.168.100.120','port':'1521','instance':'orcl'}
        self.__conn = cx_Oracle.connect(user, password,cx_Oracle.makedsn(host, port,instance))


    def exec(self,sql,params,type=False):
        cursor = self.__conn.cursor()
        try:
            if type:
                #单行参数
                # select * from table where params=:0 and params=:1
                # params=[param1,param2]
                cursor.execute(sql, params)
                #多行记录 insert params=[('TEST', 1, 'KERRY1'),('TEST', 2, 'KERRY2')]
                #cursor.executemany(sql, params)
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
'''