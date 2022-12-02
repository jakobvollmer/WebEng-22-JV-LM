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

get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
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
        docker run --rm -ti -p $ENV:RESERVATION_PORT:$ENV:RESERVATION_PORT --net=biletado_default -h backend-reservations `
            -e RESERVATIONS_APP_PORT=$ENV:RESERVATION_PORT `
            -e KEYCLOAK_HOST=$Env:KEYCLOAK_HOST `
            -e KEYCLOAK_REALM=$Env:KEYCLOAK_REALM `
            -e BACKEND_ASSETS_HOST=$Env:BACKEND_ASSETS_HOST `
            -e JAEGER_TRACECONTEXTHEADERNAME=$Env:JAEGER_TRACECONTEXTHEADERNAME `
            -e POSTGRES_RESERVATIONS_USER=$Env:POSTGRES_RESERVATIONS_USER `
            -e POSTGRES_RESERVATIONS_PASSWORD=$Env:POSTGRES_RESERVATIONS_PASSWORD `
            -e POSTGRES_RESERVATIONS_DBNAME=$Env:POSTGRES_RESERVATIONS_DBNAME `
            -e POSTGRES_RESERVATIONS_HOST=$Env:POSTGRES_RESERVATIONS_HOST `
            -e POSTGRES_RESERVATIONS_PORT=$Env:POSTGRES_RESERVATIONS_PORT `
            -e LOG_LEVEL=$Env:LOG_LEVEL `
            -e LOG_TO_CONSOLE=$Env:LOG_TO_CONSOLE `
            -v $Env:LOG_FILE_PATH_HOST":/log/" `
            $imageTag
    }
}
