# jwt_handler.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "nguyenminhanh"  # Chuỗi bí mật để ký token
ALGORITHM = "HS256"                  # Thuật toán mã hóa
ACCESS_TOKEN_EXPIRE_MINUTES = 60    # Token sẽ hết hạn sau 60 phút

# hàm để tao token truy cập
def create_access_token(data: dict):
    to_encode = data.copy() # Sao chép dữ liệu đầu vào (ví dụ {"sub": "admin"})
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Tính thời gian hết hạn
    to_encode.update({"exp": expire})# Thêm thời gian hết hạn vào token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ham để giải mã token truy cập
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])# Giải mã token
        return payload # trả về dữ liệu đã giải mã
    except JWTError:
        return None
