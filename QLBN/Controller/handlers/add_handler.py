import tkinter as tk
from Model.patient_entity import Patient

def handle_add_patient(view, model, khoa_model):
    data = view.get_form_data()

    # Kiểm tra người dùng có chọn khoa không
    if not data['khoa']:
        tk.messagebox.showerror("Lỗi", "Vui lòng chọn khoa trước khi thêm!")
        return False

    # Tìm khoa_id tương ứng
    khoa_list = khoa_model.get_all_khoa()
    khoa_id = None
    for k in khoa_list:
        if (k['khoa_id']) == data['khoa'] or k['ten_khoa'] == data['khoa']:
            khoa_id = k['khoa_id']
            break
            

    if khoa_id is None:
        tk.messagebox.showerror("Lỗi", f"Khoa '{data['khoa']}' không hợp lệ.")
        return False

    patient = Patient(
        name=data['name'],
        gender=data['gender'],
        ngaysinh=data['ngaysinh'],
        diachi=data['diachi'],
        sdt=data['sdt'],
        ngaynhapvien=data['ngaynhapvien'],
        ngayravien=data['ngayravien'],
        chuandoan=data['chuandoan'],
        khoa_id=khoa_id,
        benhnhan_id=None
    )

    if model.add_patient(patient):
        tk.messagebox.showinfo("Thành công", "Thêm bệnh nhân thành công!")
        return True
    else:
        tk.messagebox.showerror("Lỗi", "Thêm bệnh nhân thất bại!")
        return False
