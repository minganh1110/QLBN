# model/patient_entity.py

from Model.person import Person
from typing import Optional

class Patient(Person):
    def __init__(
        self,
        name: str,
        gender: str,
        ngaysinh: str,
        diachi: str,
        sdt: str,
        benhnhan_id: Optional[int] = None,
        khoa_id: Optional[int] = None,
        ngaynhapvien: Optional[str] = None,
        ngayravien: Optional[str] = None,
        chuandoan: Optional[str] = None
    ):
        super().__init__(name, gender, ngaysinh, diachi, sdt)
        self.benhnhan_id = benhnhan_id
        self.khoa_id = khoa_id
        self.ngaynhapvien = ngaynhapvien
        self.ngayravien = ngayravien
        self.chuandoan = chuandoan
