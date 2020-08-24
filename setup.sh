#!/bin/bash
sudo mkdir -p /var/flaskapp/water
cp -r * /var/flaskapp/water
sudo chown -R www-data:www-data /var/flaskapp/water
sudo cp water.conf /etc/supervisor/conf.d/water.conf
sudo systemctl restart supervisor.service
sudo supervisorctl
sudo cp water.susmarski.com /etc/nginx/sites-enabled/.
sudo adduser www-data gpio
sudo adduser www-data kmem