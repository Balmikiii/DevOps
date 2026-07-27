#!/bin/bash

set -e

# Input
read -rp "MySQL Database Name: " DB_NAME
read -rp "MySQL Username: " DB_USER
read -rp "MySQL Password: " DB_PASS
read -rp "APP URL: " APP_URL

# Basic validation
if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASS" || -z "$APP_URL" ]]; then
  echo "❌ Error: DB name, user, password or app URL cannot be empty"
  exit 1
fi

echo ""
echo "Installing Composer Dependencies..."

composer install --no-dev --optimize-autoloader

composer dump-autoload

echo ""
echo "Configuring .env..."

if [ ! -f .env ]; then
    cp .env.example .env
fi

sed -i "s|^DB_DATABASE=.*|DB_DATABASE=${DB_NAME}|g" .env
sed -i "s|^DB_USERNAME=.*|DB_USERNAME=${DB_USER}|g" .env
sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=${DB_PASS}|g" .env
sed -i "s|^APP_URL=.*|APP_URL=${APP_URL}|g" .env

echo ""
echo "Generating Application Key..."

php artisan key:generate --force

echo ""
echo "Running Migrations..."

php artisan migrate --force

echo ""
echo "Creating Storage Link..."

php artisan storage:link || true

echo ""
echo "Setting Permissions..."

sudo chown -R www-data:www-data .

sudo chmod -R 777 storage
sudo chmod -R 777 bootstrap/cache

echo ""
echo "Optimizing Laravel..."

php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear

php artisan config:cache
php artisan route:cache
php artisan view:cache

echo ""
echo "================================="
echo "Deployment Completed Successfully"
echo "Project Path: $(pwd)"
echo "================================="