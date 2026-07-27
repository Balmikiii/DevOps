#!/bin/bash

set -e

echo "======================================"
echo " Apache Virtual Host + SSL Setup "
echo "======================================"

# ---------------------------
# CHECK APACHE INSTALLATION
# ---------------------------
if ! command -v apache2 >/dev/null 2>&1; then
    echo "Apache2 is not installed."
    echo "Installing Apache2..."

    sudo apt update
    sudo apt install -y apache2

    sudo systemctl enable apache2
    sudo systemctl start apache2

    echo "✅ Apache2 installed successfully."
else
    echo "✅ Apache2 is already installed."

    sudo systemctl enable apache2
    sudo systemctl start apache2
fi

# ---------------------------
# ENABLE APACHE MODULES
# ---------------------------
echo ""
echo "Enabling Apache modules..."

sudo a2enmod rewrite
sudo a2enmod headers

echo ""
echo "Apache Status:"
systemctl is-active apache2

# ---------------------------
# DOMAIN VALIDATION LOOP
# ---------------------------
while true; do
    read -p "Enter Domain Name (example.com): " DOMAIN

    if [[ "$DOMAIN" == *.* ]]; then
        break
    else
        echo "❌ Invalid domain!"
        echo "👉 Hint: use like example.com or prestashop.com"
    fi
done

# ---------------------------
# DOCROOT INPUT
# ---------------------------
read -p "Enter Document Root (/var/www/project/public): " DOCROOT

if [ ! -d "$DOCROOT" ]; then
    echo "❌ ERROR: Directory does not exist: $DOCROOT"
    exit 1
fi

CONF_FILE="/etc/apache2/sites-available/${DOMAIN}.conf"

# ---------------------------
# VIRTUAL HOST CREATE
# ---------------------------
echo ""
echo "Creating Apache VirtualHost..."

sudo tee "$CONF_FILE" > /dev/null <<EOF
<VirtualHost *:80>
    ServerName ${DOMAIN}
    ServerAlias www.${DOMAIN}

    DocumentRoot ${DOCROOT}

    <Directory ${DOCROOT}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/${DOMAIN}_error.log
    CustomLog \${APACHE_LOG_DIR}/${DOMAIN}_access.log combined
</VirtualHost>
EOF

# ---------------------------
# APACHE SETUP
# ---------------------------
echo ""
echo "Enabling Apache modules..."

sudo a2enmod rewrite
sudo a2enmod headers

echo ""
echo "Enabling site..."

sudo a2ensite "${DOMAIN}.conf"

echo ""
echo "Checking Apache configuration..."

sudo apache2ctl configtest

echo ""
echo "Reloading Apache..."

sudo systemctl reload apache2

# ---------------------------
# HOSTS FILE OPTION
# ---------------------------
echo ""
read -p "Do you want to add domain to /etc/hosts? (y/n): " ADD_HOSTS

if [[ "$ADD_HOSTS" =~ ^[Yy]$ ]]; then

    HOST_ENTRY="127.0.0.1 $DOMAIN"

    if grep -q "$DOMAIN" /etc/hosts; then
        echo "⚠️ Domain already exists in /etc/hosts"
    else
        echo "$HOST_ENTRY" | sudo tee -a /etc/hosts > /dev/null
        echo "✅ Added to /etc/hosts: $HOST_ENTRY"
    fi

    echo ""
    read -p "Do you want to edit /etc/hosts manually now? (y/n): " EDIT_HOSTS

    if [[ "$EDIT_HOSTS" =~ ^[Yy]$ ]]; then
        sudo nano /etc/hosts
    fi
fi

# ---------------------------
# SSL SETUP
# ---------------------------
echo ""
read -p "Install SSL with Let's Encrypt? (y/n): " SSL

if [[ "$SSL" =~ ^[Yy]$ ]]; then

    echo ""
    echo "Installing Certbot..."

    sudo apt update
    sudo apt install -y certbot python3-certbot-apache

    echo ""
    echo "Generating SSL Certificate..."

    sudo certbot --apache -d "$DOMAIN" -d "www.$DOMAIN"

    echo ""
    echo "Testing Auto Renewal..."

    sudo certbot renew --dry-run

    echo ""
    echo "SSL Installed Successfully"
fi

# ---------------------------
# SUMMARY
# ---------------------------
echo ""
echo "======================================"
echo "Setup Complete"
echo "======================================"
echo "Domain      : $DOMAIN"
echo "DocumentRoot: $DOCROOT"
echo "Config File : $CONF_FILE"
echo ""
echo "Access URL:"
echo "http://$DOMAIN"
echo ""
echo "======================================"

