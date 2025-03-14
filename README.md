# Student Attendance System

## Overview

The **Student Attendance System** is a Python-based application that tracks student attendance using QRcode scanning. It provides a graphical user interface (GUI) built with `customtkinter`, allowing users to view attendance records, mark attendance, and manage student data efficiently.

## Features

- **Student Attendance Tracking**: Records attendance by scanning barcodes.
- **Graphical User Interface**: Built using `customtkinter` for a modern UI.
- **Attendance History**: Displays attendance records for each student.
- **Database Management**: Stores and retrieves data using SQLite.
- **Multi-Language Support**: Supports right-to-left (RTL) text rendering for Arabic.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.13 or later
- SQLite (bundled with Python)

### Setup

## Manually

1. Clone the repository:

   ```sh
   git clone https://github.com/your-repo/student-attendance.git
   cd student-attendance
   ```

2. Create a virtual environment:

   ```sh

   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:

     ```powershell
     venv\Scripts\activate
     ```

   - **Linux/macOS**:

     ```sh
     source venv/bin/activate
     ```

4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Automatically

   You can run the setup_env.bat on windows and it will create the virtual envirement and install the requirements.

   ```powershell
   ./setup_env.bat
   ```

## Usage

1. Run the application:

   ```sh
   python main.py
   ```

2. Use the GUI to:
   - Scan student barcodes
   - View attendance history
   - Manage attendance records

## Troubleshooting

### Missing DLLs (Windows)

If you encounter a `FileNotFoundError` related to `libzbar-64.dll`:

- Download `libzbar-64.dll` and `libiconv.dll`.
- Place them in the `venv\Lib\site-packages\pyzbar\` directory.

### Updating Dependencies

To update dependencies, run:

```sh
pip install --upgrade -r requirements.txt
```

## Contributing

Feel free to fork this repository and submit pull requests. Ensure your code follows best practices and is well-documented.

## License

This project is licensed under the MIT License.

## Contact

For support, contact [sadmoe000@gmail.com](sadmoe000@gmail.com).
