import streamlit as st
import pymysql
from pymysql.err import OperationalError
import random
from datetime import datetime, timedelta, date, time as dtime
import base64
from pathlib import Path

# ============================
# Streamlit page config
# ============================
st.set_page_config(
    page_title="Bangladesh Gen Z University Management System",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================
# CSS & Branding
# ============================
def load_css():
    try:
        with open("logo.jpg", "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        encoded_logo = ""  # Fallback if logo is missing
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
        .header h1 {{
            margin: 0;
            font-size: 3rem;
            font-weight: 600;
            font-family: 'Roboto', 'Segoe UI', sans-serif;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .content {{
            margin: 100px auto 60px auto;
            padding: 1rem;
            max-width: 900px;
            width: 94%;
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
        .captcha-hint {{
            font-size: 19px;
            color: #ffffff;
            margin: 0.5rem 0;
            text-align: center;
        }}
        .stAlert > div {{
            background: none;
            border: none;
            padding: 0.5rem;
            font-size: 19px;
            color: #ffffff;
        }}
        .pill {{
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 12px;
            margin-left: 6px;
        }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================
# Session State Initialization
# ============================
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'locked' not in st.session_state:
    st.session_state.locked = False
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None  # {'id', 'username' or 'student_id', 'role'}
if 'role' not in st.session_state:
    st.session_state.role = None
if 'login_type' not in st.session_state:
    st.session_state.login_type = "Student"
if 'captcha_answer' not in st.session_state:
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    st.session_state.captcha_answer = num1 + num2
    st.session_state.captcha_question = f"{num1} + {num2} = ?"
if 'show_add_user' not in st.session_state:
    st.session_state.show_add_user = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# ============================
# Database connection & helpers
# ============================
def get_db_connection():
    try:
        return pymysql.connect(
            host='127.0.0.1',
            port=9000,
            user='root',
            password='root',
            database='university_management_system2',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except OperationalError as e:
        st.error(f"⚠️ Database connection failed: {e}")
        return None

def db_execute(query, params=None, fetchone=False, fetchall=False, commit=False):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cur.fetchone()
            if fetchall:
                return cur.fetchall()
    except Exception as e:
        st.error(f"⚠️ Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()
    return None

# ============================
# File storage utilities (local demo)
# ============================
def upload_file(user_key, file_name, file=None, text_content=None):
    if not file_name:
        st.error("❌ Please provide a file name.")
        return False

    if file:
        allowed_types = ['text/plain', 'image/jpeg', 'image/png']
        if getattr(file, 'type', None) not in allowed_types:
            st.error("❌ Only text (.txt) and image (.jpg, .png) files are allowed.")
            return False
        if getattr(file, 'size', 0) > 5 * 1024 * 1024:  # 5MB
            st.error("❌ File size exceeds 5MB limit.")
            return False
        file_extension = file.name.split('.')[-1].lower()
    elif text_content is not None:
        file_extension = 'txt'
    else:
        st.error("❌ Please provide a file or text content.")
        return False

    user_dir = Path(str(user_key))
    user_dir.mkdir(exist_ok=True)

    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}.{file_extension}"
    file_path = user_dir / unique_filename

    try:
        with open(file_path, "wb" if file else "w", encoding=None if file else "utf-8") as f:
            if file:
                f.write(file.getvalue())
            else:
                f.write(text_content)
        st.success(f"✅ File '{file_name}' {'uploaded' if file else 'created'} successfully!")
        return True
    except Exception as e:
        st.error(f"⚠️ Error {'uploading' if file else 'creating'} file: {e}")
        return False

def get_user_files(user_key):
    try:
        user_dir = Path(str(user_key))
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
        st.error(f"⚠️ Error fetching files: {e}")
        return []

# ============================
# Authentication & User Admin
# ============================
def _captcha_ok(captcha):
    try:
        return int(captcha) == st.session_state.captcha_answer
    except Exception:
        return False

def authenticate_student(student_id, password, captcha):
    if st.session_state.locked and st.session_state.lockout_time and datetime.now() < st.session_state.lockout_time + timedelta(minutes=5):
        st.error("🔒 Account locked. Try again in 5 minutes.")
        return False

    if not student_id or not password:
        st.error("❌ Please enter both Student ID and password.")
        return False

    if not _captcha_ok(captcha):
        st.error("❌ Incorrect CAPTCHA answer.")
        return False

    user = db_execute(
        "SELECT student_id, role, password FROM users WHERE student_id=%s AND role='student'",
        (student_id,), fetchone=True
    )
    if user and password == user['password']:
        st.session_state.logged_in = True
        st.session_state.user = {'student_id': user['student_id'], 'role': user['role']}
        st.session_state.role = 'student'
        st.session_state.login_attempts = 0
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

def authenticate_admin_faculty(username, password, expected_role, captcha):
    if st.session_state.locked and st.session_state.lockout_time and datetime.now() < st.session_state.lockout_time + timedelta(minutes=5):
        st.error("🔒 Account locked. Try again in 5 minutes.")
        return False

    if not username or not password:
        st.error("❌ Please enter both username and password.")
        return False

    if not _captcha_ok(captcha):
        st.error("❌ Incorrect CAPTCHA answer.")
        return False

    user = db_execute(
        "SELECT  username, role, password FROM users WHERE username=%s",
        (username,), fetchone=True
    )
    if user and password == user['password']:
        if user['role'] == expected_role:
            st.session_state.logged_in = True
            st.session_state.user = {'username': user['username'], 'role': user['role']}
            st.session_state.role = user['role']
            st.session_state.login_attempts = 0
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

def add_user(username, password, email, role, created_at, updated_at, student_id):
    if not username or not password or not email or not role:
        st.error("❌ Please enter all required fields (Username, Password, Email, Role).")
        return False

    existing_username = db_execute("SELECT sl FROM users WHERE username=%s", (username,), fetchone=True)
    if existing_username:
        st.error("❌ Username already exists.")
        return False
    if role == 'student' and student_id:
        existing_sid = db_execute("SELECT sl FROM users WHERE student_id=%s", (student_id,), fetchone=True)
        if existing_sid:
            st.error("❌ Student ID already exists.")
            return False

    db_execute(
        """
        INSERT INTO users (username, password, email, role, created_at, updated_at, student_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (username, password, email, role, created_at, updated_at, student_id if role == 'student' else None),
        commit=True
    )
    st.success(f"✅ User {username} (Role: {role.title()}) added successfully!")
    return True

def switch_login_type(new_type):
    st.session_state.login_type = new_type
    st.session_state.login_attempts = 0
    st.session_state.locked = False
    st.session_state.lockout_time = None
    st.session_state.show_add_user = False
    st.session_state.current_page = None
    a, b = random.randint(1, 10), random.randint(1, 10)
    st.session_state.captcha_answer = a + b
    st.session_state.captcha_question = f"{a} + {b} = ?"

# ============================
# Student Pages
# ============================
def student_dashboard():
    sid = st.session_state.user.get('student_id', '—')
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Student Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, Student ID: {sid}!")
    st.info("Use the sidebar to navigate: Advising, Enrollment, Schedule, Grades, Files.")

def page_advising_and_enrollment():
    st.markdown("<h3 style='color:#fff;'>Schedule Meeting</h3>", unsafe_allow_html=True)

    default_datetime = datetime.now() + timedelta(days=1)
    meeting_date = st.date_input("Meeting Date", value=default_datetime.date())
    meeting_time = st.time_input("Meeting Time", value=default_datetime.time())
    meeting_dt = datetime.combine(meeting_date, meeting_time)
    st.caption(f"Selected: {meeting_dt}")

    st.markdown("<h3 style='color:#fff;'>Courses & Enrollment</h3>", unsafe_allow_html=True)
    q = st.text_input("Search courses by code/title:", placeholder="e.g., CSE101 or Programming")
    cond, params = "", []
    if q:
        cond = "WHERE code LIKE %s OR title LIKE %s"
        like = f"%{q}%"
        params = [like, like]

    courses = db_execute(
        f"SELECT code, title, description, credit as credit FROM courses {cond} ORDER BY title LIMIT 200",
        params, fetchall=True
    ) or []

    student_id = st.session_state.user['student_id']
    my = db_execute("SELECT course_code FROM enrollments WHERE student_id=%s", (student_id,), fetchall=True) or []
    my_set = {m['course_code'] for m in my}

    if not courses:
        st.info("No courses found.")
    else:
        for c in courses:
            st.markdown(f"**{c['code']} — {c['title']}** <span class='pill'>{float(c['credit']):.1f} cr</span>", unsafe_allow_html=True)
            st.caption((c.get('description') or '').strip())
            col1, col2 = st.columns(2)
            with col1:
                if c['code'] in my_set:
                    if st.button(f"Drop {c['code']}", key=f"drop_{c['code']}"):
                        db_execute(
                            "DELETE FROM enrollments WHERE student_id=%s AND course_code=%s",
                            (student_id, c['code']), commit=True
                        )
                        st.success("Dropped.")
                        st.rerun()
                else:
                    if st.button(f"Enroll in {c['code']}", key=f"enroll_{c['code']}"):
                        db_execute(
                            "INSERT INTO enrollments (student_id, course_code) VALUES (%s, %s)",
                            (student_id, c['code']), commit=True
                        )
                        st.success("Enrolled.")
                        st.rerun()
            with col2:
                sched = db_execute(
                    "SELECT day, start_time, end_time FROM schedules WHERE course_code=%s "
                    "ORDER BY FIELD(day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), start_time",
                    (c['code'],), fetchall=True
                ) or []
                st.caption("; ".join([f"{r['day']} {r['start_time']}–{r['end_time']}" for r in sched]) if sched else "No schedule set")
            st.divider()

def page_class_schedule():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Class Schedule</h2>", unsafe_allow_html=True)
    student_id = st.session_state.user['student_id']
    rows = db_execute(
        """
        SELECT c.title, c.credit, s.day, s.start_time, s.end_time
        FROM enrollments e
        JOIN courses c ON c.code = e.course_code
        LEFT JOIN schedules s ON s.course_code = c.code
        WHERE e.student_id = %s
        ORDER BY FIELD(s.day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), s.start_time
        """,
        (student_id,), fetchall=True
    ) or []

    if not rows:
        st.info("No classes scheduled. Enroll in some courses first.")
        return

    current_day = None
    for r in rows:
        if r['day'] != current_day:
            current_day = r['day']
            st.subheader(current_day or "Unscheduled")
        st.markdown(f"- **{r['title']}** ({float(r['credit']):.1f} cr) — {r['start_time']}–{r['end_time']}")

def page_grades():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Grades</h2>", unsafe_allow_html=True)
    student_id = st.session_state.user['student_id']

    rows = db_execute(
        """
        SELECT c.code,c.credit,g.grade
        FROM grades g
        JOIN courses c ON c.code=g.course_code
        WHERE g.student_id=%s
        ORDER BY c.title
        """,
        (student_id,), fetchall=True
    ) or []

    if not rows:
        st.info("No grades yet.")
        return

    total_weight = 0.0
    total_credit = 0.0
    for r in rows:
        st.markdown(f"- **{r['code']}** ({float(r['credit']):.1f} cr): Grade **{r['grade'] if r['grade'] is not None else '—'}**")
        if r['grade'] is not None and r['credit']:
            total_weight += float(r['grade']) * float(r['credit'])
            total_credit += float(r['credit'])

    if total_credit > 0:
        st.markdown(f"### Weighted GPA (numeric scale): **{total_weight/total_credit:.2f}**")

# ============================
# Admin Pages
# ============================
def admin_dashboard():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, {st.session_state.user['username']}!")
    st.info("Use the sidebar to manage users, courses, faculty assignments, and class schedules.")
    if st.session_state.show_add_user:
        with st.form("add_user_form", clear_on_submit=True):
            username = st.text_input("Username", placeholder="Enter username", key="new_username")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="new_password")
            email = st.text_input("Email", placeholder="Enter email (e.g., user@example.edu)", key="new_email")
            role = st.selectbox("Role", options=['student', 'faculty', 'admin'], index=0, key="new_role")
            student_id = st.text_input("Student ID (for students)", placeholder="e.g., 2021-2-60-046", key="new_student_id")

            use_custom_times = st.checkbox("Set custom Created/Updated dates (optional)", value=False)
            created_at = None
            updated_at = None
            if use_custom_times:
                created_at = st.date_input("Created At", value=date.today(), key="new_created_at").strftime('%Y-%m-%d %H:%M:%S')
                updated_at = st.date_input("Updated At", value=date.today(), key="new_updated_at").strftime('%Y-%m-%d %H:%M:%S')

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Add User", type="primary", use_container_width=True):
                    if add_user(username, password, email, role, created_at, updated_at, student_id if role=='student' else None):
                        st.session_state.show_add_user = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel", type="secondary", use_container_width=True):
                    st.session_state.show_add_user = False
                    st.rerun()
    else:
        st.caption("Tip: Go to Course Catalog to create courses, then assign faculty, then add the class schedule.")

def page_user_management():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>User Management</h2>", unsafe_allow_html=True)
    q = st.text_input("Search users (username/email/student_id):")
    cond, params = "", []
    if q:
        cond = "WHERE (username LIKE %s OR email LIKE %s OR student_id LIKE %s)"
        like = f"%{q}%"
        params = [like, like, like]

    users = db_execute(f"""
        SELECT  username, role, email, student_id, created_at
        FROM users {cond}
        ORDER BY role, username
        LIMIT 200
    """, params, fetchall=True) or []

    if not users:
        st.info("No users found.")
    else:
        for u in users:
            created = u['created_at'].strftime('%Y-%m-%d') if u['created_at'] else '—'
            st.markdown(f"- **{u['username']}** | {u['role'].title()} | {u['email']} | Student ID: {u['student_id'] or '—'} | Created: {created}")

# --- Admin: Course Catalog (CRUD: create + simple delete) ---
def page_admin_course_catalog():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Course Catalog</h2>", unsafe_allow_html=True)

    with st.form("add_course_form", clear_on_submit=True):
        code = st.text_input("Course Code", placeholder="e.g., CSE101")
        title = st.text_input("Title", placeholder="e.g., Introduction to Programming")
        credit = st.number_input("Credit", min_value=0.0, max_value=10.0, step=0.5, value=3.0)
        description = st.text_area("Description", placeholder="Short course description (optional)")
        submitted = st.form_submit_button("Add Course", type="primary", use_container_width=True)
        if submitted:
            if not code or not title:
                st.error("Course code and title are required.")
            else:
                exists = db_execute("SELECT code FROM courses WHERE code=%s", (code,), fetchone=True)
                if exists:
                    st.error("Course code already exists.")
                else:
                    db_execute(
                        "INSERT INTO courses (code, title, credit, description) VALUES (%s, %s, %s, %s)",
                        (code.strip(), title.strip(), float(credit), description.strip() if description else None),
                        commit=True
                    )
                    st.success(f"Course {code} added.")
                    st.rerun()

    st.subheader("All Courses")
    q = st.text_input("Filter by code/title", key="course_filter")
    cond, params = "", []
    if q:
        cond = "WHERE code LIKE %s OR title LIKE %s"
        like = f"%{q}%"
        params = [like, like]

    rows = db_execute(f"SELECT code, title, credit, description FROM courses {cond} ORDER BY code", params, fetchall=True) or []
    if not rows:
        st.info("No courses.")
    else:
        for r in rows:
            with st.expander(f"{r['code']} — {r['title']} ({float(r['credit']):.1f} cr)"):
                st.caption(r.get('description') or "No description.")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"Delete {r['code']}", key=f"del_course_{r['code']}"):
                        # Referential integrity: clean dependent rows (simple demo)
                        db_execute("DELETE FROM schedules WHERE course_code=%s", (r['code'],), commit=True)
                        db_execute("DELETE FROM enrollments WHERE course_code=%s", (r['code'],), commit=True)
                        db_execute("DELETE FROM faculty_courses WHERE course_code=%s", (r['code'],), commit=True)
                        db_execute("DELETE FROM grades WHERE course_code=%s", (r['code'],), commit=True)
                        db_execute("DELETE FROM courses WHERE code=%s", (r['code'],), commit=True)
                        st.success("Course and related records deleted.")
                        st.rerun()
                with c2:
                    st.caption("Edit UI can be added later.")

# --- Admin: Assign Faculty to Courses ---
def page_admin_faculty_courses():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Assign Faculty to Courses</h2>", unsafe_allow_html=True)

    faculty = db_execute("SELECT username FROM users WHERE role='faculty' ORDER BY username", fetchall=True) or []
    courses = db_execute("SELECT code, title FROM courses ORDER BY code", fetchall=True) or []
    if not faculty or not courses:
        st.info("Need at least one faculty user and one course in the catalog.")
        return

    fac_usernames = [f['username'] for f in faculty]
    course_codes = [f"{c['code']} — {c['title']}" for c in courses]
    code_by_label = {f"{c['code']} — {c['title']}": c['code'] for c in courses}

    with st.form("assign_faculty_form", clear_on_submit=True):
        sel_fac = st.selectbox("Faculty Username", fac_usernames)
        sel_course_label = st.selectbox("Course", course_codes)
        if st.form_submit_button("Assign", type="primary", use_container_width=True):
            course_code = code_by_label[sel_course_label]
            exists = db_execute(
                "SELECT 1 FROM faculty_courses WHERE username=%s AND course_code=%s",
                (sel_fac, course_code), fetchone=True
            )
            if exists:
                st.warning("This assignment already exists.")
            else:
                db_execute(
                    "INSERT INTO faculty_courses (username, course_code) VALUES (%s, %s)",
                    (sel_fac, course_code),
                    commit=True
                )
                st.success("Faculty assigned to course.")
                st.rerun()

    st.subheader("Current Assignments")
    rows = db_execute(
        """
        SELECT fc.username, fc.course_code, c.title
        FROM faculty_courses fc
        LEFT JOIN courses c ON c.code = fc.course_code
        ORDER BY fc.username, fc.course_code
        """, fetchall=True
    ) or []
    if not rows:
        st.caption("No assignments yet.")
    else:
        for r in rows:
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"- **{r['username']}** → {r['course_code']} — {r.get('title') or ''}")
            with col2:
                if st.button("Remove", key=f"remove_fc_{r['username']}_{r['course_code']}"):
                    db_execute("DELETE FROM faculty_courses WHERE username=%s AND course_code=%s",
                               (r['username'], r['course_code']), commit=True)
                    st.success("Assignment removed.")
                    st.rerun()

# --- Admin: Class Schedule Management ---
def page_admin_class_schedule():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Class Schedule</h2>", unsafe_allow_html=True)
    courses = db_execute("SELECT code, title FROM courses ORDER BY code", fetchall=True) or []
    if not courses:
        st.info("No courses found. Add courses first.")
        return

    labels = [f"{c['code']} — {c['title']}" for c in courses]
    code_by_label = {f"{c['code']} — {c['title']}": c['code'] for c in courses}
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    with st.form("add_schedule_form", clear_on_submit=True):
        sel_label = st.selectbox("Course", labels)
        sel_day = st.selectbox("Day", days, index=0)
        start_t = st.time_input("Start Time", value=dtime(9,0))
        end_t   = st.time_input("End Time", value=dtime(10,30))
        if st.form_submit_button("Add Slot", type="primary", use_container_width=True):
            if end_t <= start_t:
                st.error("End time must be after start time.")
            else:
                course_code = code_by_label[sel_label]
                # optional: check overlap
                overlap = db_execute(
                    """
                    SELECT 1 FROM schedules
                    WHERE course_code=%s AND day=%s
                      AND NOT (%s >= end_time OR %s <= start_time)
                    """,
                    (course_code, sel_day, start_t, end_t), fetchone=True
                )
                if overlap:
                    st.warning("Time slot overlaps an existing slot for this course.")
                else:
                    db_execute(
                        "INSERT INTO schedules (course_code, day, start_time, end_time) VALUES (%s,%s,%s,%s)",
                        (course_code, sel_day, start_t, end_t), commit=True
                    )
                    st.success("Time slot added.")
                    st.rerun()

    st.subheader("Current Schedule")
    q = st.text_input("Filter by course code", key="sched_filter")
    cond, params = "", []
    if q:
        cond = "WHERE s.course_code LIKE %s"
        params = [f"%{q}%"]

    rows = db_execute(
        f"""
        SELECT s.course_code, c.title, s.day, s.start_time, s.end_time
        FROM schedules s
        LEFT JOIN courses c ON c.code = s.course_code
        {cond}
        ORDER BY FIELD(s.day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), s.start_time, s.course_code
        """,
        params, fetchall=True
    ) or []

    if not rows:
        st.caption("No schedule entries.")
    else:
        for r in rows:
            col1, col2 = st.columns([5,1])
            with col1:
                st.markdown(f"- **{r['course_code']} — {r.get('title') or ''}** : {r['day']} {r['start_time']}–{r['end_time']}")
            with col2:
                if st.button("Delete", key=f"del_sched_{r['course_code']}_{r['day']}_{r['start_time']}"):
                    db_execute(
                        "DELETE FROM schedules WHERE course_code=%s AND day=%s AND start_time=%s AND end_time=%s",
                        (r['course_code'], r['day'], r['start_time'], r['end_time']), commit=True
                    )
                    st.success("Schedule entry deleted.")
                    st.rerun()

# ============================
# Faculty Pages
# ============================
def faculty_dashboard():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Faculty Dashboard</h2>", unsafe_allow_html=True)
    st.success(f"Welcome, {st.session_state.user['username']}!")
    st.info("Use the sidebar: Course Management, Grades, Files.")

def page_faculty_course_management():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Course Management</h2>", unsafe_allow_html=True)
    username = st.session_state.user['username']

    courses = db_execute(
        """
        SELECT c.code, c.title, c.credit as credit
        FROM courses c
        JOIN faculty_courses fc ON c.code = fc.course_code
        WHERE fc.username = %s
        ORDER BY c.title
        """,
        (username,), fetchall=True
    ) or []

    if not courses:
        st.info("No assigned courses.")
        return

    for c in courses:
        st.markdown(f"**{c['title']}** ({float(c['credit']):.1f} cr)")
        with st.expander("Roster"):
            roster = db_execute(
                """
                SELECT u.student_id, u.username
                FROM enrollments e
                JOIN users u ON u.student_id = e.student_id
                WHERE e.course_code = %s
                ORDER BY u.student_id
                """,
                (c['code'],), fetchall=True
            ) or []
            if not roster:
                st.caption("No students enrolled.")
            else:
                for r in roster:
                    st.markdown(f"- {r['student_id'] or r['username']}")
        sched = db_execute(
            """
            SELECT day, start_time, end_time
            FROM schedules
            WHERE course_code = %s
            ORDER BY FIELD(day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), start_time
            """,
            (c['code'],), fetchall=True
        ) or []
        if sched:
            st.caption("; ".join([f"{s['day']} {s['start_time']}–{s['end_time']}" for s in sched]))
        st.markdown("---")

def page_faculty_grades():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Enter Grades</h2>", unsafe_allow_html=True)
    username = st.session_state.user['username']

    courses = db_execute(
        """
        SELECT c.code
        FROM courses c
        JOIN faculty_courses fc ON c.code = fc.course_code
        WHERE fc.username = %s
        """,
        (username,), fetchall=True
    ) or []

    if not courses:
        st.info("No courses to grade.")
        return

    options = {f["code"]: f["code"] for f in courses}
    sel_label = st.selectbox("Select course:", list(options.keys()))
    course_code = options[sel_label]

    roster = db_execute(
        """
        SELECT u.student_id, u.username,
               (SELECT grade FROM grades g WHERE g.student_id = u.student_id AND g.course_code = %s LIMIT 1) AS grade
        FROM enrollments e
        JOIN users u ON u.student_id = e.student_id
        WHERE e.course_code = %s
        ORDER BY u.student_id, u.username
        """,
        (course_code, course_code), fetchall=True
    ) or []

    if not roster:
        st.info("No students enrolled.")
        return

    with st.form("grade_entry"):
        new_grades = {}
        for r in roster:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{r['student_id'] or r['username']}**")
            with col2:
                g = st.number_input(
                    f"Grade for {r['student_id']}",
                    min_value=0.0, max_value=4.0, step=0.01,
                    value=float(r['grade']) if r['grade'] is not None else 0.0,
                    key=f"grade_{r['student_id']}"
                )
                new_grades[r['student_id']] = g
        if st.form_submit_button("Save Grades", type="primary", use_container_width=True):
            for uid2, grd in new_grades.items():
                exists = db_execute(
                    "SELECT student_id FROM grades WHERE student_id = %s AND course_code = %s",
                    (uid2, course_code), fetchone=True
                )
                if exists:
                    db_execute(
                        "UPDATE grades SET grade = %s, updated_at = NOW() WHERE student_id = %s AND course_code = %s",
                        (grd, uid2, course_code), commit=True
                    )
                else:
                    db_execute(
                        "INSERT INTO grades (student_id, course_code, grade) VALUES (%s, %s, %s)",
                        (uid2, course_code, grd), commit=True
                    )
            st.success("✅ Grades saved.")
            st.rerun()

# ============================
# Shared: File Storage UI
# ============================
def file_storage():
    st.markdown("<h2 style='color:#003087;font-size:22px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>File Storage</h2>", unsafe_allow_html=True)
    st.info("Upload a text/image file or create a text file below:")

    user_key = st.session_state.user.get('student_id') or st.session_state.user.get('username') or st.session_state.user.get('id')

    with st.form("file_upload_form", clear_on_submit=True):
        action = st.radio("Choose an action", ("Upload File", "Create Text File"), horizontal=True, key="file_action_radio")
        file_name = st.text_input("File Name", placeholder="Enter file name (e.g., myfile)")
        file = None
        text_content = None
        if action == "Upload File":
            file = st.file_uploader("Choose a file", type=['txt', 'jpg', 'png'])
        else:
            text_content = st.text_area("Enter text content", placeholder="Type your text here...")
        if st.form_submit_button("Submit", type="primary", use_container_width=True):
            if not file_name:
                st.error("❌ Please provide a file name.")
            else:
                if upload_file(user_key, file_name, file=file, text_content=text_content):
                    st.rerun()

    st.subheader("Your Files")
    files = get_user_files(user_key)
    if files:
        for f in files:
            file_path = Path(f['file_path'])
            file_ext = file_path.suffix.lower()
            file_size = file_path.stat().st_size / 1024  # KB
            display_name = '_'.join(f['file_name'].split('_')[1:])
            st.markdown(f"{display_name} (Uploaded: {f['upload_date']} | Size: {file_size:.2f} KB)")
            with st.expander(f"Preview {display_name}"):
                if file_ext == ".txt":
                    try:
                        with open(file_path, "r", encoding="utf-8") as fh:
                            content = fh.read()
                        st.text(content)
                    except UnicodeDecodeError:
                        with open(file_path, "r", encoding="latin1") as fh:
                            content = fh.read()
                        st.text(content)
                elif file_ext in [".jpg", ".png"]:
                    st.image(file_path, caption=display_name, use_column_width=True)
            if st.button("Delete", key=f"delete_{f['file_name']}"):
                try:
                    file_path.unlink()
                    st.success(f"✅ File '{display_name}' deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Error deleting file: {e}")
    else:
        st.caption("No files uploaded yet.")

# ============================
# Sidebar (only after login)
# ============================
def render_sidebar():
    with st.sidebar:
        st.image("logo.jpg", width=40)
        if st.session_state.role == 'student':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Student Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['student_id']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="student_dashboard_btn"):
                st.session_state.current_page = 'student_dashboard'; st.rerun()
            if st.button("Course Advising", key="student_advising"):
                st.session_state.current_page = 'advising_enrollment'; st.rerun()
            if st.button("Class Schedule", key="student_schedule"):
                st.session_state.current_page = 'class_schedule'; st.rerun()
            if st.button("Grades", key="student_grades"):
                st.session_state.current_page = 'grades'; st.rerun()
            if st.button("File Storage", key="student_file_storage"):
                st.session_state.current_page = 'file_storage'; st.rerun()
            if st.button("Logout", key="student_logout", type="secondary"):
                confirm_logout()
        elif st.session_state.role == 'admin':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Admin Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['username']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="admin_dashboard"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'admin_dashboard'; st.rerun()
            if st.button("Add User", key="admin_add_user"):
                st.session_state.show_add_user = True
                st.session_state.current_page = 'admin_dashboard'; st.rerun()
            if st.button("User Management", key="admin_users"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'user_management'; st.rerun()
            if st.button("Course Catalog", key="admin_courses"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'admin_course_catalog'; st.rerun()
            if st.button("Assign Faculty", key="admin_faculty_courses"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'admin_faculty_courses'; st.rerun()
            if st.button("Class Schedule", key="admin_class_schedule"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'admin_class_schedule'; st.rerun()
            if st.button("File Storage", key="admin_file_storage"):
                st.session_state.show_add_user = False
                st.session_state.current_page = 'file_storage'; st.rerun()
            if st.button("Logout", key="admin_logout", type="secondary"):
                confirm_logout()
        elif st.session_state.role == 'faculty':
            st.markdown("<h2 style='color: #003087; font-size: 19px;'>Faculty Portal</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #374151; font-size: 19px;'>Hi, {st.session_state.user['username']}</p>", unsafe_allow_html=True)
            if st.button("Dashboard", key="faculty_dashboard"):
                st.session_state.current_page = 'faculty_dashboard'; st.rerun()
            if st.button("Course Management", key="faculty_courses"):
                st.session_state.current_page = 'course_management'; st.rerun()
            if st.button("Enter Grades", key="faculty_grades_btn"):
                st.session_state.current_page = 'faculty_grades'; st.rerun()
            if st.button("File Storage", key="faculty_file_storage"):
                st.session_state.current_page = 'file_storage'; st.rerun()
            if st.button("Logout", key="faculty_logout", type="secondary"):
                confirm_logout()

def confirm_logout():
    if st.session_state.get('logged_in'):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.login_attempts = 0
        st.session_state.locked = False
        st.session_state.lockout_time = None
        st.session_state.show_add_user = False
        st.session_state.current_page = None
        st.success("✅ Logged out successfully!")
        st.rerun()

# ============================
# Main App Logic (no sidebar on main page)
# ============================
def main():
    # ---------- Header ----------
    try:
        with open("logo.jpg", "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        encoded_logo = ""
    st.markdown(f"""
    <div class="header" style="display:flex;align-items:center;gap:12px;">
        {'<img src="data:image/jpeg;base64,' + encoded_logo + '" alt="Logo" style="width:30px;height:auto;border-radius:4px;">' if encoded_logo else ''}
        <h1 style="margin:0;font-weight:600;color:white;">Bangladesh Gen Z University Management System</h1>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Content ----------
    st.markdown("<div class='content'>", unsafe_allow_html=True)

    if not st.session_state.get('logged_in'):
        # Show login forms only (no sidebar here)
        if st.session_state.login_type == "Student":
            st.markdown("<h2 style='color:#FFFFFF;font-size:42px;font-weight:700;text-align:center;margin-bottom:0.5rem;'>Student Login</h2>", unsafe_allow_html=True)
            with st.form("student_login_form", clear_on_submit=True):
                st.markdown("<span class='input-label'>Student ID</span>", unsafe_allow_html=True)
                student_id_input = st.text_input("Student ID", placeholder="e.g., 2021-2-60-046", key="student_id", label_visibility="collapsed")
                st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
                password = st.text_input("Password", type="password", placeholder="Enter password", key="student_password", label_visibility="collapsed")
                st.markdown("<span class='input-label'>CAPTCHA</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='captcha-hint'>{st.session_state.captcha_question}</div>", unsafe_allow_html=True)
                captcha = st.text_input("CAPTCHA Answer", placeholder="Enter answer", key="student_captcha", label_visibility="collapsed")
                if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                    authenticate_student(student_id_input, password, captcha)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Forgot Password?", type="secondary", use_container_width=True, key="student_forgot"):
                    st.info("📧 Email it.support@ewu.edu for help.")
            with col2:
                if st.button("Admin/Faculty Login", type="secondary", use_container_width=True, key="switch_to_admin"):
                    switch_login_type("Admin"); st.rerun()
        else:
            st.markdown("""
            <div class="instruction">
                🔐 Authorized access only<br>
                📋 Activity logged<br>
                📞 Contact IT for support
            </div>
            <h2 style='color:#003087;font-size:19px;font-weight:600;text-align:center;margin-bottom:0.5rem;'>Admin/Faculty Login</h2>
            """, unsafe_allow_html=True)
            with st.form("admin_faculty_login_form", clear_on_submit=True):
                st.markdown("<span class='input-label'>Login as</span>", unsafe_allow_html=True)
                role = st.radio("Login as", ("Admin", "Faculty"), horizontal=True, key="admin_faculty_role", label_visibility="collapsed")
                st.markdown("<span class='input-label'>Username</span>", unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="Enter username", key="admin_username", label_visibility="collapsed")
                st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
                password = st.text_input("Password", type="password", placeholder="Enter password", key="admin_password", label_visibility="collapsed")
                st.markdown("<span class='input-label'>CAPTCHA</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='captcha-hint'>{st.session_state.captcha_question}</div>", unsafe_allow_html=True)
                captcha = st.text_input("CAPTCHA Answer", placeholder="Enter answer", key="admin_captcha", label_visibility="collapsed")
                if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                    authenticate_admin_faculty(username, password, role.lower(), captcha)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Forgot Password?", type="secondary", use_container_width=True, key="admin_forgot"):
                    st.info("📧 Email it.support@ewu.edu for help.")
            with col2:
                if st.button("Student Login", type="secondary", use_container_width=True, key="switch_to_student"):
                    switch_login_type("Student"); st.rerun()

    else:
        # Logged in: now render sidebar + content
        render_sidebar()
        if st.session_state.role == 'student':
            page_map = {
                'student_dashboard': student_dashboard,
                'advising_enrollment': page_advising_and_enrollment,
                'class_schedule': page_class_schedule,
                'grades': page_grades,
                'file_storage': file_storage
            }
        elif st.session_state.role == 'admin':
            page_map = {
                'admin_dashboard': admin_dashboard,
                'user_management': page_user_management,
                'admin_course_catalog': page_admin_course_catalog,
                'admin_faculty_courses': page_admin_faculty_courses,
                'admin_class_schedule': page_admin_class_schedule,
                'file_storage': file_storage
            }
        elif st.session_state.role == 'faculty':
            page_map = {
                'faculty_dashboard': faculty_dashboard,
                'course_management': page_faculty_course_management,
                'faculty_grades': page_faculty_grades,
                'file_storage': file_storage
            }
        else:
            page_map = {}

        current_page = st.session_state.current_page
        if current_page and current_page in page_map:
            page_map[current_page]()
        else:
            if st.session_state.role == 'student':
                st.session_state.current_page = 'student_dashboard'; student_dashboard()
            elif st.session_state.role == 'admin':
                st.session_state.current_page = 'admin_dashboard'; admin_dashboard()
            elif st.session_state.role == 'faculty':
                st.session_state.current_page = 'faculty_dashboard'; faculty_dashboard()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Footer ----------
    st.markdown("""
    <div class="footer">
        <div style="display:flex;align-items:center;justify-content:center;gap:0.8rem;flex-wrap:wrap;">
            <span>© 2025 Bangladesh Gen Z University Management System. All rights reserved.</span>
            <span>Contact: <a href="mailto:it.support@bangladeshgenzuniversity.edu">it.support@bangladeshgenzuniversity.edu</a> | Phone: +880 1234 567890 | <a href="https://www.ewu.edu">www.ewu.edu</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
