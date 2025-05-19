import mysql.connector

def get_mysql_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Adm123@',
        database='bonin'
    )