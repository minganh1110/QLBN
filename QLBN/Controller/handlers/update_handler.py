import tkinter as tk
from Model.patient_entity import Patient

def handle_update_patient(view, model, khoa_model):
    patient_id = view.get_selected_patient_id()
    if not patient_id:
        tk.messagebox.showwarning("Chưa chọn", "Vui lòng chọn bệnh nhân để cập nhật!")
        return False

    data = view.get_form_data()
    khoa_list = khoa_model.get_all_khoa()
    khoa_id = None
    for k in khoa_list:
        if str(k['khoa_id']) == data['khoa'] or k['ten_khoa'] == data['khoa']:
            khoa_id = k['khoa_id']
            break

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
        benhnhan_id=patient_id
    )

    if model.update_patient(patient):
        tk.messagebox.showinfo("Thành công", "Cập nhật bệnh nhân thành công!")
        return True
    else:
        tk.messagebox.showerror("Lỗi", "Cập nhật thất bại!")
        return False
