 RBAC-Driven Access Management System with Real-Time Audit Logs

->  Overview-:
This project implements a secure Role-Based Access Control (RBAC) driven access management system that restricts user actions based on assigned roles. It integrates authentication, authorization, and real-time audit logging to enhance security, accountability, and compliance.

The system is designed to demonstrate enterprise-level access control concepts commonly used in secure applications.

 ✨ Features
- Secure user authentication with hashed passwords
- Role-Based Access Control (RBAC) enforcement
- Multiple roles: Admin, Manager, User, Auditor
- Role-specific permissions for system actions
- Real-time audit logging of user activities
- Admin-controlled user management
- Clean and user-friendly web interface

 👥 User Roles & Permissions

| Role     | Permissions |
|---------|-------------|
| Admin   | Read, Write, Delete, Manage Users, View Logs |
| Manager| Read, Write |
| User    | Read |
| Auditor | View Logs |


 🛠️ Technologies Used
- Python
- Streamlit (Frontend & App Framework)
- Pandas (Data handling)
- bcrypt (Password hashing & security)


 🚀 How to Run the Project
1-> pip install -r requirements.txt

2-> Run the Application
streamlit run app.py

3️ ->Open in Browser
http://localhost:8501

🔐 Default Admin Login
Username: admin
Password: admin123
Role: Admin

