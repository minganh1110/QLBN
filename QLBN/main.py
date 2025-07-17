import tkinter as tk
from Controller.patient_controller import PatientController
from Controller.khoa_controller import KhoaController

def open_patient_manager():
    win = tk.Toplevel(root)
    win.title("Quản Lý Bệnh Nhân")
    PatientController(win)

def open_khoa_manager():
    win = tk.Toplevel(root)
    win.title("Quản Lý Khoa")
    KhoaController(win)

root = tk.Tk()
root.title("Hệ thống Quản Lý Bệnh Viện")

frame = tk.Frame(root)
frame.pack(padx=30, pady=30)

tk.Label(frame, text="Chọn chức năng quản lý:", font=("Arial", 14)).pack(pady=10)
tk.Button(frame, text="Quản lý bệnh nhân", width=25, command=open_patient_manager).pack(pady=10)
tk.Button(frame, text="Quản lý khoa", width=25, command=open_khoa_manager).pack(pady=10)

root.mainloop()