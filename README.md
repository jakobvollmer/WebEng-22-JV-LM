# WebEng-22-JV-LM

## Install dependencies on windows host

If you want to run the app locally on your pc, you need to install the required libraries. Execute the following command for this:

```powershell
    python3 -m pip install -r .\requirements.txt
```

## Build 

```powershell
    docker build . --tag webeng-22-jv-lm:latest
```

## Run app outside of compose

```powershell
    docker run --rm -ti -p 9000:9000 --net=biletado_default -h backend-reservations `
        -e KEYCLOAK_HOST="traefik" `
        -e KEYCLOAK_REALM="biletado" `
        -e JAEGER_TRACECONTEXTHEADERNAME="Uber-Trace-Id" `
        -e POSTGRES_RESERVATIONS_USER="postgres" `
        -e POSTGRES_RESERVATIONS_PASSWORD="postgres" `
        -e POSTGRES_RESERVATIONS_DBNAME="reservations" `
        -e POSTGRES_RESERVATIONS_HOST="postgres" `
        -e POSTGRES_RESERVATIONS_PORT="5432" `
        webeng-22-jv-lm:latest
```

## Enviroment Variable

| Key                            | example value                    | default value        | explaination                 |
|--------------------------------|----------------------------------|----------------------|------------------------------|
| KEYCLOAK_HOST                  | keycloak                         | localhost            | Keycloak host                |
| KEYCLOAK_REALM                 | biletado                         | biletado             | Keycloak realm               |
| JAEGER_TRACECONTEXTHEADERNAME  | uber-trace-id                    | uber-trace-id        | Jaeger header name           |
| POSTGRES_RESERVATIONS_USER     | admin                            |                      | DB username                  |
| POSTGRES_RESERVATIONS_PASSWORD | secret                           |                      | DB password                  |
| POSTGRES_RESERVATIONS_DBNAME   | reservation                      |                      | DB name                      |
| POSTGRES_RESERVATIONS_HOST     | postgres                         | localhost            | DB host                      |
| POSTGRES_RESERVATIONS_PORT     | 5432                             | 5432                 | DB port                      |
