#!/bin/bash

# Create directories
sudo mkdir -p /etc/nginx/ssl/live/numberninjagames.com
sudo mkdir -p /var/www/certbot

# Install certbot
sudo apt-get update
sudo apt-get install -y certbot

# Stop nginx if running
sudo docker-compose -f docker-compose.prod.yml stop nginx

# Get SSL certificate
sudo certbot certonly --standalone \
    -d numberninjagames.com \
    -d www.numberninjagames.com \
    --email admin@numberninjagames.com \
    --agree-tos \
    --no-eff-email \
    --preferred-challenges http

# Copy certificates
sudo cp /etc/letsencrypt/live/numberninjagames.com/* /etc/nginx/ssl/live/numberninjagames.com/

# Set up auto-renewal
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

# Restart nginx
sudo docker-compose -f docker-compose.prod.yml up -d nginx

echo "SSL certificates have been set up for numberninjagames.com"
echo "Auto-renewal has been configured to run daily at 12:00" 