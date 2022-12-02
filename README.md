# WebEng-22-JV-LM

## Build docker image

```powershell
    docker build . --tag registry.gitlab.com/jakobvollmer/webeng-22-jv-lm:latest
```

## Run the container outside of compose

```powershell
    docker run --rm -ti -p 9000:9000 --net=biletado_default -h backend-reservations `
        -e KEYCLOAK_HOST="<KEYCLOAK_HOST>" `
        -e KEYCLOAK_REALM="<KEYCLOAK_REALM>" `
        -e JAEGER_TRACECONTEXTHEADERNAME="<JAEGER_TRACECONTEXTHEADERNAME>" `
        -e POSTGRES_RESERVATIONS_USER="<POSTGRES_RESERVATIONS_USER>" `
        -e POSTGRES_RESERVATIONS_PASSWORD="<POSTGRES_RESERVATIONS_PASSWORD>" `
        -e POSTGRES_RESERVATIONS_DBNAME="<POSTGRES_RESERVATIONS_DBNAME>" `
        -e POSTGRES_RESERVATIONS_HOST="<POSTGRES_RESERVATIONS_HOST>" `
        -e POSTGRES_RESERVATIONS_PORT="<POSTGRES_RESERVATIONS_PORT>" `
        registry.gitlab.com/jakobvollmer/webeng-22-jv-lm:latest
```

## Example docker-compose configuration and related .env file

Here is the `docker-compose.yml` file.

```yaml
version: "3"
services:
  backend-reservations:
    image: ${BACKEND_RESERVATIONS_IMAGE_REPOSITORY}:${BACKEND_RESERVATIONS_IMAGE_VERSION}
    depends_on:
      - postgres
    environment:
      KEYCLOAK_HOST: "traefik"
      RESERVATION_PORT: "9000"
      KEYCLOAK_REALM: "biletado"
      BACKEND_ASSETS_HOST: ${BACKEND_ASSETS_HOST}
      JAEGER_TRACECONTEXTHEADERNAME: ${JAEGER_TRACECONTEXTHEADERNAME}
      POSTGRES_RESERVATIONS_USER: ${POSTGRES_RESERVATIONS_USER}
      POSTGRES_RESERVATIONS_PASSWORD: ${POSTGRES_RESERVATIONS_PASSWORD}
      POSTGRES_RESERVATIONS_DBNAME: "reservations"
      POSTGRES_RESERVATIONS_HOST: "postgres"
      POSTGRES_RESERVATIONS_PORT: "5432"
      LOG_LEVEL: "DEBUG"
      LOG_TO_CONSOLE: "True"
      LOG_FILE_PATH_HOST: ${LOG_FILE_PATH_HOST}
    expose:
      - "9000"
    restart: unless-stopped
```

And the `.env` file.
```.env
BACKEND_RESERVATIONS_IMAGE_REPOSITORY=registry.gitlab.com/jakobvollmer/webeng-22-jv-lm
BACKEND_RESERVATIONS_IMAGE_VERSION=latest
KEYCLOAK_HOST="traefik"
KEYCLOAK_REALM="biletado"
JAEGER_TRACECONTEXTHEADERNAME=Uber-Trace-Id
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_RESERVATIONS_DBNAME="reservations"
POSTGRES_RESERVATIONS_HOST=postgre
POSTGRES_RESERVATIONS_PORT=5432
```

## Enviroment Variable

| Key                            | example value                    | default value        | explaination                         |
|--------------------------------|----------------------------------|----------------------|--------------------------------------|
| KEYCLOAK_HOST                  | keycloak                         | localhost            | Keycloak host                        |
| KEYCLOAK_REALM                 | biletado                         |                      | Keycloak realm                       |
| RESERVATIONS_APP_PORT          | 9000                             | 9000                 | Reservation backend app listen port  |
| JAEGER_TRACECONTEXTHEADERNAME  | uber-trace-id                    | uber-trace-id        | Jaeger header name                   |
| POSTGRES_RESERVATIONS_USER     | admin                            |                      | DB username                          |
| POSTGRES_RESERVATIONS_PASSWORD | secret                           |                      | DB password                          |
| POSTGRES_RESERVATIONS_DBNAME   | reservation                      |                      | DB name                              |
| POSTGRES_RESERVATIONS_HOST     | postgres                         | localhost            | DB host                              |
| POSTGRES_RESERVATIONS_PORT     | 5432                             | 5432                 | DB port                              |
| LOG_LEVEL                      | DEBUG                            | INFO                 | Log level of app                     |
| LOG_TO_CONSOLE                 | True                             | False                | If True app output log to console    |

## Install dependencies on windows host

If you want to run the app locally on your pc, you need to install the required libraries. Execute the following command for this:

```powershell
    python3 -m pip install -r .\requirements.txt
```