import tkinter as tk
from tkinter import messagebox
from View.patient_form import PatientForm
from View.patient_table import PatientTable

class PatientView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill="both", expand=True)
        # thanh tìm kiếm 
         # Thanh tìm kiếm
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="Tìm kiếm:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Tìm kiếm", command=self.controller.search_patient).pack(side="left")

        # Form nhập
        self.form = PatientForm(self)
        self.form.pack(fill="x", padx=10, pady=5)

        # Bảng danh sách
        self.table = PatientTable(self, self.on_select)
        self.table.pack(fill="both", expand=True, padx=10, pady=5)

        # Nút chức năng
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Thêm", command=self.controller.add_patient).pack(side="left")
        tk.Button(btn_frame, text="Cập nhật", command=self.controller.update_patient).pack(side="left")
        tk.Button(btn_frame, text="Xóa", command=self.controller.delete_patient).pack(side="left")
        tk.Button(btn_frame, text="Làm mới", command=self.controller.load_patients).pack(side="left")

    # Giao tiếp với controller

    # Lấy dữ liệu từ form
    def get_form_data(self):
        return self.form.get_data()
    # Set dữ liệu vào form
    def set_form_data(self, data):
        self.form.set_data(data)
    # Clear form
    def clear_form(self):
        self.form.clear()
    # Hiển thị danh sách bệnh nhân
    def show_patients(self, patients):
        self.table.show_patients(patients)
    # Lấy ID bệnh nhân đã chọn
    def get_selected_patient_id(self):
        return self.table.get_selected_id()
    # Xử lý sự kiện chọn bệnh nhân
    def on_select(self, event):
        row = self.table.get_selected_row_values()
        if row:
            keys = ["name", "gender", "ngaysinh", "diachi", "sdt", "ngaynhapvien", "ngayravien", "chuandoan", "khoa"]
            data = {k: row[i+1] for i, k in enumerate(keys)}  # ID là row[0]
            self.set_form_data(data)
            
    # Xác nhận xóa bệnh nhân
    def confirm_delete(self, patient_id):
        return messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bệnh nhân ID {patient_id}?")
