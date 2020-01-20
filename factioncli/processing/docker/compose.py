import os
from factioncli.processing.config import get_config


def write_build_compose_file():
    config = get_config()

    docker_compose_file_path = os.path.join(config["FACTION_PATH"], "install/docker-compose.yml")

    docker_compose_file_contents = """
version: "3.4"

x-logging: 
      &default-logging
      driver: journald
      options:
        tag: "faction"

services:
  db:
    image: postgres:latest
    ports:
      - "5432:5432"
    volumes:
      - {0}/data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
    logging: *default-logging
  mq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "8080:15672"
    environment:
      - RABBITMQ_DEFAULT_USER={3}
      - RABBITMQ_DEFAULT_PASS={4}
    logging: *default-logging
  console:
    build: ../source/Console
    ports:
      - "{8}:443"
    depends_on:
      - api
    volumes:
      - {0}/certs:/opt/faction/certs
    logging: *default-logging
  api:
    build: ../source/API
    depends_on:
      - mq
      - db
    ports:
      - "5000:5000"
    volumes:
      - {10}:{10}
    environment:
      - API_UPLOAD_DIR={10}
      - FLASK_SECRET={9}
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
    logging: *default-logging
  core:
    build: ../source/Core
    depends_on:
      - mq
      - db
      - console
    environment:
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
      - SYSTEM_USERNAME={11}
      - SYSTEM_PASSWORD={12}
    logging: *default-logging
  build-dotnet:
    build: ../source/Build-Service-Dotnet
    depends_on:
      - core
      - api
    volumes:
      - {0}:{0}
    environment:
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
    logging: *default-logging
""".format(config["FACTION_PATH"], config["POSTGRES_USERNAME"], config["POSTGRES_PASSWORD"],
           config["RABBIT_USERNAME"], config["RABBIT_PASSWORD"], config["POSTGRES_HOST"],
           config["POSTGRES_DATABASE"], config["RABBIT_HOST"], config["CONSOLE_PORT"],
           config["FLASK_SECRET"], config["API_UPLOAD_DIR"], config["SYSTEM_USERNAME"],
           config["SYSTEM_PASSWORD"])

    with open(docker_compose_file_path, "w+") as compose_file:
        compose_file.write(docker_compose_file_contents)


def write_hub_compose_file(docker_tag):
    config = get_config()

    docker_compose_file_path = os.path.join(config["FACTION_PATH"], "install/docker-compose.yml")

    docker_compose_file_contents = """
version: "3.4"

x-logging: 
      &default-logging
      driver: journald
      options:
        tag: "faction"

services:
  db:
    image: postgres:latest
    ports:
      - "5432:5432"
    volumes:
      - {0}/data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
    logging: *default-logging
  mq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "8080:15672"
    environment:
      - RABBITMQ_DEFAULT_USER={3}
      - RABBITMQ_DEFAULT_PASS={4}
    logging: *default-logging
  console:
    image: faction/console:{13}
    ports:
      - "{8}:443"
    depends_on:
      - api
    volumes:
      - {0}/certs:/opt/faction/certs
    logging: *default-logging
  api:
    image: faction/api:{13}
    depends_on:
      - mq
      - db
    ports:
      - "5000:5000"
    volumes:
      - {10}:{10}
    environment:
      - API_UPLOAD_DIR={10}
      - FLASK_SECRET={9}
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
    logging: *default-logging
  core:
    image: faction/core:{13}
    depends_on:
      - mq
      - db
      - console
    environment:
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
      - SYSTEM_USERNAME={11}
      - SYSTEM_PASSWORD={12}
    logging: *default-logging
  build-dotnet:
    image: faction/build-dotnet:{13}
    depends_on:
      - core
      - api
    volumes:
      - {0}:{0}
    environment:
      - POSTGRES_HOST={5}
      - POSTGRES_DATABASE={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
      - RABBIT_HOST={7}
      - RABBIT_USERNAME={3}
      - RABBIT_PASSWORD={4}
    logging: *default-logging
""".format(config["FACTION_PATH"], config["POSTGRES_USERNAME"], config["POSTGRES_PASSWORD"],
           config["RABBIT_USERNAME"], config["RABBIT_PASSWORD"], config["POSTGRES_HOST"],
           config["POSTGRES_DATABASE"], config["RABBIT_HOST"], config["CONSOLE_PORT"],
           config["FLASK_SECRET"], config["API_UPLOAD_DIR"], config["SYSTEM_USERNAME"],
           config["SYSTEM_PASSWORD"]
           docker_tag)

    with open(docker_compose_file_path, "w+") as compose_file:
        compose_file.write(docker_compose_file_contents)


def write_dev_compose_file():
    config = get_config()

    docker_compose_file_path = os.path.join(config["FACTION_PATH"], "install/docker-compose.yml")

    docker_compose_file_contents = """
version: "3.4"
x-logging: 
      &default-logging
      driver: journald
      options:
        tag: "faction"

services:
  db:
    image: postgres:latest
    ports:
      - "5432:5432"
    volumes:
      - {0}/data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={6}
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
    logging: *default-logging
  mq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "8080:15672"
    environment:
      - RABBITMQ_DEFAULT_USER={3}
      - RABBITMQ_DEFAULT_PASS={4}
    logging: *default-logging
""".format(config["FACTION_PATH"], config["POSTGRES_USERNAME"], config["POSTGRES_PASSWORD"],
           config["RABBIT_USERNAME"], config["RABBIT_PASSWORD"], config["POSTGRES_HOST"],
           config["POSTGRES_DATABASE"])

    with open(docker_compose_file_path, "w+") as compose_file:
        compose_file.write(docker_compose_file_contents)