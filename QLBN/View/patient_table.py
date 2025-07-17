import tkinter as tk
from tkinter import ttk

class PatientTable(tk.Frame):
    def __init__(self, master, on_select_callback):
        super().__init__(master)

        columns = (
            "ID", "Họ tên", "Giới tính", "Ngày sinh", "Địa chỉ", "SĐT",
            "Nhập viện", "Ra viện", "Chẩn đoán", "Khoa"
        )

        # Treeview
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")  # Cố định chiều rộng ban đầu

        # Scrollbar dọc
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Scrollbar ngang
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Gắn sự kiện chọn
        self.tree.bind("<<TreeviewSelect>>", on_select_callback)

    # Hiển thị danh sách bệnh nhân
    def show_patients(self, patients):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in patients:
            self.tree.insert("", "end", values=(
                p["benhnhan_id"], p["ho_ten"], p["gioi_tinh"], p["ngay_sinh"], p["dia_chi"], p["so_dien_thoai"],
                p["ngay_nhap_vien"], p["ngay_ra_vien"], p["chan_doan"], p["khoa_id"]
            ))
    # Lấy ID bệnh nhân đã chọn
    def get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return item["values"][0]
    
    # Lấy giá trị của hàng đã chọn
    def get_selected_row_values(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]
