#!/bin/bash

# Must run as root sudo ./change_php_version.sh
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo). Example sudo ./change_php_version.sh"
  exit 1
fi

echo -e "\033[1;32mCurrent PHP Version:"
php -v | head -n 1

echo ""
read -p "Do you want to change the PHP version? (y/n): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    read -p "Enter new PHP version (example: 8.2, 7.4): " new_version
    current_version=$(php -r "echo PHP_MAJOR_VERSION.'.'.PHP_MINOR_VERSION;")
    a2dismod php$current_version
    systemctl restart apache2
    a2enmod php$new_version
    update-alternatives --set php /usr/bin/php$new_version
    update-alternatives --set phar /usr/bin/phar$new_version
    update-alternatives --set phar.phar /usr/bin/phar.phar$new_version
    systemctl restart apache2
    echo -e "\033[1;32mUpdated PHP Version:"
    php -v | head -n 1
else
    echo -e "\033[1;32mExit without changes."
    exit 0
fi