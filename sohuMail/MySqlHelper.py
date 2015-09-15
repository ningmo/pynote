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