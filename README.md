# Bewertungstool 

## Overview

---

Welcome to the Evaluation tool (Bewertungstool), developed by the R&D project [BeBeRobot](https://www.interaktive-technologien.de/projekte/beberobot).
This tool is designed to help organisations inside of a care environment to evaluate and decide if robotic systems can be a good tool for their application. 
The tool offers a Web interface and is designed to run in a Docker container on a Linux host. We have not tested deployment on Windows, which may or may not work.
The tool is designed to be used as part of an interactive workshop, where the moderator is in charge of controlling the web interface and navigates it.

The tool allows for the creation of different user accounts, and multple workshops for each user. Once the workshop is created, it is possible to select the use case that will be evaluated:
- Elderly care (inpatient) or care for the disabled (special forms of housing)
- Hospital
- Care for the elderly (outpatient) or care for the disabled (outpatient)

For each of these scenarios, we provide a list with all the possible participants and the questions that will make the evaluation possible. 
The questions are sorted in six categories (care, technology & infrastructure, institutional & social embedding, Privacy & Law, ethics and economy). 
Each category has a maximum of 8 questions, but it is possible to extend this list. 
After all the questions are answered, the moderator of the workshop receives a PDF Report with the results of the discussion. 

This app was developed based on Django and the Django CMS packages. 
If you are new to Django, you can get some [information](https://docs.djangoproject.com/en/4.2/) here. 

## Installation

---

***Warning: These instructions are not complete yet. This warning will be removed once the tool can be installed following these instructions.***

You need to have Docker installed on your system to run this project.
- [Install Docker](https://docs.docker.com/engine/install/) here. 
- If you have not used Docker in the past, please read this [introduction on Docker](https://docs.docker.com/get-started/) here.

Once you have Docker installed, you can download the repository and build the Docker image with:
```bash
    git clone https://github.com/BeBeRobot/Bewertungstool.git
    cd Bewertungstool
    docker compose build
```

You should now use a text editor and edit the following two files:
- docker-compose.yml: Set a (random) database password in the "POSTGRES_PASSWORD" line
- .env-local: If the web server should be reachable under a certain URL (e.g. bewertungtool.mydomain.de), add this URL to the "DOMAIN_ALIASES" line

Then start the tool using the following command:
```bash
    docker compose up
```

This will start two Docker containers, one for the database and one for the webserver. The call shown above starts in interactive mode. This is recommended for the first start, so that you can see any error that might occur. For production mode, use
```bash
    docker compose up -d
```

Once the tool is running and no more messages are printed to the console, you need to create a shell for creating a superuser and restoring the database. In order to create a shell inside the running virtual machine (docker) run:
```bash
    docker exec -ti bewertungstool-bewertungstool_web-1 bash
```

Once you are inside of the shell, you need to create a [superuser](https://docs.djangoproject.com/en/4.2/intro/tutorial02/) to be able to access the djanto admin site, where you will be able to access and manage the database:
```bash
    python manage.py createsuperuser
```
You will be asked to enter the desired username and password. 
Once it is created, you will be able to access the database of your project using the [Django admin interface](http://localhost:8998/admin).

In order to load the set of questions into the database, you need to run (also inside the shell):
```bash
    python manage.py dbrestore
```

This command will fill up the following tables:
- Lang/ Aku/ Ambu polls: where the questions for each setting are defined. 
- Lang/ Aku/ Ambu mouses: where the Mouse over text of each question is defined. 
- Roles Lang/ Aku/ Ambu: where the roles of each setting are defined. 

**Note:** Creation of the superuser and restorage of the database is only needed the first time that you are building up the tool. Once they are created, you don't need to use a shell again. 

**Note2:** If you do any modification to the "models.py" file. You would need to restart the docker in order to load them:
`docker restart bewertungstool_web`

### Deployment

Note that in order to fully be able to run this project, you need to set some variables to your desired values. 

#### Env variables
- To deploy this project in testing mode (recommended) set the environment variable `DEBUG` to `True` in your hosting environment.
- For production environment (if `DEBUG` is false) django requires you to whitelist the domain. Set the env var `DOMAIN` to the host, i.e. `www.domain.com` or `*.domain.com`.
- For configurating the sending of Emails you need to define your `EMAIL_HOST`, `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` inside `settings.py`.
- You also need to establish your own path for `DATABASE_URL` and `DBBACKUP_STORAGE_OPTIONS` inside `settings.py`.
- You need to define your own password for `POSTGRES_PASSWORD` inside `docker-compose.yml`. 

### Security considerations

The Bewertungstool deliberately uses unencrypted HTTP and not HTTPS. For production use, we strongly recommend to run the Docker container behind a reverse proxy (e.g. based on Apache or NGINX) and use the reverse proxy to manage HTTPS and to provide certificates (e.g. using Let'sEncrypt).

A sample `docker-compose.yml` script for such a setting is provided below. Note that the `port:` setting in the `bewertungstool_web` section has been removed since the HTTP port is not exposed directly anymore, but routed through the reverse proxy, which uses the standard HTTPS port.

```yaml
version: '3.5'

services:

  reverse_proxy:
    image: nginx:1.19
    container_name: reverse
    hostname: reverse
    ports:
      - 80:80
      - 443:443
    networks:
      - internal
    volumes:
      - /export/nginx/config:/etc/nginx
      - /export/nginx/log:/var/log/nginx
      - /export/certbot/conf:/etc/letsencrypt
      - /export/certbot/www:/var/www/certbot
    command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"

  bewertungstool_web:
    image: bewertungstool_web
    hostname: bewertungstool_web
    build: .
    depends_on:
      database_default:
        condition: service_started
    volumes:
      - "./data:/data:rw"
    command:
      - /bin/sh
      - -c
      - |
        cd /app
        sleep 15
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver 0.0.0.0:80
    networks:
      - internal
    env_file: ./.env-local

  database_default:
    image: postgres:9.6-alpine
    environment:
      POSTGRES_DB: "db"
      POSTGRES_PASSWORD: "your_password"
      POSTGRES_HOST_AUTH_METHOD: "trust"
      SERVICE_MANAGER: "fsm-postgres"
    networks:
      - internal
    volumes:
      - "./postgres-data:/var/lib/postgresql/data:rw"

networks:
  internal:
```

This is a sample configuration file for NGINX as a reverse proxy.

```nginx
upstream bewertungstool {
  server        bewertungstool_web:80;
}

server {
  listen        443 ssl;
  server_name   bewertungtool.mydomain.de;
  include       /etc/nginx/common.conf;
  include       /etc/nginx/ssl.conf;
  location / {
    proxy_pass  http://bewertungstool_web;
    include     /etc/nginx/common_location.conf;
  }
}
```

## Acknowledgements

---

This work was funded by the German Federal Ministry of Education and Research as part of the BeBeRobot project (grant no. 16SV8342)
[OFFIS - Institute for Information Technology](https://www.offis.de/) was in charge of developing and reviewing the source code. 
[University of Osnabrück](https://www.igb.uni-osnabrueck.de/abteilungen/pflegewissenschaft.html), [SIBIS Institute for Social and Technical Research GmbH](http://www.sibis-institut.de/), [University of Siegen](https://forschung.uni-siegen.de/) and [German Caritas Association e.V., Freiburg](https://www.caritas.de/diecaritas/deutschercaritasverband/verbandszentrale/standorte/dcv-zentrale-freiburg) developed the content of the tool (e.g. questions and help text). 

