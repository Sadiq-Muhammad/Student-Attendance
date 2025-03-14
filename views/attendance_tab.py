#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image
from pyzbar.pyzbar import decode

from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage
from tkinter import messagebox
from awesometkinter.bidirender import add_bidi_support

from utils.database import DatabaseManager
from utils.global_variable import Arial
from utils.email import send_department_email

DB = DatabaseManager()

class AttendanceTab(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.session = "start"  # "start" means not scanning; "end" means scanning is active.
        self.session_id = None
        self.camera_active = False
        self.cap = None  # Will hold the VideoCapture object
        
        self.start_end_session_btn = CTkButton(self, text="ابداء تسجيل الحضور", font=Arial(26), command=self.start_end_session)
        self.start_end_session_btn.pack()
        
        # Create a label widget for showing the camera feed.
        # Initially hidden.
        self.camera_label = CTkLabel(self, text="")
        
        # Upload button placed below the camera widget
        self.upload_image_btn = CTkButton(self, text="اختر صورة من الجهاز", font=Arial(24), command=self.upload_image)
        
        self.student_name_label = CTkLabel(self, text="", text_color="green", font=Arial(22))
        self.student_name_label.pack(pady=5)
        
        add_bidi_support(self.start_end_session_btn)
        add_bidi_support(self.student_name_label)
    
    def start_end_session(self):
        if self.session == "start":
            # Start scanning session: update state, show upload button and camera widget.
            self.session = "end"
            self.session_id = DB.start_attendance_session()
            self.start_end_session_btn.configure(text="إنهاء تسجيل الحضور")
            self.camera_label.pack()
            self.upload_image_btn.pack(pady=5)
            self.start_camera()
        else:
            # End scanning session: update state and hide camera widget and upload button.
            self.session = "start"
            DB.end_attendance_session(session_id=self.session_id)
            result = send_department_email(session_id=self.session_id)
            self.start_end_session_btn.configure(text="ابداء تسجيل الحضور")
            self.student_name_label.configure(text="")
            self.camera_label.pack_forget()
            self.upload_image_btn.pack_forget()
            self.stop_camera()
            messagebox.showinfo("انتباه", result)
    
    def start_camera(self):
        # Open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("خطاء", ".لا يمكن فتح الكامرة")
            return
        self.camera_active = True
        self.update_camera()  # start updating the camera feed in the widget
    
    def stop_camera(self):
        self.camera_active = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def update_camera(self):
        if not self.camera_active:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("خطاء", ".فشل في الحصول على الاطار")
            self.after(30, self.update_camera)
            return
        
        # Detect QR code using OpenCV's QRCodeDetector
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            self.student_name_label.configure(text=DB.mark_attendance(session_id=self.session_id, qr_code=data))
        
        # Convert frame from BGR to RGB and then to a PIL image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        
        desired_size = (320, 240)
        resized_image = pil_image.resize(desired_size, Image.LANCZOS)
        
        # Create a CTkImage from the PIL image.
        # Note: You can adjust the size parameter as needed.
        ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=desired_size)
        
        # Update the label with the new image. Save a reference to avoid garbage collection.
        self.camera_label.configure(image=ctk_image)
        self.camera_label.ctk_image = ctk_image
        
        # Schedule the next frame update.
        self.after(30, self.update_camera)
    
    def upload_image(self):
        # Open file dialog to choose an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return  # no file selected
        
        # Open the image using PIL and convert it to OpenCV format
        pil_image = Image.open(file_path).convert("RGB")
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Use pyzbar to decode QR codes in the image
        decoded_objs = decode(open_cv_image)
        if decoded_objs:
            for obj in decoded_objs:
                qr_text = obj.data.decode('utf-8')
                self.student_name_label.configure(text=DB.mark_attendance(session_id=self.session_id, qr_code=qr_text))
        else:
            # Fallback: try using OpenCV's QRCodeDetector
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(open_cv_image)
            if data:
                self.student_name_label.configure(text=DB.mark_attendance(session_id=self.session_id, qr_code=data))
            else:
                self.student_name_label.configure(text="لم يتم العثور على كود في الصورة المرفقة")

# Additional import needed for numpy conversion in upload_image
import numpy as np
