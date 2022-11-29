# run in admin powershell befor executing this file: >>Set-ExecutionPolicy RemoteSigned<<
docker build . --tag webeng-22-jv-lm:latest
docker run --rm -ti -p 9000:9000 webeng-22-jv-lm:latest

# Install python libs on windows
# python3 -m pip install -r .\requirements.txt

# Running local change following in traefic->backend-reservation
# comment:   - url: http://backend-reservations:9000
# uncomment: - url: http://host.docker.internal:9000