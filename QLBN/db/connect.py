import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',   
            database='qlbn'   
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Lỗi kết nối MySQL:", e)
        return None

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Kết nối thành công!")
        conn.close()
    except Exception as e:
        print("Lỗi khi kết nối:", e)