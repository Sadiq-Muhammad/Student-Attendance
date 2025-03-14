#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customtkinter import CTkToplevel, CTkTextbox, CTkLabel
from awesometkinter.bidirender import add_bidi_support
from utils.global_variable import Arial
from utils.database import DatabaseManager
from datetime import datetime

DB = DatabaseManager()

class WinAttendanceDetail(CTkToplevel):
    def __init__(self, student_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("تفاصيل الحضور")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        
        # Fetch attendance history
        history = DB.get_student_attendance_history(student_id=student_id)
        
        # Title label
        title_label = CTkLabel(self, text="سجل الحضور", font=Arial(16))
        title_label.pack(pady=10)

        # Create a scrollable text widget
        text_box = CTkTextbox(self, width=380, height=300, wrap="none")
        text_box.pack(pady=10, padx=10, fill="both", expand=True)

        # Add data to the text box
        for session_id, status, scan_time in history:
            formatted_time = None
            if scan_time != None:
                # Convert scan_time from ISO format to "YYYY-M-D : h:mm AM/PM"
                formatted_time = datetime.fromisoformat(scan_time).strftime("%Y-%m-%d : %I:%M %p")
            else:
                formatted_time = ""
            record_text = f"{formatted_time} : الوقت"  + " | " + f"{status} : الحالة" + "\n"
            add_bidi_support(text_box, record_text)  # Right-to-left support for Arabic
            text_box.insert("end", record_text)
        
        text_box.configure(state="disabled")  # Make text read-only
