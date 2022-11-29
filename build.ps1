# run in admin powershell befor executing this file: >>Set-ExecutionPolicy RemoteSigned<<
docker build . --tag registry.gitlab.com/jakobvollmer/webeng-22-jv-lm:latest
docker push registry.gitlab.com/jakobvollmer/webeng-22-jv-lm
docker run --rm -ti -p 9000:9000 --net=biletado_default -h backend-reservations `
    -e KEYCLOAK_HOST="traefik" `
    -e KEYCLOAK_REALM="biletado" `
    -e JAEGER_TRACECONTEXTHEADERNAME="Uber-Trace-Id" `
    -e POSTGRES_RESERVATIONS_USER="postgres" `
    -e POSTGRES_RESERVATIONS_PASSWORD="postgres" `
    -e POSTGRES_RESERVATIONS_DBNAME="reservations" `
    -e POSTGRES_RESERVATIONS_HOST="postgres" `
    -e POSTGRES_RESERVATIONS_PORT="5432" `
    registry.gitlab.com/jakobvollmer/webeng-22-jv-lm:latest

# Running local change following in traefic->backend-reservation
# comment:   - url: http://backend-reservations:9000
# uncomment: - url: http://host.docker.internal:9000

# docker login registry.gitlab.com
# Username + acces token