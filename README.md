# Bitespeed

# Bitespeed Backend Task: Identity Reconciliation

This project is a **FastAPI-based backend service** that implements **identity reconciliation** for Bitespeed. It links multiple customer orders placed with different contact details (emails/phone numbers) into a single **primary contact** to ensure seamless customer experience.


##  **Installation Guide**
### **Clone the Repository**
```sh
git clone https://github.com/Srihari-12/Bitespeed.git
cd bitespeed-backend-task
```
### Install the dependencies
```sh
pip install -r requirements.txt
```

### **Database Connection**
#### Start mysql server
```sh
mysql -u root -p
```
#### Create Database
```
create database bitespeed;
```

### env file
#### Ensure your env file contains 
```sh
DATABASE_URL=mysql+pymysql://root:password@localhost/bitespeed
```


