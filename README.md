# Hierarchical Key Management System
HKMS is an advanced key management solution designed to provide organizations with a flexible and secure way to manage and control encryption keys. By establishing a hierarchical key structure, HKMS allows different levels of users or systems to access specific data based on their permissions. This structure not only improves security, but also simplifies the process of key management and distribution.
## Installation
First, you need to modify the `setting.py` file (Before that, it is necessary to install the MySQL database)
```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'keymanage',   #your mysql database name
        'USER':'root',         #your mysql username
        'PASSWORD':'123456',   #your mysql password
        'HOST':'127.0.0.1',
        'PORT':3306,
    }
}
```
Then, execute the following code in the terminal to install the required libraries
```
pip install -i requirements.txt
```
Afterwards, create tables in the database and execute the following command
```
python manage.py makemigrations
python manage.py migrate
```
Finally, execute the following code in the terminal to run the project
```
python manage.py runserver
```
## Screenshot
![image](https://github.com/user-attachments/assets/1d1444a7-4310-46ef-867d-2e3e36b03b08)
