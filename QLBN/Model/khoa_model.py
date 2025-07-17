from db.connect import get_connection
from Model.khoa_entity import khoa_entity
from typing import List, Dict

class KhoaModel:
    def __init__(self):
        self.connection = get_connection()
    def add_khoa(self, ten_khoa: str) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Khoa (ten_khoa) VALUES (%s)"
            cursor.execute(query, (ten_khoa,))
            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Loi khi them khoa:", e)
            return False
    def get_all_khoa(self) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Khoa"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except Exception as e:
            print("Loi khi lay danh sach khoa:", e)
            return []
    def get_khoa_id_by_name(self, ten_khoa: str) -> int:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return None

        try:
            cursor = self.connection.cursor()
            query = "SELECT khoa_id FROM Khoa WHERE ten_khoa = %s"
            cursor.execute(query, (ten_khoa,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None

        except Exception as e:
            print("Loi khi tim khoa theo ten:", e)
            return None
    # Cập nhật thông tin khoa
    def update_khoa(self, khoa: khoa_entity) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Khoa
                SET ten_khoa = %s
                WHERE khoa_id = %s
            """
            cursor.execute(query, (khoa.ten_khoa, khoa.khoa_id))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi cap nhat khoa:", e)
            return False
    # Xóa khoa theo ID
    def delete_khoa(self, khoa_id: int) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Khoa WHERE khoa_id = %s"
            cursor.execute(query, (khoa_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi xoa khoa:", e)
            return False
    # Tìm kiếm khoa theo tên
    def search_khoa(self, keyword: str):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Khoa WHERE ten_khoa LIKE %s"
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Lỗi khi tìm kiếm khoa:", e)
            return []