# 📦 ECR App – Electronic Collection & Retail Management System

> 🚀 A role-based web application built using Flask + MySQL to manage distributor inventory, product listings, and collections from retail shops.


---

## 🛠 Tech Stack

- Frontend: HTML, Bootstrap 5
- Backend: Python (Flask)
- Database: MySQL
- Templating: Jinja2

---

## 👤 User Roles & Access

| Role         | Permissions                                                                 |
|--------------|------------------------------------------------------------------------------|
| Distributor  | ➕ Add/Edit/Delete Products, 💰 Add Dues                                      |
| Salesman     | 💸 Collect Dues, View Retailer Dues                                          |
| Retailer     | 🛍️ View Products, Place Orders *(optional)*                                 |

---

## 📁 Project Structure

ecr_app/
├── app.py
├── db_config.py
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── products.html
│   ├── add_product.html
│   ├── edit_product.html
│   └── collections.html
├── static/
│   └── images/
└── README.md

---

## 🗃️ Database Schema (MySQL)

- users: `id`, `username`, `password`, `role`
- products: `id`, `name`, `price`, `purchase_price`, `company`, `image_url`
- collections: `id`, `username`, `amount`

📌 Import with `ecr_app.sql`

---

## 🔑 Sample Credentials

| Role        | Username     | Password     |
|-------------|--------------|--------------|
| Distributor | `admin`      | `admin2211`  |
| Salesman    | `suresh`     | `suresh123`  |
| Retailer    | `sbe`        | `sai123`    |

---

## 🖥️ How to Run Locally

```bash
# Step 1: Clone the repo
git clone https://github.com/sirin1735/ECR-App.git
cd ECR-App

# Step 2: Install requirements
pip install flask mysql-connector-python

# Step 3: Set up the MySQL database and import schema

# Step 4: Run the app
python3 app.py
