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
- .env-local:
  - In the "DATABASE_URL" line, replace "your_password" with the same database password as used in docker-compose.yml
  - If the web server should be reachable under a certain URL (e.g. bewertungtool.mydomain.de), add this URL to the "DOMAIN_ALIASES" line

Then start the tool using the following command:
```bash
    docker compose up
```

This will start two Docker containers, one for the database and one for the webserver. The call shown above starts in interactive mode. This is recommended for the first start, so that you can see any error that might occur. For production mode, use
```bash
    docker compose up -d
```

Once the tool is running and no more messages are printed to the console, you need to create a shell for restoring the database. In order to create a shell inside the running virtual machine (docker) run:
```bash
    docker exec -ti bewertungstool-bewertungstool_web-1 bash
```

In order to load the set of questions into the database, you need to run :
```bash
    python manage.py dbrestore
```

This command will populate the following SQL tables:
- Lang/ Aku/ Ambu polls: the questions for each care setting
- Lang/ Aku/ Ambu mouses: the tooltips for each question
- Roles Lang/ Aku/ Ambu: the user roles of each care setting

You will now be able to access the database of your project using the [Django admin interface](http://localhost:8998/admin) and the following data:

- Username: admin
- Password: BeBeRobot$DefaultPassword123

Since we are providing a default password, we strongly recommend changing it, after login one time on the admin site and proving that the mentioned tables were filled. In order to do so, just run (also inside the shell):
```bash
    python manage.py changepassword admin
```

+After this step, you can exit the shell in the Docker container:
+```bash
+    exit
+```

**Note 1:** Restoring the database is only needed the first time that you are setting up the tool. After that, you don't need to use a shell again.
**Note 2:** If you ever modify the "models.py" file you need to restart the docker contained in order to load the modified models:
```bash
    docker restart bewertungstool_web
```

### Deployment

In order to be fully able to run this project, you need to set some variables to your desired values inside `Bewertungstool/.env-local`:

- To deploy this project in testing mode (recommended as a first step), set the variable `DEBUG` to `True`.
- To deploy this project in production mode (`DEBUG` set to false), Django requires you to whitelist the domain. Set the variable `DOMAIN` to the host, i.e. `www.domain.com` or `*.domain.com`. If your page has different domain aliases you can also define them under the variable list `DOMAIN_ALIASES`.
- In order to enable the tool to send e-mails, you need to define your `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` and, if different from 587, also your `EMAIL_PORT`.
- In addition, if you want to allow users to create their own accounts inside the tool you have to set the variable `REGISTRATION_DISABLED` to `False`. Please take into account that in order to fully allow registration all the variables for the email also need to be defined. 
- By default django-admin startproject adds a randomly-generated `SECRET_KEY`  to each new project. But if you want to define your own `SECRET_KEY`. More information about `SECRET_KEY` and its use can be found [here](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key).

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

