# 🚀 DevOps Server Automation Toolkit

A collection of DevOps automation scripts for Linux server setup, website deployment, server configuration, database management, and development environment setup.

This toolkit helps developers and system administrators automate common server tasks and reduce manual work.

---

# 📌 Project Overview

Managing a server manually requires many steps such as:

- Installing required software
- Configuring Apache and Nginx
- Creating databases
- Managing PHP versions
- Deploying applications
- Testing email services
- Managing server configurations


This project provides ready-to-use automation scripts that make these tasks faster, easier, and more reliable.

---

# 📁 Project Structure

```
DevOps/

├── menu.py
│
├── README.md
│
├── bash/
│
│   ├── basic_tool_install_on_the_server.sh
│   ├── apache_virtualhost_setup.sh
│   ├── change_php_version.sh
│   ├── create_db.sh
│   └── laravel_project_setup.sh
│
└── python/
│
    ├── email_testing.py
    └── nginx_virtualhost_setup.py
    └── ssh_connect.py
```

---

# ⚙️ Requirements

## Operating System

Supported:

- Ubuntu 22.04+
- Debian based Linux systems


## Required Access

Before running scripts, make sure you have:

- Root access
- sudo permission
- Internet connection


## Required Software

Depending on the script, you may need:

- Bash
- Python 3
- PHP
- Composer
- MySQL
- Apache
- Nginx


---

# 🚀 Installation


Clone the repository:

```bash
git clone https://github.com/balmikiii/DevOps.git
```


Go to project directory:

```bash
cd DevOps
```


Give permission to shell scripts:

```bash
chmod +x bash/*.sh
```


Now run the required script according to your requirement.

---

# 📜 Scripts Usage


## 🖥️ 1. Server Basic Setup
### Menu

```
python menu.py
```

### Description

List all menus

### Script

```
bash/basic_tool_install_on_the_server.sh
```


### Run Command

```bash
sudo ./bash/basic_tool_install_on_the_server.sh
```


### Description

This script prepares a fresh Linux server for development and hosting.

It installs common tools, PHP environment, Node.js, SSH service, and basic firewall configuration.

Use this script when setting up a new VPS or server.


---

## 🌐 2. Apache Virtual Host Setup


### Script

```
bash/apache_virtualhost_setup.sh
```


### Run Command

```bash
sudo ./bash/apache_virtualhost_setup.sh
```


### Description

This script creates and configures websites on an Apache server.

It automatically prepares virtual host configuration and makes the server ready to host domains.

Use it when you need to deploy a website using Apache.


---

## ⚡ 3. PHP Version Switch


### Script

```
bash/change_php_version.sh
```


### Run Command

```bash
sudo ./bash/change_php_version.sh
```


### Description

This script helps to switch PHP versions on an Apache server.

It is useful when different projects require different PHP versions.

Example:

- Project A requires PHP 8.1
- Project B requires PHP 8.2


---

## 🗄️ 4. MySQL Database Setup


### Script

```
bash/create_db.sh
```


### Run Command

```bash
sudo ./bash/create_db.sh
```


### Description

This script creates a MySQL database and user automatically.

It helps developers quickly prepare a database environment for new applications.

Useful for:

- New project setup
- Laravel applications
- Website deployment


---

## 🚀 5. Laravel Project Setup


### Script

```
bash/laravel_project_setup.sh
```


### Run Command

```bash
./bash/laravel_project_setup.sh
```


### Description

This script automates Laravel project deployment.

It helps configure the application, install dependencies, prepare environment settings, and complete common deployment tasks.

Useful for:

- Laravel deployment
- Production setup
- Server migration


---

## 📧 6. SMTP Email Testing


### Script

```
python/email_testing.py
```


### Run Command

```bash
python3 python/email_testing.py
```


### Description

This script is used to test SMTP email sending functionality.

It helps verify that email configuration is working correctly before using email features inside an application.

Supports:

- Gmail SMTP
- Custom SMTP servers


---

## 🌍 7. Nginx Virtual Host Setup


### Script

```
python/nginx_virtualhost_setup.py
```


### Run Command

```bash
sudo python3 python/nginx_virtualhost_setup.py
```


### Description

This script automates Nginx website configuration.

It helps create a new website setup, configure Nginx, and make deployment easier.

Useful for:

- VPS hosting
- Multiple websites
- Nginx based servers


---

## 🌍 8. Connect SSH if exist details in ~/.ssh/config


### Script

```
python/ssh_connect.py
```


### Run Command

```bash
sudo python3 python/ssh_connect.py
```


### Description

This script detect you system configs ssh host name.

Useful for:

- List all ssh name

---

# 🔐 Security Recommendations


Never upload sensitive information:

- Passwords
- Database credentials
- SMTP passwords
- API keys
- Private configuration files


Always use:

- Environment variables
- `.env` files
- Secure credential management


---

# 🛠 Useful Server Commands


## Check PHP Version

```bash
php -v
```


## Check Python Version

```bash
python3 --version
```


## Check Node Version

```bash
node -v
```


## Check MySQL Status

```bash
sudo systemctl status mysql
```


## Check Apache Status

```bash
sudo systemctl status apache2
```


## Check Nginx Status

```bash
sudo systemctl status nginx
```


---

# 🎯 Use Cases


This toolkit can be used for:

- VPS server setup
- Website deployment
- Laravel hosting
- PHP application deployment
- Database management
- Server automation
- Development environment setup
- Linux server administration


---

# 💼 Freelance & Hiring


Need help with server setup, deployment, or development work?


Available services:


- 🖥️ Linux VPS Setup
- 🌐 Apache Configuration
- 🌍 Nginx Configuration
- 🚀 Laravel Deployment
- 🐘 PHP Application Setup
- 🗄️ Database Configuration
- 🔒 SSL Setup
- ⚙️ DevOps Automation
- 🔧 Server Management


For freelance projects, technical support, project deployment, or hiring requirements, feel free to contact.

---

# 📞 Contact


📧 **Email**

```
balmikiii@hotmail.com
```


🐙 **GitHub**

```
https://github.com/balmikiii
```


💼 **LinkedIn**

```
https://www.linkedin.com/in/balmikikumar/
```


📸 **Instagram**

```
https://instagram.com/balmikiii
```


---

# ⭐ Support


If this project helps you:

- Give a star ⭐
- Share with developers
- Suggest improvements


---

# 📜 License


Free to use for learning, development, and automation purposes.

---

## Author

Balmiki Kumar