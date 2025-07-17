

from db.connect import get_connection
from Model.patient_entity import Patient
from typing import List, Dict


class PatientModel:
    def __init__(self):
        self.connection = get_connection()

    def add_patient(self, patient: Patient) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False

        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO ThongTinBenhNhan
                (ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai, khoa_id, ngay_nhap_vien, ngay_ra_vien, chan_doan)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient.name,
                patient.ngaysinh,
                patient.gender,
                patient.diachi,
                patient.sdt,
                patient.khoa_id,
                patient.ngaynhapvien,
                patient.ngayravien,
                patient.chuandoan
            ))
            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Loi khi them benh nhan:", e)
            return False

    def update_patient(self, patient: Patient) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False

        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE ThongTinBenhNhan
                SET ho_ten = %s,
                    ngay_sinh = %s,
                    gioi_tinh = %s,
                    dia_chi = %s,
                    so_dien_thoai = %s,
                    khoa_id = %s,
                    ngay_nhap_vien = %s,
                    ngay_ra_vien = %s,
                    chan_doan = %s
                WHERE benhnhan_id = %s
            """
            cursor.execute(query, (
                patient.name,
                patient.ngaysinh,
                patient.gender,
                patient.diachi,
                patient.sdt,
                patient.khoa_id,
                patient.ngaynhapvien,
                patient.ngayravien,
                patient.chuandoan,
                patient.benhnhan_id
            ))
            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Loi khi cap nhat benh nhan:", e)
            return False

    def get_all_patients(self) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM ThongTinBenhNhan"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print("Loi khi lay danh sach benh nhan:", e)
            return []
    def get_patient_by_id(self, patient_id: int) -> Patient:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return None
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM ThongTinBenhNhan WHERE benhnhan_id = %s"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                # Tạo đối tượng Patient từ dict result
                return Patient(
                    benhnhan_id=result.get("benhnhan_id"),
                    name=result.get("ho_ten"),
                    ngaysinh=result.get("ngay_sinh"),
                    gender=result.get("gioi_tinh"),
                    diachi=result.get("dia_chi"),
                    sdt=result.get("so_dien_thoai"),
                    khoa_id=result.get("khoa_id"),
                    ngaynhapvien=result.get("ngay_nhap_vien"),
                    ngayravien=result.get("ngay_ra_vien"),
                    chuandoan=result.get("chan_doan")
                )
            else:
                return None

        except Exception as e:
            print("Loi khi lay benh nhan theo ID:", e)
            return
        

        
    def delete_patient(self, patient_id: int) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM ThongTinBenhNhan WHERE benhnhan_id = %s"
            cursor.execute(query, (patient_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi xoa benh nhan:", e)
            return False
        
    def search_patient(self, keyword: str) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT * FROM ThongTinBenhNhan
                WHERE ho_ten LIKE %s OR dia_chi LIKE %s OR so_dien_thoai LIKE %s OR benhnhan_id LIKE %s
            """
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Loi khi tim kiem benh nhan:", e)
            return []


        
