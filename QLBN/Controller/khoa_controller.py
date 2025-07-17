import tkinter as tk
from Model.khoa_model import KhoaModel
from View.khoa_view import KhoaView

class KhoaController:
    def __init__(self, root):
        self.model = KhoaModel()
        self.view = KhoaView(root, self)
        self.load_khoa()

    def load_khoa(self):
        ds = self.model.get_all_khoa()
        self.view.show_khoa(ds)
        self.view.clear_form()

    def add_khoa(self):
        data = self.view.get_form_data()
        if not data["ten_khoa"]:
            tk.messagebox.showerror("Lỗi", "Tên khoa không được để trống!")
            return
        if self.model.add_khoa(data["ten_khoa"]):
            tk.messagebox.showinfo("Thành công", "Thêm khoa thành công!")
            self.load_khoa()
        else:
            tk.messagebox.showerror("Lỗi", "Thêm khoa thất bại!")

    def update_khoa(self):
        khoa_id = self.view.get_selected_khoa_id()
        if not khoa_id:
            tk.messagebox.showwarning("Chưa chọn", "Vui lòng chọn khoa để cập nhật!")
            return
        data = self.view.get_form_data()
        if not data["ten_khoa"]:
            tk.messagebox.showerror("Lỗi", "Tên khoa không được để trống!")
            return
        if self.model.update_khoa(khoa_id, data["ten_khoa"]):
            tk.messagebox.showinfo("Thành công", "Cập nhật khoa thành công!")
            self.load_khoa()
        else:
            tk.messagebox.showerror("Lỗi", "Cập nhật khoa thất bại!")

    def delete_khoa(self):
        khoa_id = self.view.get_selected_khoa_id()
        if not khoa_id:
            tk.messagebox.showwarning("Chưa chọn", "Vui lòng chọn khoa để xóa!")
            return
        if self.view.confirm_delete(khoa_id):
            if self.model.delete_khoa(khoa_id):
                tk.messagebox.showinfo("Thành công", "Xóa khoa thành công!")
                self.load_khoa()
            else:
                tk.messagebox.showerror("Lỗi", "Xóa khoa thất bại!")

    def search_khoa(self):
        keyword = self.view.search_entry.get()
        if not keyword:
            self.load_khoa()
            return
        ds = self.model.search_khoa(keyword)
        self.view.show_khoa(ds)

