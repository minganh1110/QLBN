import tkinter as tk
from Model.patient_model import PatientModel
from Model.khoa_model import KhoaModel
from View.patient_view import PatientView
from Controller.handlers.add_handler import handle_add_patient
from Controller.handlers.update_handler import handle_update_patient
from Controller.handlers.delete_handler import handle_delete_patient

class PatientController:
    def __init__(self, root):
        self.model = PatientModel()
        self.khoa_model = KhoaModel()
        self.view = PatientView(root, self)
        self.load_patients()

    # Tìm kiếm bệnh nhân
    def search_patient(self):
        keyword = self.view.search_entry.get()
        if not keyword:
            self.load_patients()
            return
        ds = self.model.search_patient(keyword)
        self.view.show_patients(ds)
    # Tải danh sách bệnh nhân từ model và hiển thị lên view
    def load_patients(self):
        ds = self.model.get_all_patients()
        self.view.show_patients(ds)
        self.view.clear_form()


    # Thêm bệnh nhân mới
    def add_patient(self):
        if handle_add_patient(self.view, self.model, self.khoa_model):
            self.load_patients()


    # Cập nhật thông tin bệnh nhân
    def update_patient(self):
        if handle_update_patient(self.view, self.model, self.khoa_model):
            self.load_patients()


            
    # Xóa bệnh nhân đã chọn
    def delete_patient(self):
        if handle_delete_patient(self.view, self.model):
            self.load_patients()
