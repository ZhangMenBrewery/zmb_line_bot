import sqlite3
# import psycopg2
import MySQLdb

sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# pg_conn = psycopg2.connect(
#     dbname ='zmb_line_bot',
#     user = 'zhangmen',
#     password = '54685508',
#     host='192.168.60.12',
#     port = '5432'
# )

# pg_cursor = pg_conn.cursor()

mysql_conn = MySQLdb.connect(host='zhangmen.mysql.pythonanywhere-services.com', user='zhangmen', passwd='@Zmb54685508', db='zhangmen$zmb_line_bot')
mysql_cursor = mysql_conn.cursor()

sqlite_cursor.execute("SELECT * FROM mybot_beer")
# sqlite_cursor.execute("SELECT * FROM mybot_can")
rows = sqlite_cursor.fetchall()

for row in rows:
    row = tuple(item.replace('"', '') if isinstance(item, str) else item for item in row)
    row = tuple('' if item is None else item for item in row)
    # pg_cursor.execute('INSERT INTO callback_can ("id","time","eName","cName","ABV","NT_330ml","Description","image_url","order_url","order_text") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)
    # pg_cursor.execute('INSERT INTO callback_beer (id,"tapNum",time,"Style","eName","cName","Keyword","ABV","IBU","SRM","NT_29L","NT_330ml","AwardRecord","Malt","Hop","Adj","Feature","Description") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)
    # insert_query = f"INSERT INTO callback_can VALUES ({', '.join(['%s' for _ in row])})"
    # mysql_cursor.execute(insert_query, row)
    mysql_cursor.execute('INSERT INTO callback_beer (id,tapNum,time,Style,eName,cName,Keyword,ABV,IBU,SRM,NT_29L,NT_330ml,AwardRecord,Malt,Hop,Adj,Feature,Description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)

# pg_conn.commit()
mysql_conn.commit()

sqlite_cursor.close()
sqlite_conn.close()
# pg_cursor.close()
# pg_conn.close()
mysql_cursor.close()
mysql_conn.close()