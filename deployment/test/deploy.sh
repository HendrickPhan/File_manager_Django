#!/bin/bash

SERVER_SSH="centos@server.example"
SERVER_SSH_KEY="~/.ssh/id_rsa"

DOMAIN="filer.example.com"

# Copy source code to server
read -p "Do you want to copy source code to server? Press y or yes to allow: " yn
if [ "$yn" == "y" ] || [ "$yn" == "Y" ] || [ "$yn" == "yes" ] || [ "$yn" == "YES" ]; then
    tar -pczf $DOMAIN.tar.gz --exclude ".git/" --exclude "deployment/test/*.tar.gz" --exclude "deployment/prod/*.tar.gz" --exclude "env/" ../..
    scp -r -i $SERVER_SSH_KEY $DOMAIN.tar.gz $SERVER_SSH:/tmp
    ssh -t -i $SERVER_SSH_KEY $SERVER_SSH "mkdir -p /home/fi/$DOMAIN && tar -zvxf /tmp/$DOMAIN.tar.gz -C /home/fi/$DOMAIN"
fi

# Install virtual environment
read -p "Do you want to install virtual environment? Press y or yes to allow: " yn
if [ "$yn" == "y" ] || [ "$yn" == "Y" ] || [ "$yn" == "yes" ] || [ "$yn" == "YES" ]; then
    ssh -t -i $SERVER_SSH_KEY $SERVER_SSH "cd /home/fi/$DOMAIN && python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && sudo mkdir -p /var/www/filer.example.com/static && sudo mkdir -p /var/www/filer.example.com/media && sudo chown -R fi:fi /var/www/filer.example.com && sudo chmod -R 755 /var/www/filer.example.com"
fi

# Install nginx virtual hosts
read -p "Do you want to install nginx virtual hosts? Press y or yes to allow: " yn
if [ "$yn" == "y" ] || [ "$yn" == "Y" ] || [ "$yn" == "yes" ] || [ "$yn" == "YES" ]; then
    scp -r -i $SERVER_SSH_KEY uwsgi_params $SERVER_SSH:/tmp
    scp -r -i $SERVER_SSH_KEY nginx.conf $SERVER_SSH:/tmp
    ssh -t -i $SERVER_SSH_KEY $SERVER_SSH "sudo cp /tmp/uwsgi_params /etc/nginx/uwsgi_params && sudo cp /tmp/nginx.conf /etc/nginx/sites-available/$DOMAIN.conf && cd /etc/nginx/sites-enabled && sudo ln -sf ../sites-available/$DOMAIN.conf . && sudo nginx -t && sudo nginx -s reload && sudo rm -rf /tmp/nginx.conf"
fi

# Install ibenefit filer service
read -p "Do you want to install ibenefit filer service? Press y or yes to allow: " yn
if [ "$yn" == "y" ] || [ "$yn" == "Y" ] || [ "$yn" == "yes" ] || [ "$yn" == "YES" ]; then
    scp -r -i $SERVER_SSH_KEY ibenefit_filer.service $SERVER_SSH:/tmp
    ssh -t -i $SERVER_SSH_KEY $SERVER_SSH "sudo cp /tmp/ibenefit_filer.service /etc/systemd/system/ibenefit_filer.service && sudo systemctl enable ibenefit_filer && sudo systemctl start ibenefit_filer && sudo systemctl status ibenefit_filer"
fi

# Migrate database and Static Files
read -p "Do you want to migrate static files? Press y or yes to allow: " yn
if [ "$yn" == "y" ] || [ "$yn" == "Y" ] || [ "$yn" == "yes" ] || [ "$yn" == "YES" ]; then
    ssh -t -i $SERVER_SSH_KEY $SERVER_SSH "cd /home/fi/$DOMAIN && source env/bin/activate && cd /home/fi/$DOMAIN/file_manager_django && python manage.py migrate && python manage.py collectstatic && sudo systemctl restart ibenefit_filer"
fi