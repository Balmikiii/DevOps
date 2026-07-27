#!/bin/bash

set -euo pipefail

# -----------------------------
# Check MySQL Installation
# -----------------------------
if ! command -v mysql >/dev/null 2>&1; then
    echo "MySQL is not installed. Installing..."

    sudo apt update
    sudo apt install -y mysql-server

    sudo systemctl enable mysql
    sudo systemctl start mysql
else
    echo "MySQL is already installed."

    sudo systemctl enable mysql
    sudo systemctl start mysql
fi


# Input
read -rp "MySQL Database Name: " DB_NAME
read -rp "MySQL Username: " DB_USER
read -rp "MySQL Password: " DB_PASS

# Basic validation
if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASS" ]]; then
  echo "❌ Error: DB name, user or password cannot be empty"
  exit 1
fi

SERVER_IP=$(hostname -I | awk '{print $1}')
if [[ -z "$SERVER_IP" ]]; then
  SERVER_IP="localhost"
fi

echo "Starting MySQL service..."
sudo systemctl enable mysql
sudo systemctl start mysql

echo "Creating Database & User..."
# Safer mysql execution (no sudo mysql assumption)
mysql -u root -p <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php > /dev/null
echo "MySQL Status:"
systemctl is-active mysql
echo "====================================="
echo "Setup Completed Successfully"
echo "====================================="
echo "Database Name : $DB_NAME"
echo "Database User : $DB_USER"
echo "Database Password : $DB_PASS"
echo "PHP Test URL  : http://$SERVER_IP/info.php"
echo "====================================="
