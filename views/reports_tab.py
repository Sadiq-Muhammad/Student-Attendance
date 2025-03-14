#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkComboBox, StringVar
from tkinter import ttk, messagebox
from awesometkinter.bidirender import add_bidi_support

from .win_attendance_detail import WinAttendanceDetail
from utils.global_variable import Arial
from utils.database import DatabaseManager

DB = DatabaseManager()

class ReportsTab(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.search_entry_var = StringVar()
        
        stages_options = ["المرحلة", "المرحلة الاولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة"]
        departments_options = ["القسم", "علوم الحاسوب", "نظم المعلومات", "انظمة طبية"]
        
        self.search_field = CTkEntry(self,textvariable=self.search_entry_var, justify="right", font=Arial(12))
        self.search_label = CTkLabel(self, text=": بحث", font=Arial(16))
        self.stage_combo = CTkComboBox(self, values=stages_options, font=Arial(12), justify="right", command=self.load_table)
        self.dep_combo = CTkComboBox(self, values=departments_options, font=Arial(12), justify="right", command=self.load_table)
        self.show_details_btn = CTkButton(self, text="عرض التفاصيل", font=Arial(12), command=self.openStudentDetails)
        
        
        columns = ("Absents", "Attendance","Name","ID")
        headings = ("الغياب", "الحضور", "اسم الطالب", "معرف الطالب")
        widths = (150, 200, 300, 150)
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=19)
        
        for col, heading, width in zip(columns, headings, widths):
            self.table.heading(col, text=heading, anchor='center')
            self.table.column(col, width=width, anchor='center')
        
        add_bidi_support(self.table)
        add_bidi_support(self.search_field)
        add_bidi_support(self.dep_combo)
        add_bidi_support(self.stage_combo)
        
        self.show_details_btn.grid(row=0, column=0, padx=10, pady=5)
        self.stage_combo.grid(row=0, column=1, padx=10, pady=5)
        self.dep_combo.grid(row=0, column=2, padx=10, pady=5)
        self.search_field.grid(row=0, column=3, padx=10, pady=5, ipady=3)
        self.search_label.grid(row=0, column=4, padx=10, pady=5)
        
        self.table.grid(row=2, column=0, columnspan=5, sticky="nsew")
        
        self.search_entry_var.trace_add("write", self.search_table)
    
    def search_table(self, name1, name2, op):
        if self.dep_combo.get() == "القسم" or self.stage_combo.get() == "المرحلة":
            messagebox.showerror("انتباه", ".يرجى اختيار القسم و المرحلة")
            return
        pattren = self.search_entry_var.get()
        self.table.delete(*self.table.get_children())
        students = DB.search_students_attendance_summary(pattren, self.dep_combo.get(), self.stage_combo.get())
        for student in students:
            self.table.insert('', 'end', values=(student[3], student[2], student[1], student[0]))
    
    def load_table(self, _):
        if self.dep_combo.get() == "القسم" or self.stage_combo.get() == "المرحلة":
            return
        self.table.delete(*self.table.get_children())
        students = DB.get_students_attendance_summary(self.dep_combo.get(), self.stage_combo.get())
        for student in students:
            self.table.insert('', 'end', values=(student[3], student[2], student[1], student[0]))
        
    def openStudentDetails(self):
        curItem = self.table.focus()
        
        if len(curItem) != 0:
            values = self.table.item(curItem)['values']
            self.editStudent_window = WinAttendanceDetail(student_id=values[-1])
            self.editStudent_window.wm_transient(self)
        else:
            messagebox.showerror("خطاء", ".الرجاء قم بأختيار طالب")