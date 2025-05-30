# TinyLink
TinyLink is a simple URL shortener service using Django and Django Rest Framework.
It allows generating short (tiny) links to manage long URLs efficiently
(in development)


## Technologies used

- Python 3.9.21

- Django 4.2.20

- MySQL

# Installation & Setup Guide
## Prerequisites
- github
- docker
```
    sudo dnf check-update
    sudo dnf config-manager -y --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf install -y docker-ce docker-ce-cli containerd.io git openssh
    sudo service sshd restart
    sudo systemctl start docker
    sudo systemctl status docker
    sudo systemctl enable docker
```
## Clone
```
git clone --branch develop https://github.com/dfigat/TinyLink.git
cd TinyLink
```
## Generate Certificates
```
sudo bash ~/env/issue-certificate.sh -d yourdomain.com -o ${PWD}/certs
```

## Create Enviormental Variables
- guide to creating those is also in env.example
- .env should be in docker directory inside TinyLink directory
### Template for your .env file
```
NGINX_CONFIG_PATH=path to frontend.conf file (absolute)
WWW_HOME="../frontend"
CERT_DIR="certs"
RESTART_POLICY="unless-stopped"

DATABASE_NAME=""
DATABASE_USER=""
DATABASE_PASSWORD=""
DATABASE_ROOT_PASSWORD=""
DATABASE_HOST="mariadb"
DATABASE_PORT="3306"

TEST_DATABASE_NAME=""
TEST_DATABASE_USER=""
TEST_DATABASE_PASSWORD=""
TEST_DATABASE_HOST="mariadb"
TEST_DATABASE_PORT="3306"

SECRET_KEY=""

ALLOWED_HOST="https://yourdomain.com"
ALLOWED_DOMAIN="yourdomain.com"

CERT_PATH="(absolute path to certificate's fullchain.pem)"
KEY_PATH="(absloute path to certificate's privkey.pem)"

API_URL="https://yourdomain.com:PORT/api/"
API_URL_SHORTENED="https://yourdomain.com:PORT/"

WEB_KEY=""
```


## Build docker
```
sudo docker compose -f docker/docker-compose-frontend.yml -f docker/docker-compose-server.yml up -d --build
```

## Done!


## Features

- Generate short (tiny) URLs from long ones

- Redirect to the original URL using the short code

- View all stored links, including date of last usage

- Delete old links based on a time threshold

- Show the configuration of the shortening service
## API Reference

#### Create new short code

```http
  POST /api/v2.0/short/
```

| Argument | Type     
| :-------- | :------- 
| `long_link` | `URL`

#### Get link by code

```http
  GET /api/v2.0/short/${code}/
```

#### Get code by link

```http
  GET /api/v2.0/code/${long_link}/
```

#### Get all links

```http
  GET /api/v2.0/all/
```

#### Get count of stored links

```http
  GET /api/v2.0/get_count_all
```

#### Get server configuration

```http
  GET /api/v2.0/config/
```
#### Delete records by threshold
```http
  DELETE /api/v2.0/delete/{days}
```

## Client
- There is also a script tiny.py you can use to access the api
```
cd scripts
./tiny.py help
```

(for now days are fixed at 30 and providing argument won't affect it)
## A quick demo
![DEMO](.assets/demo.gif)

## Testing
- to run tests use
```
python manage.py test
```
- to run with code coverage use
```
coverage run --source='.' manage.py test
```
#### To see the results of code coverage use any of the following
- to see results in terminal
```
coverage report
```
- to see results in html
```
coverage html
```


