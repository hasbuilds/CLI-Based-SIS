# CLI-Based School Information System (CLI-Based-SIS) — v1

A command-line based School Information System (SIS) built with Python.  
The system is designed to help small schools manage student records, basic authentication, and data exports using a lightweight, offline-first approach.

> This project focuses on **practical problem-solving**, not frameworks.

---

## 📌 Problem Statement

Many small and rural schools:
- Rely heavily on paper-based student records
- Lack affordable school management software
- Face challenges in data organization, retrieval, and reporting
- Do not always have reliable internet access

**CLI-Based-SIS** addresses these issues by providing a simple, local, and easy-to-use system that runs entirely from the command line.

---

## 🎯 What This System Solves

- Eliminates paper-based student record keeping
- Centralizes student data in a structured format
- Reduces manual errors during registration and reporting
- Enables quick export of student data for reporting or backups
- Works **offline** with minimal hardware requirements

---

## ✨ Features (v1)

### 🔐 Admin Authentication
- Admin sign-up and login
- Basic input validation
- Password confirmation during registration

### 👨‍🎓 Student Management
- Register new students
- Remove existing students
- View a formatted list of all registered students
- Store:
  - Full name
  - Sex
  - Date of birth
  - Class level
  - Year of admission

### 📁 Data Persistence
- Admin data stored in JSON
- Student records stored in JSON
- Automatic file creation and updates

### 📤 Data Export
- Export student records to:
  - Excel (`.xlsx`)
- Enables easy sharing and reporting

### 🖥️ Command-Line Interface
- Menu-driven navigation
- Clear prompts and feedback
- Error handling for invalid inputs

---

## 🗂️ Project Structure (v1)

```text
CLI-Based-SIS/
│
├── main.py                 # Main application entry point
├── admin_data.json         # Stores admin credentials and details
├── students_data.json      # Stores student records
└── requirements.txt        # Project dependencies
