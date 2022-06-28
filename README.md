# Installations

## Install virtual environment
```
python3 -m venv env
```

## Dev
```
source env/bin/activate
python manage.py runserver
```

## Testing
```
sudo mkdir -p /var/www/filer.vipn.net/static
sudo mkdir -p /var/www/filer.vipn.net/media
sudo chown -R fi:fi /var/www/filer.vipn.net
sudo chmod -R 755 /var/www/filer.vipn.net

sudo cp deployment/uwsgi_params /etc/nginx/uwsgi_params
sudo cp deployment/test/nginx.conf /etc/nginx/sites-available/filer.vipn.net.conf
sudo cp deployment/test/ibenefit_filer.service /etc/systemd/system/ibenefit_filer.service
sudo systemctl enable ibenefit_filer
sudo systemctl start ibenefit_filer
sudo systemctl status ibenefit_filer
```

## Production
```
sudo mkdir -p /var/www/filer.ibenefit.vn/static
sudo mkdir -p /var/www/filer.ibenefit.vn/media
sudo chown -R fi:fi /var/www/filer.ibenefit.vn
sudo chmod -R 755 /var/www/filer.ibenefit.vn

sudo cp deployment/uwsgi_params /etc/nginx/uwsgi_params
sudo cp deployment/test/nginx.conf /etc/nginx/sites-available/filer.ibenefit.vn.conf
sudo cp deployment/prod/ibenefit_filer.service /etc/systemd/system/ibenefit_filer.service
sudo systemctl enable ibenefit_filer
sudo systemctl start ibenefit_filer
sudo systemctl status ibenefit_filer
```

