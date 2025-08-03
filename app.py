import streamlit as st
import pymysql
from pymysql.err import OperationalError
import random
from datetime import datetime, timedelta
import base64
import os
from pathlib import Path

st.set_page_config(
    page_title="Buff University Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

def load_css():
    with open("logo.jpg", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: url(data:image/jpeg;base64,{encoded_logo}) no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(90deg, #003087, #0059b3);
            color: white;
            padding: 0.5rem;
            text-align: center;
            width: 100%;
            height: 80px;
            position: fixed;
            top: 0;
            left: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .header img {{
            width: 30px;
            height: auto;
        }}
        .header h1 {{
            margin: 0;
            font-size: 3rem;
            font-weight: 600;
            font-family: 'Roboto', 'Segoe UI', sans-serif;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .content {{
            margin: 60px auto 60px auto;
            padding: 1rem;
            max-width: 380px;
            width: 90%;
        }}
        .footer {{
            background: linear-gradient(90deg, #003087, #0059b3);
            color: white;
            padding: 0.8rem;
            text-align: center;
            font-size: 0.8rem;
            width: 100%;
            position: fixed;
            bottom: 0;
            left: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .footer a {{
            color: #93c5fd;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        div[data-testid="stForm"] {{
            border: 3px solid #f1f1f1;
            padding: 16px;
            background-color: rgba(0, 0, 0, 0.5);
            width: 100%;
            height: auto;
            box-sizing: border-box;
        }}
        .input-label {{
            font-size: 19px;
            color: #ffffff;
            font-weight: 500;
            margin-bottom: 0.4rem;
            display: block;
            text-align: left;
        }}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 12px 20px;
            font-size: 19px;
            color: #ffffff;
            background-color: rgba(0, 0, 0, 0.5);
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }}
        .stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder {{
            color: #cccccc;
            font-size: 19px;
        }}
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {{
            border-color: #003087;
            box-shadow: 0 0 4px rgba(0,48,135,0.3);
            outline: none;
            color: #ffffff;
        }}
        .stRadio > div {{
            display: flex;
            justify-content: center;
            gap: 1.2rem;
            margin-bottom: 0.5rem;
        }}
        .stRadio > div > label > div {{
            font-size: 19px;
            color: #ffffff;
        }}
        .stRadio > div > label > input[type=radio] {{
            accent-color: #04AA6D;
        }}
        .stFormSubmitButton button {{
            background-color: #04AA6D;
            color: #ffffff;
            padding: 14px 20px;
            border: none;
            border-radius: 6px;
            font-size: 19px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            transition: opacity 0.3s ease, transform 0.2s ease;
        }}
        .stFormSubmitButton button:hover {{
            opacity: 0.8;
            transform: translateY(-2px);
        }}
        .secondary-btn {{
            background: #6b7280;
            color: #ffffff;
            padding: 8px;
            border-radius: 6px;
            font-size: 19px;
            font-weight: 500;
            border: none;
            width: 100%;
            cursor: pointer;
            transition: background 0.3s ease, transform 0.2s ease;
        }}
        .secondary-btn:hover {{
            background: #4b5563;
            transform: translateY(-2px);
        }}
        .captcha-hint {{
            font-size: 19px;
            color: #ffffff;
            margin: 0.5rem 0;
            text-align: center;
        }}
        .instruction {{
            font-size: 19px;
            color: #ffffff;
            margin-bottom: 0.5rem;
            line-height: 1.4;
            text-align: left;
        }}
        .stAlert > div {{
            background: none;
            border: none;
            padding: 0.5rem;
            font-size: 19px;
            color: #ffffff;
        }}
        .sidebar .stButton > button {{
            width: 100%;
            text-align: left;
            padding: 8px;
            margin-bottom: 5px;
            border-radius: 6px;
            font-size: 19px;
            background: #f0f4f8;
            border: 1px solid #d1d5db;
            transition: background 0.3s ease;
        }}
        .sidebar .stButton > button:hover {{
            background: #e0e7ff;
        }}
        .button-row {{
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        .uploaded-file {{
            font-size: 19px;
            color: #ffffff;
            margin: 0.5rem 0;
        }}
        @media screen and (max-width: 600px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            .header img {{
                width: 25px;
            }}
            .footer, .footer a {{
                font-size: 0.7rem;
            }}
            .content {{
                margin: 50px auto 50px auto;
                padding: 0.8rem;
            }}
            .title {{
                font-size: 1.4rem;
            }}
            .input-label, .stTextInput > div > div > input, .stTextInput > div > div > input::placeholder, 
            .stTextArea > div > div > textarea, .stTextArea > div > div > textarea::placeholder,
            .stRadio > div > label > div, .stFormSubmitButton button, .captcha-hint, .instruction, .secondary-btn, .uploaded-file {{
                font-size: 16px;
            }}
        }}
        @media screen and (max-width: 300px) {{
            .button-row {{
                flex-direction: column;
            }}
            .secondary-btn {{
                width: 100%;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize session state
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'locked' not in st.session_state:
    st.session_state.locked = False
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'login_type' not in st.session_state:
    st.session_state.login_type = "Student"
if 'captcha_answer' not in st.session_state:
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    st.session_state.captcha_answer = num1 + num2
    st.session_state.captcha_question = f"{num1} + {num2} = ?"
if 'show_add_student' not in st.session_state:
    st.session_state.show_add_student = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# Database connection
def get_db_connection():
    try:
        return pymysql.connect(
            host='127.0.0.1',
            port=9000,
            user='root',
            password='root',
            database='university_management_system',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except OperationalError as e:
        st.error(f"⚠️ Database connection failed: {e}")
        return None

# File upload/create function
def upload_file(user_id, file_name, file=None, text_content=None):
    if not file_name:
        st.error("❌ Please provide a file name.")
        return False

    if file:
        allowed_types = ['text/plain', 'image/jpeg', 'image/png']
        if file.type not in allowed_types:
            st.error("❌ Only text (.txt) and image (.jpg, .png) files are allowed.")
            return False

        if file.size > 5 * 1024 * 1024:  # 5MB limit
            st.error("❌ File size exceeds 5MB limit.")
            return False

        file_extension = file.name.split('.')[-1].lower()
    elif text_content is not None:
        file_extension = 'txt'
    else:
        st.error("❌ Please provide a file or text content.")
        return False

    # Use student_id for students, username for admins/teachers
    folder_name = user_id
    user_dir = Path(folder_name)
    user_dir.mkdir(exist_ok=True)

    # Use original file name with timestamp to avoid conflicts
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}.{file_extension}"
    file_path = user_dir / unique_filename

    try:
        with open(file_path, "wb" if file else "w") as f:
            if file:
                f.write(file.getvalue())
            else:
                f.write(text_content)
        st.success(f"✅ File '{file_name}' {'uploaded' if file else 'created'} successfully in folder '{folder_name}'!")
        return True
    except Exception as e:
        st.error(f"⚠️ Error {'uploading' if file else 'creating'} file: {e}")
        return False

# Fetch user's files
def get_user_files(user_id):
    try:
        folder_name = user_id
        user_dir = Path(folder_name)
        files = []
        if user_dir.exists():
            for file_path in user_dir.glob("*"):
                if file_path.is_file():
                    timestamp_str = file_path.stem.split('_')[0]
                    try:
                        upload_date = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
                    except ValueError:
                        upload_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    files.append({
                        'file_name': file_path.name,
                        'file_path': str(file_path),
                        'upload_date': upload_date
                    })
        return sorted(files, key=lambda x: x['upload_date'], reverse=True)
    except Exception as e:
        st.error(f"⚠️ Error fetching files from folder '{folder_name}': {e}")
        return []

def authenticate_student(student_id, password, captcha):
    if st.session_state.locked and st.session_state.lockout_time:
        if datetime.now() < st.session_state.lockout_time + timedelta(minutes=5):
            st.error("🔒 Account locked. Try again in 5 minutes.")
            return False
        else:
            st.session_state.locked = False
            st.session_state.login_attempts = 0
            st.session_state.lockout_time = None
    
    if not student_id or not password:
        st.error("❌ Please enter both Student ID and password.")
        return False
        
    try:
        if int(captcha) != st.session_state.captcha_answer:
            st.error("❌ Incorrect CAPTCHA answer.")
            return False
    except ValueError:
        st.error("❌ Enter a valid number for CAPTCHA.")
        return False

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                sql = "SELECT student_id, role, password FROM users WHERE student_id=%s AND role='student'"
                cursor.execute(sql, (student_id,))
                user = cursor.fetchone()
                
                if user:
                    if password == user['password']:
                        st.session_state.logged_in = True
                        st.session_state.user = {'student_id': user['student_id'], 'role': user['role']}
                        st.session_state.role = 'student'
                        st.session_state.login_attempts = 0
                        st.session_state.show_add_student = False
                        st.session_state.current_page = 'student_dashboard'
                        st.success(f"✅ Welcome, Student ID: {user['student_id']}!")
                        st.rerun()
                        return True
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= 5:
                            st.session_state.locked = True
                            st.session_state.lockout_time = datetime.now()
                            st.error("🔒 Too many failed attempts. Account locked for 5 minutes.")
                        else:
                            remaining = 5 - st.session_state.login_attempts
                            st.error(f"❌ Invalid credentials. {remaining} attempt{'s' if remaining != 1 else ''} left.")
                        return False
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 5:
                        st.session_state.locked = True
                        st.session_state.lockout_time = datetime.now()
                        st.error("🔒 Too many failed attempts. Account locked for 5 minutes.")
                    else:
                        remaining = 5 - st.session_state.login_attempts
                        st.error(f"❌ Invalid credentials. {remaining} attempt{'s' if remaining != 1 else ''} left.")
                    return False
        finally:
            conn.close()
    return False

def authenticate_admin_teacher(username, password, expected_role, captcha):
    if st.session_state.locked and st.session_state.lockout_time:
        if datetime.now() < st.session_state.lockout_time + timedelta(minutes=5):
            st.error("🔒 Account locked. Try again in 5 minutes.")
            return False
        else:
            st.session_state.locked = False
            st.session_state.login_attempts = 0
            st.session_state.lockout_time = None
    
    if not username or not password:
        st.error("❌ Please enter both username and password.")
        return False
        
    try:
        if int(captcha) != st.session_state.captcha_answer:
            st.error("❌ Incorrect CAPTCHA answer.")
            return False
    except ValueError:
        st.error("❌ Enter a valid number for CAPTCHA.")
        return False

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = "SELECT username, role, password FROM users WHERE username=%s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if user:
                    if password == user['password']:
                        if user['role'] == expected_role:
                            st.session_state.logged_in = True
                            st.session_state.user = {'username': user['username'], 'role': user['role']}
                            st.session_state.role = user['role']
                            st.session_state.login_attempts = 0
                            st.session_state.show_add_student = False
                            st.session_state.current_page = f"{user['role']}_dashboard"
                            st.success(f"✅ Welcome, {user['username']} ({user['role'].title()})!")
                            st.rerun()
                            return True
                        else:
                            st.error(f"❌ This login is for {expected_role.title()}s only.")
                            return False
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= 5:
                            st.session_state.locked = True
                            st.session_state.lockout_time = datetime.now()
                            st.error("🔒 Too many failed attempts. Account locked for 5 minutes.")
                        else:
                            remaining = 5 - st.session_state.login_attempts
                            st.error(f"❌ Invalid credentials. {remaining} attempt{'s' if remaining != 1 else ''} left.")
                        return False
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 5:
                        st.session_state.locked = True
                        st.session_state.lockout_time = datetime.now()
                        st.error("🔒 Too many failed attempts. Account locked for 5 minutes.")
                    else:
                        remaining = 5 - st.session_state.login_attempts
                        st.error(f"❌ Invalid credentials. {remaining} attempt{'s' if remaining != 1 else ''} left.")
                    return False
        finally:
            conn.close()
    return False

def add_student(username, password, email, role, created_at, updated_at, student_id):
    if not username or not password or not email or not role:
        st.error("❌ Please enter all required fields (Username, Password, Email, Role).")
        return False

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                if student_id:
                    sql = "SELECT username, student_id FROM users WHERE username=%s OR student_id=%s"
                    cursor.execute(sql, (username, student_id))
                else:
                    sql = "SELECT username FROM users WHERE username=%s"
                    cursor.execute(sql, (username,))
                existing = cursor.fetchone()
                if existing:
                    if existing['username'] == username:
                        st.error("❌ Username already exists.")
                    elif student_id and existing['student_id'] == student_id:
                        st.error("❌ Student ID already exists.")
                    return False
                
                sql = "INSERT INTO users (username, password, email, role, created_at, updated_at, student_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    username,
                    password,
                    email,
                    role,
                    created_at if created_at else None,
                    updated_at if updated_at else None,
                    student_id if student_id else None
                ))
                conn.commit()
                st.success(f"✅ User {username} (Role: {role.title()}) added successfully!")
                return True
        except OperationalError as e:
            st.error(f"⚠️ Error adding user: {e}")
            return False
        finally:
            conn.close()
    return False

def switch_login_type(new_type):
    st.session_state.login_type = new_type
    st.session_state.login_attempts = 0
    st.session_state.locked = False
    st.session_state.lockout_time = None
    st.session_state.show_add_student = False
    st.session_state.current_page = None
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    st.session_state.captcha_answer = num1 + num2
    st.session_state.captcha_question = f"{num1} + {num2} = ?"

def student_dashboard():
    st.markdown(f"<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Student Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, Student ID: {st.session_state.user['student_id']}!")
    st.write("### Your Student Portal")
    st.info("Access your academic information below:")
    st.markdown("""
    - **Course Advising**: View and manage your course registrations.
    - **Class Schedule**: Check your weekly class schedule.
    - **Grades**: View your grades and academic performance.
    - **Drop Semester**: Request to drop the current semester.
    - **File Storage**: Upload or create text files.
    """)

def file_storage():
    st.markdown(f"<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>File Storage</h2>", unsafe_allow_html=True)
    st.info("Upload a text/image file or create a text file below:")
    
    # Determine user_id based on role
    user_id = st.session_state.user['student_id'] if st.session_state.role == 'student' else st.session_state.user['username']
    
    # File Upload Form
    with st.form("file_upload_form", clear_on_submit=True):
        st.markdown("<span class='input-label'>Select Action</span>", unsafe_allow_html=True)
        action = st.radio(
            "Choose an action",
            ("Upload File", "Create Text File"),
            horizontal=True,
            key="file_action_radio",
            label_visibility="collapsed"
        )
        
        st.markdown("<span class='input-label'>File Name</span>", unsafe_allow_html=True)
        file_name = st.text_input(
            "File Name",
            placeholder="Enter file name (e.g., myfile.txt)",
            key="file_name_input",
            label_visibility="collapsed"
        )

        file = None
        text_content = None
        if action == "Upload File":
            st.markdown("<span class='input-label'>Select File</span>", unsafe_allow_html=True)
            file = st.file_uploader(
                "Choose a file",
                type=['txt', 'jpg', 'png'],
                key="file_uploader_input",
                label_visibility="collapsed"
            )
        elif action == "Create Text File":
            st.markdown("<span class='input-label'>Text Content</span>", unsafe_allow_html=True)
            text_content = st.text_area(
                "Enter text content",
                placeholder="Type your text here...",
                key="text_content_input",
                label_visibility="collapsed"
            )

        if st.form_submit_button("Submit", type="primary", use_container_width=True):
            if not file_name:
                st.error("❌ Please provide a file name.")
            else:
                if upload_file(user_id, file_name, file=file, text_content=text_content):
                    st.rerun()
    
    # File List with Preview
    st.markdown("<h3 style='color: #003087; font-size: 16px; font-weight: 600; margin-top: 1rem;'>Your Files</h3>", unsafe_allow_html=True)
    files = get_user_files(user_id)
    if files:
        for file in files:
            file_path = Path(file['file_path'])
            file_ext = file_path.suffix.lower()
            file_size = file_path.stat().st_size / 1024  # Size in KB
            # Display original file name (after timestamp)
            display_name = '_'.join(file['file_name'].split('_')[1:])
            st.markdown(
                f"<div class='uploaded-file'>{display_name} (Uploaded: {file['upload_date']} | Size: {file_size:.2f} KB)</div>",
                unsafe_allow_html=True
            )
            
            # Preview for Text and Image Files
            with st.expander(f"Preview {display_name}"):
                if file_ext == ".txt":
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        st.text(content)
                    except UnicodeDecodeError:
                        with open(file_path, "r", encoding="latin1") as f:
                            content = f.read()
                        st.text(content)
                elif file_ext in [".jpg", ".png"]:
                    st.image(file_path, caption=display_name, use_column_width=True)
            
            # Delete Button
            if st.button("Delete", key=f"delete_{file['file_name']}"):
                try:
                    file_path.unlink()
                    st.success(f"✅ File '{display_name}' deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Error deleting file: {e}")
    else:
        st.markdown("<div class='uploaded-file'>No files uploaded yet.</div>", unsafe_allow_html=True)

def admin_dashboard():
    st.markdown(f"<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, {st.session_state.user['username']}!")
    st.write("### Admin Control Panel")
    if st.session_state.show_add_student:
        st.markdown("<h3 style='color: #003087; font-size: 16px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Add New User</h3>", unsafe_allow_html=True)
        with st.form("add_student_form", clear_on_submit=True):
            st.markdown("<span class='input-label'>Username</span>", unsafe_allow_html=True)
            username = st.text_input(
                "Username",
                placeholder="Enter username",
                key="new_student_username",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="new_student_password",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Email</span>", unsafe_allow_html=True)
            email = st.text_input(
                "Email",
                placeholder="Enter email (e.g., user@ewu.edu)",
                key="new_student_email",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Role</span>", unsafe_allow_html=True)
            role = st.selectbox(
                "Role",
                options=['student', 'teacher', 'admin'],
                index=0,
                key="new_user_role",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Student ID (Optional)</span>", unsafe_allow_html=True)
            student_id = st.text_input(
                "Student ID",
                placeholder="Enter Student ID (e.g., 2021-2-60-046) or leave blank",
                key="new_student_id",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Name (Optional)</span>", unsafe_allow_html=True)
            name = st.text_input(
                "Name",
                placeholder="Enter full name (e.g., John Doe) or leave blank",
                key="new_student_name",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Created At (Optional)</span>", unsafe_allow_html=True)
            created_at = st.date_input(
                "Created At",
                value=None,
                key="new_user_created_at",
                label_visibility="collapsed"
            )
            st.markdown("<span class='input-label'>Updated At (Optional)</span>", unsafe_allow_html=True)
            updated_at = st.date_input(
                "Updated At",
                value=None,
                key="new_user_updated_at",
                label_visibility="collapsed"
            )
            if st.form_submit_button("Add User", type="primary", use_container_width=True):
                created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else None
                updated_at_str = updated_at.strftime('%Y-%m-%d %H:%M:%S') if updated_at else None
                if add_student(username, password, email, role, created_at_str, updated_at_str, student_id):
                    st.session_state.show_add_student = False
                    st.rerun()
            if st.form_submit_button("Cancel", type="secondary", use_container_width=True):
                st.session_state.show_add_student = False
                st.rerun()
    else:
        st.info("Manage university operations below:")
        st.markdown("""
        - **User Management**: Add or update user accounts.
        - **System Settings**: Configure portal settings.
        - **File Storage**: Upload or create text files.
        """)

def teacher_dashboard():
    st.markdown(f"<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Teacher Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, {st.session_state.user['username']}!")
    st.write("### Teacher Portal")
    st.info("Manage your teaching activities below:")
    st.markdown("""
    - **Course Management**: View and manage your courses.
    - **Student Grades**: Enter or update student grades.
    - **Class Schedule**: View your teaching schedule.
    - **File Storage**: Upload or create text files.
    """)

def render_sidebar():
    with st.sidebar:
        st.image("logo.jpg", width=40)
        if st.session_state.role == 'student':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Student Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['student_id']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="student_dashboard_btn"):
                st.session_state.current_page = 'student_dashboard'
                st.rerun()
            if st.button("Course Advising", key="student_advising"):
                st.session_state.current_page = 'course_advising'
                st.rerun()
            if st.button("Class Schedule", key="student_schedule"):
                st.session_state.current_page = 'class_schedule'
                st.rerun()
            if st.button("Grades", key="student_grades"):
                st.session_state.current_page = 'grades'
                st.rerun()
            if st.button("Drop Semester", key="student_drop"):
                st.session_state.current_page = 'drop_semester'
                st.rerun()
            if st.button("File Storage", key="student_file_storage"):
                st.session_state.current_page = 'file_storage'
                st.rerun()
            if st.button("Logout", key="student_logout", type="secondary"):
                confirm_logout()
        elif st.session_state.role == 'admin':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Admin Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['username']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="admin_dashboard"):
                st.session_state.show_add_student = False
                st.session_state.current_page = 'admin_dashboard'
                st.rerun()
            if st.button("Add User", key="admin_add_student"):
                st.session_state.show_add_student = True
                st.session_state.current_page = 'admin_dashboard'
                st.rerun()
            if st.button("User Management", key="admin_users"):
                st.session_state.show_add_student = False
                st.session_state.current_page = 'user_management'
                st.rerun()
            if st.button("File Storage", key="admin_file_storage"):
                st.session_state.show_add_student = False
                st.session_state.current_page = 'file_storage'
                st.rerun()
            if st.button("Logout", key="admin_logout", type="secondary"):
                confirm_logout()
        elif st.session_state.role == 'teacher':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Teacher Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['username']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="teacher_dashboard"):
                st.session_state.current_page = 'teacher_dashboard'
                st.rerun()
            if st.button("Course Management", key="teacher_courses"):
                st.session_state.current_page = 'course_management'
                st.rerun()
            if st.button("Student Grades", key="teacher_grades"):
                st.session_state.current_page = 'student_grades'
                st.rerun()
            if st.button("Class Schedule", key="teacher_schedule"):
                st.session_state.current_page = 'teacher_schedule'
                st.rerun()
            if st.button("File Storage", key="teacher_file_storage"):
                st.session_state.current_page = 'file_storage'
                st.rerun()
            if st.button("Logout", key="teacher_logout", type="secondary"):
                confirm_logout()

def confirm_logout():
    if st.session_state.get('logged_in'):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.login_attempts = 0
        st.session_state.locked = False
        st.session_state.lockout_time = None
        st.session_state.show_add_student = False
        st.session_state.current_page = None
        st.success("✅ Logged out successfully!")
        st.rerun()

# Main UI
with st.container():
    with open("logo.jpg", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <div class="header">
        <img src="data:image/jpeg;base64,{encoded_logo}" alt="EWU Logo" style='width: 30px; height: auto;'>
        <h1 style='margin: 0; font-weight: 600; color: white;'>Buff University Poral</h1>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('logged_in') and st.session_state.role in ['student', 'admin', 'teacher']:
        render_sidebar()

    with st.container():
        st.markdown("<div class='content'>", unsafe_allow_html=True)
        if st.session_state.get('logged_in') and st.session_state.role in ['student', 'admin', 'teacher']:
            if st.session_state.role == 'student':
                if st.session_state.current_page == 'student_dashboard':
                    student_dashboard()
                elif st.session_state.current_page == 'course_advising':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Course Advising</h2>", unsafe_allow_html=True)
                    st.info("Course advising functionality coming soon!")
                elif st.session_state.current_page == 'class_schedule':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Class Schedule</h2>", unsafe_allow_html=True)
                    st.info("Class schedule functionality coming soon!")
                elif st.session_state.current_page == 'grades':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Grades</h2>", unsafe_allow_html=True)
                    st.info("Grades functionality coming soon!")
                elif st.session_state.current_page == 'drop_semester':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Drop Semester</h2>", unsafe_allow_html=True)
                    st.info("Semester drop functionality coming soon!")
                elif st.session_state.current_page == 'file_storage':
                    file_storage()
                else:
                    student_dashboard()
            elif st.session_state.role == 'admin':
                if st.session_state.current_page == 'admin_dashboard':
                    admin_dashboard()
                elif st.session_state.current_page == 'user_management':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>User Management</h2>", unsafe_allow_html=True)
                    st.info("User management functionality coming soon!")
                elif st.session_state.current_page == 'file_storage':
                    file_storage()
                else:
                    admin_dashboard()
            elif st.session_state.role == 'teacher':
                if st.session_state.current_page == 'teacher_dashboard':
                    teacher_dashboard()
                elif st.session_state.current_page == 'course_management':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Course Management</h2>", unsafe_allow_html=True)
                    st.info("Course management functionality coming soon!")
                elif st.session_state.current_page == 'student_grades':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Student Grades</h2>", unsafe_allow_html=True)
                    st.info("Student grades functionality coming soon!")
                elif st.session_state.current_page == 'teacher_schedule':
                    st.markdown("<h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Class Schedule</h2>", unsafe_allow_html=True)
                    st.info("Class schedule functionality coming soon!")
                elif st.session_state.current_page == 'file_storage':
                    file_storage()
                else:
                    teacher_dashboard()
        else:
            if st.session_state.login_type == "Student":
                st.markdown("<h2 style='color: #FFFFFF; font-size: 42px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Student Login</h2>", unsafe_allow_html=True)
                
                with st.form("student_login_form", clear_on_submit=True):
                    st.markdown("<span class='input-label'>Student ID</span>", unsafe_allow_html=True)
                    student_id = st.text_input(
                        "Student ID",
                        placeholder="Enter Student ID (e.g., 2021-2-60-046)",
                        key="student_id",
                        label_visibility="collapsed"
                    )
                    st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter password",
                        key="student_password",
                        label_visibility="collapsed"
                    )
                    st.markdown("<span class='input-label'>CAPTCHA</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='captcha-hint'>{st.session_state.captcha_question}</div>", unsafe_allow_html=True)
                    captcha = st.text_input(
                        "CAPTCHA Answer",
                        placeholder="Enter answer",
                        key="student_captcha",
                        label_visibility="collapsed"
                    )
                    if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                        authenticate_student(student_id, password, captcha)
                
                st.markdown("<div class='button-row'>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Forgot Password?", type="secondary", use_container_width=True, key="student_forgot"):
                        st.info("📧 Email it.support@ewu.edu for help.")
                with col2:
                    if st.button("Admin/Teacher Login", type="secondary", use_container_width=True, key="switch_to_admin", on_click=switch_login_type, args=("Admin/Teacher",)):
                        pass
                st.markdown("</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="instruction">
                    🔐 Authorized access only<br>
                    📋 Activity logged<br>
                    📞 Contact IT for support
                </div>
                <h2 style='color: #003087; font-size: 19px; font-weight: 600; text-align: center; margin-bottom: 0.5rem;'>Admin/Teacher Login</h2>
                """, unsafe_allow_html=True)
                
                with st.form("admin_teacher_login_form", clear_on_submit=True):
                    st.markdown("<span class='input-label'>Login as</span>", unsafe_allow_html=True)
                    role = st.radio(
                        "Login as",
                        ("Admin", "Teacher"),
                        horizontal=True,
                        key="admin_teacher_role",
                        label_visibility="collapsed"
                    )
                    st.markdown("<span class='input-label'>Username</span>", unsafe_allow_html=True)
                    username = st.text_input(
                        "Username",
                        placeholder="Enter username",
                        key="admin_username",
                        label_visibility="collapsed"
                    )
                    st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter password",
                        key="admin_password",
                        label_visibility="collapsed"
                    )
                    st.markdown("<span class='input-label'>CAPTCHA</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='captcha-hint'>{st.session_state.captcha_question}</div>", unsafe_allow_html=True)
                    captcha = st.text_input(
                        "CAPTCHA Answer",
                        placeholder="Enter answer",
                        key="admin_captcha",
                        label_visibility="collapsed"
                    )
                    if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                        authenticate_admin_teacher(username, password, role.lower(), captcha)
                
                st.markdown("<div class='button-row'>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Forgot Password?", type="secondary", use_container_width=True, key="admin_forgot"):
                        st.info("📧 Email it.support@ewu.edu for help.")
                with col2:
                    if st.button("Student Login", type="secondary", use_container_width=True, key="switch_to_student", on_click=switch_login_type, args=("Student",)):
                        pass
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.8rem; flex-wrap: wrap;">
            <span>© 2025 East West University. All rights reserved.</span>
            <span>Contact: <a href="mailto:it.support@ewu.edu">it.support@ewu.edu</a> | Phone: +880 1234 567890 | <a href="https://www.ewu.edu">www.ewu.edu</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)