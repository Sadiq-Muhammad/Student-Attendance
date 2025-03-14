#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, StringVar
from tkinter import ttk, messagebox
from awesometkinter.bidirender import add_bidi_support

from .win_student_template import WinStudentTemplate
from utils.global_variable import Arial
from utils.database import DatabaseManager

DB = DatabaseManager()

class StudentsTab(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.search_entry_var = StringVar()
        
        self.search_field = CTkEntry(self,textvariable=self.search_entry_var, justify="right", font=Arial(12))
        self.search_label = CTkLabel(self, text=": بحث", font=Arial(16))
        self.add_btn = CTkButton(self,text="اضافة", font=Arial(16), width=100, command=self.openAddStudentWindow)
        self.edit_btn = CTkButton(self,text="تعديل", font=Arial(16), width=100, command=self.openEditStudentWindow)
        self.delete_btn = CTkButton(self,text="حذف", font=Arial(16), width=100, command=self.delete_student)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", rowheight=30, font=Arial(14))
        style.configure("Treeview", rowheight=25)
        
        columns = ("Stage", "Dep","Name","ID")
        headings = ("المرحلة", "القسم", "اسم الطالب", "معرف الطالب")
        widths = (150, 200, 300, 150)
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=19)
        for col, heading, width in zip(columns, headings, widths):
            self.table.heading(col, text=heading, anchor='center')
            self.table.column(col, width=width, anchor='center')
        
        self.delete_btn.grid(row=0, column=0, padx=10, pady=5)
        self.edit_btn.grid(row=0, column=1, padx=10, pady=5)
        self.add_btn.grid(row=0, column=2, padx=10, pady=5)
        self.search_field.grid(row=0, column=3, padx=10, pady=5, ipady=3)
        self.search_label.grid(row=0, column=4, padx=10, pady=5)
        
        self.table.grid(row=2, column=0, columnspan=5, sticky="nsew")
        
        add_bidi_support(self.table)
        add_bidi_support(self.search_field)
        
        self.search_entry_var.trace_add("write", self.search_table)
        
        self.load_table()
    
    def search_table(self, name1, name2, op):
        pattren = self.search_entry_var.get()
        self.table.delete(*self.table.get_children())
        students = DB.search_students("%"+pattren+"%")
        for student in students:
            self.table.insert('', 'end', values=(student[3], student[2], student[1], student[0]))
    
    def load_table(self):
        self.table.delete(*self.table.get_children())
        students = DB.get_all_students()
        for student in students:
            self.table.insert('', 'end', values=(student[3], student[2], student[1], student[0]))
    
    def delete_student(self):
        curItem = self.table.focus()
        if len(curItem) != 0:
            res = messagebox.askyesno("انتباه", "هل انت متأكد من حذف هذا الطالب ؟")
            if res == False:
                return
            values = self.table.item(curItem)['values']
            DB.delete_student(values[-1])
            self.load_table()
        else:
             messagebox.showerror("خطاء", ".الرجاء قم بأختيار طالب")
        
    def openAddStudentWindow(self):
        self.addStudent_window = WinStudentTemplate(mode="add")
        self.addStudent_window.wm_transient(self)
        self.wait_window(self.addStudent_window)
        self.load_table()
    
    def openEditStudentWindow(self):
        curItem = self.table.focus()
        
        if len(curItem) != 0:
            values = self.table.item(curItem)['values']
            self.editStudent_window = WinStudentTemplate(mode="edit", student_id=values[-1])
            self.editStudent_window.wm_transient(self)
            self.wait_window(self.editStudent_window)
            self.load_table()
        else:
            messagebox.showerror("خطاء", ".الرجاء قم بأختيار طالب")