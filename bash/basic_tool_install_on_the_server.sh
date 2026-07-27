#!/bin/bash

set -e

echo "=================================="
echo " Basic Server Setup with PHP + Node.js development Environment "
echo "=================================="

### TIMEZONE SET
read -p "Enter timezone (e.g. Asia/Kolkata): " TZ
sudo timedatectl set-timezone "$TZ"
echo "Timezone set to $TZ"

### UPDATE SYSTEM
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

### BASIC TOOLS
echo "Installing basic tools..."
sudo apt install -y \
curl \
wget \
git \
unzip \
zip \
software-properties-common \
nano \ 
htop

### PHP INSTALLATION
echo "Installing PHP and required extensions..."
sudo apt install -y \
php \
libapache2-mod-php \
php-cli \
php-common \
php-mysql \
php-fpm \
php-curl \
php-mbstring \
php-xml \
php-zip \
php-bcmath \
php-gd \
php-intl \

PHP_VERSION=$(php -r "echo PHP_VERSION;")
echo "PHP Installed: $PHP_VERSION"

### NODE.JS INSTALL (LTS)
echo "Installing Node.js (LTS)..."

curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)

echo "Node Installed: $NODE_VERSION"
echo "NPM Installed : $NPM_VERSION"


# ---------------------------
# CHECK OPENSSH SERVER
# ---------------------------
if ! dpkg -l | grep -qw openssh-server; then
    echo "OpenSSH Server is not installed."
    echo "Installing OpenSSH Server..."

    sudo apt update
    sudo apt install -y openssh-server

    sudo systemctl enable ssh
    sudo systemctl start ssh

    echo "✅ OpenSSH Server installed successfully."
else
    echo "✅ OpenSSH Server is already installed."

    sudo systemctl enable ssh
    sudo systemctl start ssh
fi

echo ""
echo "OpenSSH Status:"
systemctl is-active ssh


### FIREWALL SETUP (UFW)
echo "Configuring Firewall (UFW)..."

sudo apt install -y ufw

sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443

sudo ufw --force enable

echo "Firewall Status:"
sudo ufw status

### DONE
echo "=================================="
echo " Base Setup Completed Successfully "
echo "=================================="
echo "Timezone : $TZ"
echo "PHP      : $PHP_VERSION"
echo "Node     : $NODE_VERSION"
echo "NPM      : $NPM_VERSION"
echo "Firewall : Enabled (SSH, HTTP, HTTPS allowed)"
echo "Tools    : curl, wget, git, htop installed"
echo "=================================="


