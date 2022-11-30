# run in admin powershell befor executing this file: >>Set-ExecutionPolicy RemoteSigned<<
# Running local change following in traefic->backend-reservation
# comment:   - url: http://backend-reservations:9000
# uncomment: - url: http://host.docker.internal:9000

# docker login registry.gitlab.com
# Username + acces token

function info {
    write-host "You need to choose a build tag <local|remote>"
    write-host "-> local: uses tag for local image."
    write-host "-> remote: uses tag for gitlab-docker-registry and pushes docker image on gitlab-docker-registry."
    write-host "-------- optional args --------"
    write-host "<run> as second command. If set a example container starts."

    exit
}

$cmd=$args[0]
$run=$args[1]

if (([string]::IsNullOrEmpty($cmd))) {
    info

} elseif ($cmd -eq "local") {
    $imageTag="webeng-22-jv-lm:latest"

} elseif ($cmd -eq "remote") {
    $imageTag="registry.gitlab.com/jakobvollmer/webeng-22-jv-lm:latest"

} else {
    info
}

docker build . --tag $imageTag

if ($cmd -eq "remote") {
    docker push $imageTag
}

if (-not ([string]::IsNullOrEmpty($run))) {
    if ($run -eq "run") {
        docker run --rm -ti -p 9000:9000 --net=biletado_default -h backend-reservations `
            -e KEYCLOAK_HOST="traefik" `
            -e KEYCLOAK_REALM="biletado" `
            -e JAEGER_TRACECONTEXTHEADERNAME="Uber-Trace-Id" `
            -e POSTGRES_RESERVATIONS_USER="postgres" `
            -e POSTGRES_RESERVATIONS_PASSWORD="postgres" `
            -e POSTGRES_RESERVATIONS_DBNAME="reservations" `
            -e POSTGRES_RESERVATIONS_HOST="postgres" `
            -e POSTGRES_RESERVATIONS_PORT="5432" `
            -e LOG_TO_CONSOLE=True `
            -e LOG_LEVEL="DEBUG" `
            -e RESERVATIONS_APP_PORT=9000 `
            $imageTag
    }
}
