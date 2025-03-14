import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .database import DatabaseManager

DB = DatabaseManager()

def send_department_email(session_id, sender_email="inferno1272000@gmail.com", sender_password="udke qoxv ezrm ipzp", recipient_email="sadmoe000@gmail.com"):
    """
    Sends an email with attendance information for a department and stage.
    
    Parameters:
        department (str): The department name.
        stage (str): The stage level.
        attendance_data (list of tuples): Each tuple contains (student_name, status) where status is 'present' or 'absent'.
        sender_email (str): The Gmail address to send from.
        sender_password (str): The password or app-specific password for the Gmail account.
        recipient_email (str): The recipient's email address.
    """
    department, stage, attendance_data = DB.get_attendance_data(session_id)
    
    # Create the message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"تقرير الحضور لقسم {department} - {stage}"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Build an HTML table for attendance data with RTL support
    html_table = """
    <table border="1" style="border-collapse: collapse; direction: rtl; text-align: right; width: 100%;">
    <tr>
        <th style="padding: 8px; text-align: right;">اسم الطالب</th>
        <th style="padding: 8px; text-align: right;">الحالة</th>
    </tr>
    """
    for student_name, status in attendance_data:
        html_table += f"""
    <tr>
        <td style="padding: 8px; text-align: right;">{student_name}</td>
        <td style="padding: 8px; text-align: right;">{status}</td>
    </tr>
        """
    html_table += "</table>"

    # Create the HTML content for the email with Arabic direction and alignment
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
        body {{
            font-family: 'Arial', sans-serif;
            direction: rtl;
            text-align: right;
        }}
        </style>
    </head>
    <body>
        <h2>القسم: {department}</h2>
        <h3>المرحلة: {stage}</h3>
        {html_table}
    </body>
    </html>
    """


    # Attach the HTML content to the message
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    # Connect to Gmail SMTP server and send email
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        return ".تم إرسال البريد بنجاح"
    except Exception as e:
        return f"فشل إرسال البريد بسبب : {e}"
    finally:
        server.quit()
