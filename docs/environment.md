# Ark Environment Variables

The Ark is customizable with severall different environment variables. These are easily set with [docker-compose](./docker.md)

## Variables

- `ARK_DATABASE` _Default: files/theark.sqlite_ - The location of the Ark DB
- `ARK_CONFIG` _Default: config.yml_ - The location of the Ark configuration file
- `ARK_USERNAME` _Default: admin_ - The username for the ark
- `ARK_PASSWORD` _Default: changeme_ - The password for the ark
- `ARK_COOKIE` _Default: super-secret_ - The api cookie value for the ark

- `FLASK_HOST` _Default: 0.0.0.0_ - The interface for Flask to bind to
- `FLASK_PORT` _Default: 80_ - The port for Flask to bind to
- `FLASK_DEBUG` _Default: false_ - Whether or not Flask should be in debug mode