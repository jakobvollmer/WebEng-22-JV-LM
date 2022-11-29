# run in admin powershell befor executing this file: >>Set-ExecutionPolicy RemoteSigned<<
docker build . --tag webeng-22-jv-lm:latest
docker run --rm -ti -p 9000:9000 --net=biletado_default `
    -e KEYCLOAK_HOST="traefik" `
    -e KEYCLOAK_REALM="biletado" `
    -e JAEGER_TRACECONTEXTHEADERNAME="Uber-Trace-Id" `
    -e POSTGRES_RESERVATIONS_USER="postgres" `
    -e POSTGRES_RESERVATIONS_PASSWORD="postgres" `
    -e POSTGRES_RESERVATIONS_DBNAME="reservations" `
    -e POSTGRES_RESERVATIONS_HOST="postgres" `
    -e POSTGRES_RESERVATIONS_PORT="5432" `
    webeng-22-jv-lm:latest

# Install python libs on windows
# python3 -m pip install -r .\requirements.txt

# Running local change following in traefic->backend-reservation
# comment:   - url: http://backend-reservations:9000
# uncomment: - url: http://host.docker.internal:9000