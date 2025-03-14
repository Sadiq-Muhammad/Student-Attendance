#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkComboBox
from tkinter import ttk, messagebox
from awesometkinter.bidirender import add_bidi_support
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

from utils.global_variable import Arial
from utils.database import DatabaseManager
from utils.qrcode import generate_student_qr_code

DB = DatabaseManager()

class WinStudentTemplate(CTkToplevel):
    def __init__(self, mode: str, student_id: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False,False)
        self.mode = mode
        self.title("اضافة طالب" if mode=="add" else "تعديل طالب")
        self.columnconfigure(0, weight=1)
        
        stages_options = ["المرحلة الاولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة"]
        departments_options = ["علوم الحاسوب", "نظم المعلومات", "انظمة طبية"]
        
        submit_text = "إضافة" if mode=="add" else "تعديل"
        
        self.voice_input = CTkButton(self, width=200, text="إدخال صوتي", font=Arial(16), command=self.speech_to_text)
        self.name_field = CTkEntry(self, width=200, justify="right", font=Arial(12))
        self.name_label = CTkLabel(self, text=": أسم الطالب", font=Arial(16))
        self.dep_combo = CTkComboBox(self, width=200, values=departments_options, font=Arial(12), justify="right")
        self.dep_label = CTkLabel(self, text=": القسم", font=Arial(16))
        self.stage_combo = CTkComboBox(self, width=200, values=stages_options, font=Arial(12), justify="right")
        self.stage_label = CTkLabel(self, text=": المرحلة", font=Arial(16))
        self.submit_btn = CTkButton(self, width=200, text=submit_text, font=Arial(16), command=self.submit)

        add_bidi_support(self.name_field)
        add_bidi_support(self.stage_combo)
        add_bidi_support(self.dep_combo)
        
        if mode != "add":
            student = DB.get_student(student_id=student_id)
            self.name_field.insert(0, student[1])
            self.dep_combo.set(student[2])
            self.stage_combo.set(student[3])

        self.voice_input.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.name_field.grid(row=1, column=0, padx=10, pady=5)
        self.name_label.grid(row=1, column=1, padx=10, pady=5)
        self.dep_combo.grid(row=2, column=0, padx=10, pady=5)
        self.dep_label.grid(row=2, column=1, padx=10, pady=5)
        self.stage_combo.grid(row=3, column=0, padx=10, pady=5)
        self.stage_label.grid(row=3, column=1, padx=10, pady=5)
        self.submit_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    
    def submit(self):
        if self.mode=="add":
            try:
                student_id = DB.add_student(full_name=self.name_field.get(), department=self.dep_combo.get(), stage=self.stage_combo.get())
                qrcode_str = "QR" + str(student_id)
                generate_student_qr_code(self.name_field.get(), qrcode_str)
                DB.update_student(student_id=student_id, qr_code=qrcode_str)
                messagebox.showinfo("نجاح", ".تم إضافة الطالب و انشاء الكود الخاص به في ملف اكواد الطلبة على سطح المكتب")
            except:
                messagebox.showerror("خطاء", "حدث الخطاء في عملية إضافة الطالب")
        else:
            try:
                DB.update_student(full_name=self.name_field.get(), department=self.dep_combo.get(), stage=self.stage_combo.get())
                messagebox.showinfo("نجاح", ".تم تعديل معلومات الطالب بنجاح")
            except:
                messagebox.showerror("خطاء", "حدث الخطاء في عملية تعديل معلومات الطالب")
    
    def speech_to_text(self):
        recognizer = Recognizer()
        with Microphone() as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='ar-SA')
                self.name_field.insert(0, text)
            except UnknownValueError:
                messagebox.showerror("خطاء", "Google Speech Recognition could not understand audio")
            except RequestError as e:
                messagebox.showerror("خطاء", f"Could not request results from Google Speech Recognition service; {e}")