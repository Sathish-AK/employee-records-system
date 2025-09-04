# 🏢 Employee Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **Django-based Employee Management System** with a dynamic Form Builder.  
Users can register, log in, create custom forms, and add employees using those forms.  
Includes JWT-secured REST APIs for integration.  

---

## ✨ Features

- 🔐 **User Authentication**
  - Register, Login, Profile Management, Change Password  
  - Strong password validation + Show/Hide toggle  

- 📋 **Dynamic Form Builder**
  - Create forms with text, number, password, and date fields  
  - Drag-and-drop field ordering  
  - Required field validation  
  - Prevent duplicate field names  

- 👨‍💼 **Employee Management**
  - Create, edit, delete employees with custom forms  
  - Mask password fields in employee list  
  - Search employees by ID, Form Name, or Field Data  

- ⚡ **REST APIs (JWT Secured)**  
  - Token-based authentication  
  - Employee & Form APIs  

- 🎨 **Modern UI**  
  - Bootstrap-based, responsive, and clean design  

---

## ⚙️ Requirements

- Python **3.8+**  
- pip (Python package manager)  
- Git  

(Optional but recommended: Virtual environment `venv`)  

---

## 🚀 Quick Start

```bash
git clone https://github.com/your-username/employee-management-system.git
cd employee-management-system

# Linux/Mac
chmod +x install.sh
./install.sh

# Windows
install.bat
