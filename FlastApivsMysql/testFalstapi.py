from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi origin (có thể thay bằng domain cụ thể)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mô hình dữ liệu (tuỳ bảng)
class Item(BaseModel):
    masv: int
    hoten: str
    tuoi: int

# Hàm kết nối MySQL
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='qlsv'  # Thay 'qlsv' bằng tên database của bạn
    )

# API GET dữ liệu từ bảng
@app.get("/items", response_model=List[Item])
def get_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT masv, hoten, tuoi FROM sinhvien")  # Thay 'sinhvien' bằng tên bảng bạn muốn truy vấn
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result