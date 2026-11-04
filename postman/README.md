# MediTrack - Smart Pharmacy Management System 🏥

A full-stack Pharmacy Inventory & Order Management System developed to replace manual tracking with a modern, digital solution. 

## 🚀 Features
- **Secure Authentication:** JWT-based login with Role-Based Access Control (Admin, Pharmacist, Customer).
- **Inventory Management:** Complete CRUD (Create, Read, Update, Delete) functionality for medicines.
- **Live Analytics Dashboard:** Visualized stock distribution, total revenue, and low-stock alerts using Chart.js.
- **Order Processing:** Automated stock deduction when an order is placed using SQL transactions.
- **Search & Filter:** Real-time frontend search by medicine name or manufacturer.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, Flask-JWT-Extended
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Tools:** Postman, MySQL Workbench, Git

## ⚙️ How to Run Locally
1. Clone the repository:
   `git clone https://github.com/SreeTakshaj/meditrack-pharmacy-management.git`
2. Navigate to the backend folder:
   `cd backend`
3. Create and activate a virtual environment:
   `python -m venv venv`
   `venv\Scripts\activate` (Windows)
4. Install dependencies:
   `pip install -r requirements.txt`
5. Set up the database:
   - Create a MySQL database named `meditrack_db`.
   - Run the SQL script located in `backend/database/schema.sql`.
6. Create a `.env` file in the backend directory and add your credentials:
   ```env
   DB_PASSWORD=your_mysql_password
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret