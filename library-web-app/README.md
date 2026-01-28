# Library Management Web App

A simple library management app built using flask and sqlite database.

## Features

### Authentication
- User login using username and password
- Passwords are securely hashed using **bcrypt**
- JWT is generated on successful login
- JWT is stored in **HTTP-only cookies**
- Logout clears authentication token
- Unauthenticated users are redirected to login page

---

### Admin Features
- Login to admin dashboard
- Add new books to the library
- View all books (both available and issued)

> Note: Edit, delete, and borrowed history features are intentionally not implemented as per modified role requirements. I will add them later !

---

### Member Features
- Login to member dashboard
- View only available books

> Note: Borrow and return functionality is not implemented as per modified role requirements. I will add them later !

---

## 📥 Cloning the Repository

```bash
git clone <your-repository-url>
cd library-web-app
```

## Installation and Setup steps

### 1. Create a virtual environment
```python
python -m venv <your_venv>
your_venv\Scripts\activate
```


### 2. Install the dependencies
```python
pip install -r requirements.txt
```

### 3. Run the application ( Make sure you are in the right directory )
```python 
python app.py
# access the application on localhost:<port>
```
