import mysql.connector

conn = mysql.connector.connect(
    host="localhost",       # hoặc IP máy chủ
    port=3306,              # cổng MySQL, thường là 3306
    user="root",            # tài khoản MySQL
    password="",  # mật khẩu
    database="qlsv"    # tên database
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM sinhvien")  # Thay 'sinhvien' bằng tên bảng bạn muốn truy vấn
for row in cursor.fetchall():
    print(row)

conn.close()