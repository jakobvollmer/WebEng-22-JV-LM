# WebEng-22-JV-LM
  This projekt is written in python using the flask framework.

## Run projekt
### Compose
  Download *https://gitlab.com/biletado/compose* and replace *.env* and *compose.yml* with files of this directory.

### Database preparation
  You have to change key `from` to `From` and `to` to `To`

## Build docker image locally
```powershell
  ./debug.ps1 local
```

## Run docker container local in biletado enviroment
  Start the compose without the reservation backend. Then run following command:
```powershell
  ./debug.ps1 local run
```

## Container enviroment variable
| Key                            | example value                    | default value        | explaination                         |
|--------------------------------|----------------------------------|----------------------|--------------------------------------|
| KEYCLOAK_HOST                  | keycloak                         | localhost            | Keycloak host                        |
| KEYCLOAK_REALM                 | biletado                         |                      | Keycloak realm                       |
| RESERVATION_PORT               | 9000                             | 9000                 | Reservation backend app listen port  |
| JAEGER_TRACECONTEXTHEADERNAME  | uber-trace-id                    | uber-trace-id        | Jaeger header name                   |
| POSTGRES_RESERVATIONS_USER     | admin                            |                      | DB username                          |
| POSTGRES_RESERVATIONS_PASSWORD | secret                           |                      | DB password                          |
| POSTGRES_RESERVATIONS_DBNAME   | reservation                      |                      | DB name                              |
| POSTGRES_RESERVATIONS_HOST     | postgres                         | localhost            | DB host                              |
| POSTGRES_RESERVATIONS_PORT     | 5432                             | 5432                 | DB port                              |
| LOG_LEVEL                      | DEBUG                            | INFO                 | Log level of app                     |
| LOG_TO_CONSOLE                 | True                             | False                | If True app output log to console    |
| BACKEND_ASSETS_HOST            | traefik                          | localhost            | Hostname of the asset backend        |

## Logs
  The backend log files are located in the /log directory on the contianer. In order to be able to access the log files, this directory must be mounted on the host. The environment variable *LOG_FILE_PATH_HOST* specifies the directory for the log files on the host computer.

## CI/CD Pipeline
`biletado-reservations` uses _GitLab CI_ as a continuous integration system. The current pipeline compiles the project and pushes a Docker container to the gitlab-repository. The pipeline also runs system test and fails the build if these do not pass.

The test files are in the test folder of the projekt.
