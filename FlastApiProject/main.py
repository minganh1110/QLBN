# main.py
from fastapi import FastAPI, HTTPException, Depends,Query
from pydantic import BaseModel
from connect_mysql import get_connection
from jwt_handler import create_access_token, decode_access_token
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests 
app = FastAPI()

# CORS cho phép gọi từ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Model dữ liệu ====
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    gmail: str



security = HTTPBearer()  # Middleware cho token

# ==== API: Đăng nhập ====
@app.post("/login")
def login(request: LoginRequest):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Không kết nối được MySQL!")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tlb_user WHERE user_name=%s AND password=%s",
                       (request.username, request.password))
        user = cursor.fetchone()

        if user:
            token = create_access_token({"sub": user["user_name"]})
            return {
                "message": "✅ Đăng nhập thành công!",
                "access_token": token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="❌ Sai tài khoản hoặc mật khẩu!")
    finally:
        cursor.close()
        conn.close()

# ==== API: Đăng ký ====
@app.post("/register")
def register(request: RegisterRequest):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Không kết nối được MySQL!")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tlb_user WHERE user_name=%s", (request.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Tên tài khoản đã tồn tại!")

        cursor.execute("INSERT INTO tlb_user (user_name, password, gmail) VALUES (%s, %s, %s)",
                       (request.username, request.password, request.gmail))
        conn.commit()
        return {"message": "🎉 Đăng ký thành công!"}
    finally:
        cursor.close()
        conn.close()

# ==== API: Xác thực token (dành cho home.html/admin.html) ====
@app.get("/profile")
def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):# Nhận token từ header Authorization
    token = credentials.credentials # Lấy token từ header Authorization
    payload = decode_access_token(token)# Giải mã token
    if not payload:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc hết hạn")

    return {"username": payload["sub"]}# Trả về thông tin người dùng từ token
# ==== API: lay category ====
# Model trả về
# Model dùng khi gửi dữ liệu từ client (POST, PUT)
class CategoryCreate(BaseModel):
    madanhmuc: int
    TenDanhMuc: str
    img_url: str
    mota: str

# Model dùng khi trả dữ liệu cho client (GET)
class Category(CategoryCreate):
    id: int

@app.get("/category", response_model=list[Category])
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, TenDanhMuc, img_url, madanhmuc,mota FROM tbl_category")  
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "TenDanhMuc": r[1], "img_url": r[2],"madanhmuc": r[3],"mota": r[4] } for r in rows]
#==== API them moi category ====
@app.post("/category")
def create_category(category: CategoryCreate):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_category (madanhmuc, TenDanhMuc, img_url, mota) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (category.madanhmuc, category.TenDanhMuc, category.img_url, category.mota))
    conn.commit()
    conn.close()
    return {"message": "Đã thêm danh mục thành công"}

#==== API Sua category ====
@app.put("/category/{id}")
def update_category(id: int, category: CategoryCreate):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE tbl_category SET madanhmuc=%s, TenDanhMuc=%s, img_url=%s, mota=%s WHERE id=%s"
    cursor.execute(sql, (category.madanhmuc, category.TenDanhMuc, category.img_url, category.mota, id))
    conn.commit()
    conn.close()
    return {"message": "Đã cập nhật danh mục thành công"}
#==== API Xoa category ====
@app.delete("/category/{id}")
def delete_category(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_category WHERE id=%s"
    cursor.execute(sql, (id,))
    conn.commit()
    conn.close()
    return {"message": "Đã xóa danh mục thành công"}



#==== api lay san pham ====

class Product(BaseModel):
    id: int
    id_category: int
    nameprd: str
    img_urlprd: str
    maprd: int
    quantity: int
    price: int
    des: str
    

@app.get("/products", response_model=list[Product])
def get_products_by_category(categoryId: int = Query(..., alias="categoryId")):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, nameprd, price, quantity, img_urlprd, id_category, maprd, des FROM tbl_product WHERE id_category = %s"
    cursor.execute(sql, (categoryId,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "nameprd": r[1],
            "price": r[2],
            "quantity": r[3],
            "img_urlprd": r[4],
            "id_category": r[5],
            "maprd": r[6],
            "des": r[7]
        } for r in rows
    ]
 #==== API đăng nhập bằng Google ====
