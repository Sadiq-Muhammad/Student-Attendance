import os
import qrcode

def generate_student_qr_code(student_full_name, unique_data):
    """
    Generate a QR code image for a student and save it on the desktop under
    "Students QR Codes" folder with the student's full name as the file name.
    
    :param student_full_name: The student's full name to use as the file name.
    :param unique_data: The unique data (e.g., QR code string) to embed in the QR code.
    :return: The file path where the QR code image was saved.
    """
    # Determine the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_name = "Students QR Codes"
    folder_path = os.path.join(desktop_path, folder_name)
    
    # Create the folder if it doesn't exist.
    os.makedirs(folder_path, exist_ok=True)
    
    # Create a safe file name (remove or replace invalid characters if needed).
    # For simplicity, we assume student_full_name is safe.
    file_name = f"{student_full_name}.png"
    file_path = os.path.join(folder_path, file_name)
    
    # Create the QR code.
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code; increase if needed.
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(unique_data)
    qr.make(fit=True)
    
    # Generate and save the image.
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    return file_path
