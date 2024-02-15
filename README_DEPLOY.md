##Update Server and Install python and GIT
Update your local package index and then install the packages by typing

```bazaar
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx supervisor
sudo apt-get install git
```

## Clone SALT API

Cloning the saltapi repository using git home directory for user and cd to it.
```bazaar
cd ~
git clone https://github.com/saltastro/saltapi.git
cd saltapi/
```
## Create a Python Virtual Environment 
Start by installing the virtualenv package using pip
```bazaar
sudo pip3 install virtualenv
```
We can create a virtual environment to store our Flask project's Python requirements by typing:
```bazaar
virtualenv tacvenv
```
This will install a local copy of Python and pip into a directory called tacvenv within your project directory.
##Installing requirements
Before installing applications within the virtual environment, it need to activated by. 
```bazaar
source tacvenv/bin/activate

```
and install requirements
```bazaar
pip3 install -r requirements.txt 
```
deactivate after installing by running.
```bazaar
deactivate
```
##Setup Nginx
create a Nginx config file by make sure user has sudo permissions:
```bazaar
sudo nano /etc/nginx/sites-available/tacapi
```
A file will open and add the following.

```
 server {
    listen 80;
    server_name hostname;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8080;
    }
}

```
please note hostname need to be replaced by real hostname
save and close file
```bazaar
Ctrl + o
Enter
Ctrl + x
```
To enable the Nginx server block configuration just created, link the file to the sites-enabled directory:
```bazaar
sudo ln -s /etc/nginx/sites-available/tacapi /etc/nginx/sites-enabled/tacapi
```
(please note site-enables is a directory not a file)

## Setup supervisor

create a supervisor config file by make sure user has sudo permissions:
```bazaar
sudo nano /etc/supervisor/conf.d/tacapi.cape.saao.ac.za.conf
```
A file will open and add the following.
```bazaar
[program:website]
command=/home/tacapi/saltapi/tacvenv/bin/uwsgi uwsgi.ini
directory=/home/tacapi/saltapi
user=www-data
environment=ENVIRONMENT_VARIABLE_1="value",ENVIRONMENT_VARIABLE_2="value",...
```
save and close file
```bazaar
Ctrl + o
Enter
Ctrl + x
```

## Reboot server
```bazaar
sudo reboot
```


