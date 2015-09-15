#-*- coding:utf-8 -*-
import MySQLdb

class MySqlHelper:
    @staticmethod
    def FetchSql(host, user, password, database, sql, port=3306):
        try:
            conn = MySQLdb.connect (host=host,
                                    user=user,
                                    passwd=password,
                                    db=database, 
                                    charset="utf8")
            cursor = conn.cursor ()
            cursor.execute (sql)
            rows = cursor.fetchall ()
            cursor.close ()
            conn.close ()
            return rows
        except Exception,what:
            print "Error in ExecuteSql:%s" % sql
            raise what
    @staticmethod
    def ExecuteSql(host, user, password, database, sql, port=3306):
        try:
            conn = MySQLdb.connect (host=host, user=user, passwd=password, db=database, charset="utf8")
            cursor = conn.cursor ()
            rows = cursor.execute (sql)
            cursor.close ()
            conn.close ()
            return rows
        except Exception,what:
            print "Error in ExecuteSql:%s" % sql
            raise what