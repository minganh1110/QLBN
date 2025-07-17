import tkinter as tk
from tkinter import ttk
from Model.khoa_model import KhoaModel

class PatientForm(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Thông tin bệnh nhân")
        self.entries = {}
        self.khoa_map = {}          # ánh xạ tên khoa → id
        self.khoa_map_reverse = {}  # ánh xạ id → tên khoa
        self.create_form()

    def create_form(self):
        labels = [
            ("Họ tên", "name"),
            ("Giới tính", "gender"),
            ("Ngày sinh", "ngaysinh"),
            ("Địa chỉ", "diachi"),
            ("SĐT", "sdt"),
            ("Ngày nhập viện", "ngaynhapvien"),
            ("Ngày ra viện", "ngayravien"),
            ("Chẩn đoán", "chuandoan")
        ]

        for i, (label, key) in enumerate(labels):
            tk.Label(self, text=label).grid(row=i//2, column=(i % 2) * 2, sticky="w", padx=5, pady=2)
            entry = tk.Entry(self)
            entry.grid(row=i//2, column=(i % 2) * 2 + 1, padx=5, pady=2)
            self.entries[key] = entry

        # Combobox cho Khoa
        tk.Label(self, text="Khoa").grid(row=4, column=0, sticky="w", padx=5, pady=2)

        khoa_model = KhoaModel()
        ds_khoa = khoa_model.get_all_khoa()

        khoa_names = []
        for k in ds_khoa:
            ten = k['ten_khoa']
            ma = k['khoa_id']
            self.khoa_map[ten] = ma
            self.khoa_map_reverse[ma] = ten
            khoa_names.append(ten)

        khoa_cb = ttk.Combobox(self, values=khoa_names, state="readonly")
        khoa_cb.grid(row=4, column=1, padx=5, pady=2)
        self.entries["khoa"] = khoa_cb

    # Lấy dữ liệu từ form (trả về khoa_id)
    def get_data(self):
        data = {k: e.get() for k, e in self.entries.items()}
        ten_khoa = data.get("khoa")
        data["khoa"] = self.khoa_map.get(ten_khoa)
        return data

    # Gán dữ liệu vào form
    def set_data(self, data):
        for k, v in data.items():
            if k not in self.entries:
                continue
            if k == "khoa":
                ten_khoa = self.khoa_map_reverse.get(v, "")
                self.entries[k].set(ten_khoa)
            else:
                self.entries[k].delete(0, tk.END)
                self.entries[k].insert(0, v if v else "")

    # Xóa trắng form
    def clear(self):
        for k, e in self.entries.items():
            if k == "khoa":
                e.set("")
            else:
                e.delete(0, tk.END)
