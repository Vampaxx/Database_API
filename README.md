# Flask MySQL Authentication API


## Introduction

This project is a REST API built with Flask, using MySQL for data storage and JWT for authentication. It allows user signup, login, retrieval, update, and deletion of user accounts.

### Features

- User Registration: Allows users to sign up with an email and password.
- User Login: Users can log in and receive a JWT token for subsequent requests.
- JWT Authentication: Endpoints are protected with JWT tokens.
- CRUD Operations:

    - Create new accounts.
    - Retrieve all accounts or a specific account by email.
    - Update an existing account.
    - Delete accounts.

### Enter the Document Summarizer: Your Efficient Reading Companion

The Document Summarizer acts as a smart assistant that allows users to upload documents and receive concise summaries, saving time and effort while enhancing productivity.

## Requirements

  - Python 3.9
  - MySQL Database
  - Flask
  - Flask-MySQLdb
  - Flask-JWT-Extended
  - python-dotenv

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vampaxx/Database_API
   cd Database_API
   
2. **Open VScode:**
   ```bash
   code . 
3. **Set up a virtual environment:**
    ```bash
    conda activate [your environment name]
4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
5. **Add your API key into .env:**
    ```bash
    db_host      = your_mysql_host      
    db_user      = your_mysql_username  
    db_password  = your_mysql_password  
    db_name      = your_database_name      
    secret_key   = your_jwt_secret_key   
6. **Configure MySQL:**
Ensure your MySQL server is running, and create the necessary database and table:
    ```bash
    CREATE DATABASE user_database;
    
    USE User_database;
    
    CREATE TABLE sign_up (
        account_id 	INT AUTO_INCREMENT PRIMARY KEY,    
        email 		VARCHAR(100) UNIQUE NOT NULL,      
        passwords 	VARCHAR(255) NOT NULL,             
        created_at 	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  7. **Running the Application**

    ```bash
    python app.py
