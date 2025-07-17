import tkinter as tk
from tkinter import ttk, messagebox

class KhoaView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Thanh tìm kiếm
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="Tìm kiếm khoa:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Tìm kiếm", command=self.controller.search_khoa).pack(side="left")

        # Form nhập thông tin khoa
        form = tk.LabelFrame(self, text="Thông tin khoa")
        form.pack(fill="x", padx=10, pady=5)
        tk.Label(form, text="Tên khoa:").grid(row=0, column=0)
        self.ten_khoa_entry = tk.Entry(form)
        self.ten_khoa_entry.grid(row=0, column=1)

        # Nút chức năng
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Thêm", command=self.controller.add_khoa).pack(side="left")
        tk.Button(btn_frame, text="Cập nhật", command=self.controller.update_khoa).pack(side="left")
        tk.Button(btn_frame, text="Xóa", command=self.controller.delete_khoa).pack(side="left")
        tk.Button(btn_frame, text="Làm mới", command=self.controller.load_khoa).pack(side="left")

        # Bảng danh sách khoa
        self.tree = ttk.Treeview(self, columns=("ID", "Tên khoa"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def get_form_data(self):
        return {
            "ten_khoa": self.ten_khoa_entry.get()
        }

    def set_form_data(self, data):
        self.ten_khoa_entry.delete(0, tk.END)
        self.ten_khoa_entry.insert(0, data.get("ten_khoa", ""))

    def clear_form(self):
        self.ten_khoa_entry.delete(0, tk.END)

    def show_khoa(self, ds_khoa):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for k in ds_khoa:
            self.tree.insert("", "end", values=(k["khoa_id"], k["ten_khoa"]))

    def get_selected_khoa_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return item["values"][0]

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item["values"]
        self.ten_khoa_entry.delete(0, tk.END)
        self.ten_khoa_entry.insert(0, vals[1])

    def confirm_delete(self, khoa_id):
        return messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa khoa ID {khoa_id}?")