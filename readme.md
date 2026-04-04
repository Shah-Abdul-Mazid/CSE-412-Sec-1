<p align="center">
  <img src="logo.jpg" alt="Bangladesh University Management System Logo" width="120"/>
</p>

<h1 align="center">🎓 Bangladesh University Management System</h1>

<p align="center">
  <b>A full-featured, role-based university management web application built with Python, Streamlit, and MySQL.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/PyMySQL-1.1-00758F?style=for-the-badge&logo=database&logoColor=white" alt="PyMySQL"/>
  <img src="https://img.shields.io/badge/License-Academic-green?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <code>CSE-412</code> · <code>Database Management System</code> · <code>Section 1</code> · <code>East West University</code>
</p>

---

## 📋 Description

The **Bangladesh University Management System** is a comprehensive web-based platform designed to digitize and streamline core university operations. Built as a course project for **CSE-412: Database Management System (Section 1)** at **East West University**, the system provides dedicated portals for three user roles — **Students**, **Faculty**, and **Administrators** — each with tailored dashboards and functionalities.

The application features a fully relational MySQL database backend with 12 interconnected tables, secure role-based authentication with CAPTCHA verification and account lockout protection, and an intuitive Streamlit-powered frontend with custom CSS styling and responsive design.

---

## 🏷️ Tags

`university-management-system` · `streamlit` · `python` · `mysql` · `pymysql` · `role-based-access-control` · `student-portal` · `course-enrollment` · `grade-management` · `class-scheduling` · `academic-advising` · `file-storage` · `database-project` · `cse412` · `east-west-university` · `crud-operations` · `web-application` · `bangladesh`

---

## ✨ Features

### 🔐 Authentication & Security
- Role-based login (Student, Faculty, Admin) with separate login portals
- Math-based CAPTCHA verification on every login attempt
- Account lockout after 5 failed attempts (5-minute cooldown)
- Session state management with secure logout

### 👨‍🎓 Student Portal
| Feature | Description |
|---------|-------------|
| **Dashboard** | Personalized welcome page with navigation guidance |
| **Course Advising & Enrollment** | Browse, search, enroll in, and drop courses with real-time schedule preview |
| **Class Schedule** | View weekly schedule organized by day and time |
| **Grades** | View course grades with weighted GPA calculation |
| **File Storage** | Upload (`.txt`, `.jpg`, `.png`), create text files, preview, and delete personal files |

### 👨‍🏫 Faculty Portal
| Feature | Description |
|---------|-------------|
| **Dashboard** | Welcome page with quick navigation |
| **Course Management** | View assigned courses, student rosters, and class schedules |
| **Grade Entry** | Enter and update numeric grades (0.0–4.0) for enrolled students |
| **File Storage** | Personal file upload and management |

### 🛡️ Admin Portal
| Feature | Description |
|---------|-------------|
| **Dashboard** | Overview with quick-access Add User form |
| **User Management** | Search and view all users by username, email, or student ID |
| **Add User** | Create new student, faculty, or admin accounts with optional custom timestamps |
| **Course Catalog (CRUD)** | Create courses with code, title, credits, description; delete with cascading cleanup |
| **Faculty Assignment** | Assign/remove faculty members to/from courses |
| **Class Schedule** | Add/delete time slots per course per day with overlap detection |
| **File Storage** | Personal file upload and management |

---

## 🗄️ Database Schema

The MySQL database (`university_management_system2`) consists of **12 tables**:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│      users       │     │     courses       │     │    schedules     │
├──────────────────┤     ├──────────────────┤     ├──────────────────┤
│ sl (PK)          │     │ id (PK)          │     │ id (PK)          │
│ username (UQ)    │     │ name             │     │ course_id (FK)   │
│ password         │     │ description      │     │ start_time       │
│ email (UQ)       │     │ credits          │     │ end_time         │
│ role             │     │ created_at       │     │ day              │
│ student_id       │     │ updated_at       │     │ created_at       │
│ created_at       │     └──────────────────┘     │ updated_at       │
│ updated_at       │                               └──────────────────┘
└──────────────────┘
```

| Table | Purpose |
|-------|---------|
| `users` | Stores all user accounts (students, faculty, admins) |
| `courses` | Course catalog with code, title, credits, description |
| `enrollments` | Maps students to their enrolled courses |
| `grades` | Stores numeric grades per student per course |
| `schedules` | Weekly class time slots (day + start/end time) |
| `faculty_courses` | Maps faculty members to their assigned courses |
| `advising` | Advising meeting records between students and advisors |
| `assignments` | Course assignment definitions with due dates |
| `submissions` | Student assignment submissions and grading |
| `attendance` | Per-class attendance tracking (present/absent/late) |
| `feedback` | Student course feedback and evaluations |
| `ledgers` | Financial transaction records (credit/debit) |
| `logs` | User activity audit trail |
| `notifications` | User notification messages with read status |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | [Streamlit](https://streamlit.io/) v1.46+ with custom CSS |
| **Backend** | Python 3.10+ |
| **Database** | MySQL 8.0 |
| **DB Driver** | PyMySQL 1.1 |
| **Fonts** | Google Fonts (Roboto) |
| **File Storage** | Local filesystem (per-user directories) |

### Key Dependencies
```
streamlit==1.46.1
PyMySQL==1.1.1
pandas==2.3.0
pillow==11.2.1
Flask==3.1.1
streamlit-authenticator==0.4.2
streamlit-option-menu==0.4.0
```

---

## 🚀 Getting Started

### Prerequisites
- **Python** 3.10 or higher
- **MySQL** 8.0 or higher (running on `127.0.0.1:9000`)
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shah-Abdul-Mazid/CSE-412-Sec-1.git
   cd CSE-412-Sec-1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   - Start your MySQL server on port `9000`
   - Create the database and import the schema:
     ```sql
     CREATE DATABASE university_management_system2;
     USE university_management_system2;
     SOURCE University_Management_System.sql;
     ```
   - Update the connection config in `app.py` if your MySQL host/port/credentials differ:
     ```python
     host='127.0.0.1',
     port=9000,
     user='root',
     password='root',
     database='university_management_system2'
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**  
   Navigate to `http://localhost:8501`

### Default Login Credentials

| Role | Username / Student ID | Password |
|------|----------------------|----------|
| **Admin** | `admin` | `admin` |
| **Student** | `2021-2-60-046` | `Mazid046` |
| **Student** | `2022-1-60-328` | `Monisha123` |

---

## 📁 Project Structure

```
CSE-412-Sec-1/
├── app.py                              # Main application (1180 lines)
├── University_Management_System.sql    # Database schema & seed data
├── requirements.txt                    # Python dependencies
├── logo.jpg                            # University logo
├── readme.md                           # This file
├── .gitignore                          # Git ignore rules
├── hi.txt                              # Welcome message
│
├── Admin/                              # Admin uploaded files
│   └── *.txt
│
├── 2021-2-60-046/                      # Student file storage (Shah Abdul Mazid)
│   └── *.txt, *.png
│
├── 2022-1-60-328/                      # Student file storage (Monisha)
│   └── *.txt
│
└── 2022-1-60-396/                      # Student file storage
    └── *.txt
```

---

## 👥 Team Members

| Name | Student ID | Email |
|------|-----------|-------|
| Shah Abdul Mazid | 2021-2-60-046 | 2021-2-60-046@std.ewubd.edu |
| Monisha Bani Nibedita Shuci | 2022-1-60-328 | 2022-1-60-328@std.ewubd.edu |

---

## 📚 Course Information

| | |
|---|---|
| **Course** | CSE-412: Database Management System |
| **Section** | 1 |
| **University** | East West University, Bangladesh |
| **Semester** | 2025 |

---

## 📄 License

This project is developed for academic purposes as part of the CSE-412 course at East West University. All rights reserved by the respective authors.

---

<p align="center">
  Made with ❤️ at <b>East West University, Bangladesh</b>
</p>