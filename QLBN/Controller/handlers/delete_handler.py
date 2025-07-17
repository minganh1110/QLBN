import tkinter as tk

def handle_delete_patient(view, model):
    patient_id = view.get_selected_patient_id()
    if not patient_id:
        tk.messagebox.showwarning("Chưa chọn", "Vui lòng chọn bệnh nhân để xóa!")
        return False

    if view.confirm_delete(patient_id):
        if model.delete_patient(patient_id):
            tk.messagebox.showinfo("Thành công", "Xóa bệnh nhân thành công!")
            return True
        else:
            tk.messagebox.showerror("Lỗi", "Xóa thất bại!")
            return False
    return False
