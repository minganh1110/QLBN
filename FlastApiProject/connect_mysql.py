import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',   # đổi
            database='qltk'    # đổi
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None
