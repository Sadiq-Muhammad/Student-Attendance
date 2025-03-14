#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customtkinter import CTk, CTkTabview, set_appearance_mode
from awesometkinter.bidirender import add_bidi_support

from .students_tab import StudentsTab
from .attendance_tab import AttendanceTab
from .reports_tab import ReportsTab
from utils.global_variable import *

set_appearance_mode("light")

class MainWin(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("تسجيل حضور الطلبة")  # Arabic title
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        # Center the window
        x = (SCREEN_WIDTH // 2) - (WIN_WIDTH // 2) - 100
        y = (SCREEN_HEIGHT // 2) - (WIN_HEIGHT // 2) - 100
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{x}+{y}")
        self.resizable(False, False)
        
        self.tab_view = CTkTabview(self, width=int(WIN_WIDTH * 0.95), height=int(WIN_HEIGHT * 0.95), border_width=5, text_color="#000000")
        add_bidi_support(self.tab_view)
        # Adding tabs
        self.tab_view.add("التقارير")
        self.tab_view.add("تسجيل الحضور")
        self.tab_view.add("قائمة الطلبة")
        
        self.tab_view.set("قائمة الطلبة")
        
        for button in self.tab_view._segmented_button._buttons_dict.values():
            button.configure(width=75, height=35, font=Arial(16),) #Change font using font object
            
        self.tab_view.menu_tab = StudentsTab(self.tab_view.tab("قائمة الطلبة"))
        self.tab_view.attendance_tab = AttendanceTab(self.tab_view.tab("تسجيل الحضور"))
        self.tab_view.reports_tab = ReportsTab(self.tab_view.tab("التقارير"))
        
        self.tab_view.menu_tab.pack()
        self.tab_view.attendance_tab.pack()
        self.tab_view.reports_tab.pack()
        
        self.tab_view.pack()
        
