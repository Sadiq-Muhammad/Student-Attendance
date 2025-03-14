import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='assets\\attendance.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create students table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                department TEXT NOT NULL,
                stage TEXT NOT NULL,
                qr_code TEXT UNIQUE
            )
        ''')
        # Create attendance_sessions table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT NOT NULL DEFAULT 'open'
            )
        ''')
        # Create attendance_records table.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                scan_time TEXT,
                FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        self.conn.commit()

    # ---------------------------
    # CRUD operations for students
    # ---------------------------
    def add_student(self, full_name, department, stage):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO students (full_name, department, stage)
            VALUES (?, ?, ?)
        ''', (full_name, department, stage))
        self.conn.commit()
        return cursor.lastrowid

    def get_student(self, student_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        return cursor.fetchone()
    
    def search_students(self, name_pattern):
        cursor = self.conn.cursor()
        # Use wildcards and parameterized queries to avoid SQL injection.
        cursor.execute("SELECT * FROM students WHERE full_name LIKE ?", ('%' + name_pattern + '%',))
        return cursor.fetchall()

    def update_student(self, student_id, full_name=None, department=None, stage=None, qr_code=None):
        cursor = self.conn.cursor()
        fields = []
        values = []
        if full_name is not None:
            fields.append("full_name = ?")
            values.append(full_name)
        if department is not None:
            fields.append("department = ?")
            values.append(department)
        if stage is not None:
            fields.append("stage = ?")
            values.append(stage)
        if qr_code is not None:
            fields.append("qr_code = ?")
            values.append(qr_code)
        values.append(student_id)
        sql = "UPDATE students SET " + ", ".join(fields) + " WHERE student_id = ?"
        cursor.execute(sql, values)
        self.conn.commit()

    def delete_student(self, student_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()

    def get_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students')
        return cursor.fetchall()

    # ---------------------------------------
    # Attendance session and record operations
    # ---------------------------------------
    def start_attendance_session(self):
        """
        Called when the professor starts a new session.
        """
        cursor = self.conn.cursor()
        start_time = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO attendance_sessions (start_time, status)
            VALUES (?, 'open')
        ''', (start_time,))
        self.conn.commit()
        return cursor.lastrowid

    def mark_attendance(self, session_id, qr_code):
        """
        Called when a student scans their QR code.
        If the student is found and not already marked in this session, mark them as present.
        """
        cursor = self.conn.cursor()
        # Identify the student by QR code.
        cursor.execute('SELECT student_id, full_name FROM students WHERE qr_code = ?', (qr_code,))
        student = cursor.fetchone()
        if student is None:
            return "الطالب غير موجود في قاعدة البيانات"
        student_id = student['student_id']
        student_name = student['full_name']
        # Check if attendance has already been recorded.
        cursor.execute('''
            SELECT * FROM attendance_records
            WHERE session_id = ? AND student_id = ?
        ''', (session_id, student_id))
        record = cursor.fetchone()
        if record:
            return "تم تسجيل حضور هذا الطالب بالفعل"
        scan_time = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO attendance_records (session_id, student_id, status, scan_time)
            VALUES (?, ?, 'حاضر', ?)
        ''', (session_id, student_id, scan_time))
        self.conn.commit()
        return student_name

    def end_attendance_session(self, session_id):
        """
        Called when the professor finishes the attendance session.
        For every student from the same stage and department as a student 
        who attended the session, insert an 'absent' record if no record exists.
        Then, update the session to close it.
        """
        cursor = self.conn.cursor()
        end_time = datetime.now().isoformat()
        # Close the session.
        cursor.execute('''
            UPDATE attendance_sessions
            SET end_time = ?, status = 'closed'
            WHERE session_id = ?
        ''', (end_time, session_id))
        
        # Get one student who attended the session.
        cursor.execute('''
            SELECT student_id FROM attendance_records
            WHERE session_id = ?
            LIMIT 1
        ''', (session_id,))
        present_student = cursor.fetchone()
        
        if present_student is None:
            # No student attended the session, so nothing to filter on.
            # Optionally, you might want to mark all students as absent or handle this case differently.
            self.conn.commit()
            return
        
        # Get the stage and department of the present student.
        cursor.execute('''
            SELECT stage, department FROM students
            WHERE student_id = ?
        ''', (present_student['student_id'],))
        student_info = cursor.fetchone()
        
        if student_info is None:
            self.conn.commit()
            return
        
        stage = student_info['stage']
        department = student_info['department']
        
        # Get all students with the same stage and department.
        cursor.execute('''
            SELECT student_id FROM students
            WHERE stage = ? AND department = ?
        ''', (stage, department))
        filtered_students = cursor.fetchall()
        
        for student in filtered_students:
            student_id = student['student_id']
            # Check if this student already has a record for the session.
            cursor.execute('''
                SELECT * FROM attendance_records
                WHERE session_id = ? AND student_id = ?
            ''', (session_id, student_id))
            record = cursor.fetchone()
            if not record:
                cursor.execute('''
                    INSERT INTO attendance_records (session_id, student_id, status, scan_time)
                    VALUES (?, ?, 'غائب' ?)
                ''', (session_id, student_id, end_time))
                
        self.conn.commit()

    def get_attendance_data(self, session_id):
        """
        Retrieves the attendance data for a given session_id.
        
        Returns:
            department (str): The department of the students in the session.
            stage (str): The stage of the students in the session.
            attendance_data (list of tuples): Each tuple contains (student_full_name, status)
        """
        cursor = self.conn.cursor()
        
        # Get department and stage from one attendance record.
        cursor.execute('''
            SELECT s.department, s.stage 
            FROM attendance_records ar
            JOIN students s ON ar.student_id = s.student_id
            WHERE ar.session_id = ?
            LIMIT 1
        ''', (session_id,))
        result = cursor.fetchone()
        if result is None:
            # No attendance records exist for this session.
            return None, None, []
        
        department = result['department']
        stage = result['stage']
        
        # Get all attendance records for the session with student names.
        cursor.execute('''
            SELECT s.full_name, ar.status
            FROM attendance_records ar
            JOIN students s ON ar.student_id = s.student_id
            WHERE ar.session_id = ?
            ORDER BY s.full_name
        ''', (session_id,))
        
        rows = cursor.fetchall()
        # Format the data as a list of tuples (full_name, status)
        attendance_data = [(row['full_name'], row['status']) for row in rows]
        
        return department, stage, attendance_data

    def get_students_attendance_summary(self, department, stage):
        """
        Returns a summary of student attendance (student_id, full_name, total present, total absent)
        based on department and stage.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.student_id, s.full_name, 
                   SUM(CASE WHEN ar.status = 'حاضر' THEN 1 ELSE 0 END) AS total_present,
                   SUM(CASE WHEN ar.status = 'غائب' THEN 1 ELSE 0 END) AS total_absent
            FROM students s
            LEFT JOIN attendance_records ar ON s.student_id = ar.student_id
            WHERE s.department = ? AND s.stage = ?
            GROUP BY s.student_id, s.full_name
        ''', (department, stage))
        
        return cursor.fetchall()

    def search_students_attendance_summary(self, name_pattern, department, stage):
        """
        Searches for students by name pattern and returns attendance summary 
        (student_id, full_name, total present, total absent) based on department and stage.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.student_id, s.full_name, 
                   SUM(CASE WHEN ar.status = 'حاضر' THEN 1 ELSE 0 END) AS total_present,
                   SUM(CASE WHEN ar.status = 'غائب' THEN 1 ELSE 0 END) AS total_absent
            FROM students s
            LEFT JOIN attendance_records ar ON s.student_id = ar.student_id
            WHERE s.full_name LIKE ? AND s.department = ? AND s.stage = ?
            GROUP BY s.student_id, s.full_name
        ''', ('%' + name_pattern + '%', department, stage))
        
        return cursor.fetchall()

    def get_student_attendance_history(self, student_id):
        """
        Returns the attendance history (session_id, status, scan_time) for a given student.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ar.session_id, ar.status, ar.scan_time
            FROM attendance_records ar
            WHERE ar.student_id = ?
            ORDER BY ar.session_id
        ''', (student_id,))
        
        return cursor.fetchall()
