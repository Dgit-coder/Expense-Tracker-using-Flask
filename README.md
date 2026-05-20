# Expense Tracker Application – Overview

The Expense Tracker is a web-based application developed using the Flask framework and SQLite database. The main purpose of this project is to help users manage and track their daily expenses efficiently through a simple and user-friendly interface.

The application provides a complete expense management system with user authentication features such as signup, login, and logout. After logging in, users can add expenses with details like date, expense name, and amount spent. All expense records are stored in a SQLite database and displayed on the dashboard along with the total expense calculation.

The project follows CRUD operations:

* **Create** → Add new expenses
* **Read** → View all expenses
* **Delete** → Remove unwanted expenses

Additionally, the application includes a monthly expense filtering feature that allows users to view expenses and total spending for a particular month and year.

The backend is built using Flask routes, session management, and SQL queries, while the frontend is handled using HTML templates rendered through Flask’s `render_template()` function.

## Key Features

* User Signup and Login System
* Session-based Authentication
* Add and Delete Expenses
* Monthly Expense Report
* Automatic Total Expense Calculation
* SQLite Database Integration
* Simple and Responsive Interface

## Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **HTML/CSS**
* **Jinja2 Templates**

## Working Flow

1. User registers or logs into the application.
2. After authentication, the dashboard is displayed.
3. Users can add expense details.
4. Expenses are stored in the SQLite database.
5. The dashboard shows all expenses and total spending.
6. Users can filter expenses month-wise or delete records when required.

## Objective of the Project

The objective of this project is to provide a simple and effective solution for personal expense management while demonstrating the implementation of Flask, database connectivity, session handling, and CRUD operations in web development.
