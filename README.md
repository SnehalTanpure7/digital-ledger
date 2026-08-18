SmartKhata – Digital Ledger Management System

SmartKhata is a digital ledger management system designed to help shopkeepers manage customer credit and payment records digitally. It replaces 
traditional notebook-based ledgers with an organized and easy-to-use web application.

✨ Features
👤 Customer Management – Add and manage customer details
💰 Credit/Udhaar Management – Record customer credit transactions
💳 Payment Tracking – Record payments made by customers
⏳ Pending Amounts – Easily view outstanding balances
✅ Completed Transactions – Track fully paid accounts
📜 Transaction History – Maintain a complete record of transactions
📊 Dashboard – View important customer and payment information
🔐 Shopkeeper Login – Secure access to shopkeeper records
📅 Date & Time Tracking – Store transaction date and time
📱 Future SMS Notifications – Planned feature for notifying customers about new credit and payments

🛠️ Technologies Used
Python
Flask
SQLite
HTML5
CSS3
Bootstrap
JavaScript
Jinja2

📂 Project Structure
digital-ledger/
│
├── app.py
├── function.py
├── templates/
├── static/
├── .gitignore
└── README.md

⚙️ How to Run the Project
1. Clone the repository
   git clone https://github.com/SnehalTanpure7/digital-ledger.git
2. Open the project
   cd digital-ledger
3. Create a virtual environment
   python -m venv venv
4. Activate the virtual environment
   Windows: venv\Scripts\activate
5. Install required packages
   pip install -r requirements.txt
6. Run the Flask application
   python app.py
Then open the local URL shown in the terminal.


🔒 Data & Security

The project uses SQLite for local data storage. Database files and environment variables are excluded from the Git repository using .gitignore.
Sensitive information such as passwords, API keys, and secret configuration should not be committed to GitHub.

🚀 Future Enhancements
📱 SMS notifications for customers
🔔 Payment and credit reminders
📈 Advanced reports and analytics
📊 Monthly transaction summaries
📄 Export transactions to PDF/Excel
🔐 Improved authentication and security
☁️ Cloud database support
🎯 Project Goal

The goal of SmartKhata is to provide shopkeepers with a simple, digital, and organized way to manage customer credit and payment records while reducing dependency on traditional paper-based ledgers.



👩‍💻 Developer
Snehal Tanpure
Computer Technology Student
