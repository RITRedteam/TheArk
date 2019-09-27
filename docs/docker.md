# Deployment with Docker
Docker makes deployment of the ark very very simple. Below is a well-commented example of a docker-compose file with basic configuration options.

You can deploy this file with the following command:
```bash
docker-compose up -d theark
```

```yml
# docker-compose.yml
version: '3'
services:
    theark:
        build: https://github.com/ritredteam/theark.git
        network_mode: 'host'
        privileged: true
        environment:
            # Specify the HOST if you do _not_ want flask to listen on 0.0.0.0
            #- FLASK_HOST=10.2.3.4
            # Defaults to 80
            #- FLASK_PORT=8080
            - ARK_USERNAME=admin
            - ARK_PASSWORD=changeme
            # If you would like a persistent database, use a volume mapping like below
            - ARK_DATABASE=./db/theark.sqlite
            # Optional: Specify a config file, requires the volume mapping below
            #- ARK_CONFIG=./config.yml
        volumes:
            - ./storage:/opt/theark/db/:rw
            # - ./config.yml:/opt/theark/config.yml:ro
```