import os
import subprocess
from factioncli.processing.config import get_config

def write_compose_file():
    config = get_config()

    docker_compose_file_path = os.path.join(config["FACTION_PATH"], "install/docker-compose.yml")

    docker_compose_file_contents = """
version: "3"
services:
  db:
    build: ./factiondb
    ports:
      - "5432:5432"
    volumes:
      - {0}/data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USERNAME={1}
      - POSTGRES_PASSWORD={2}
  mq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "8080:15672"
    environment:
      - RABBITMQ_DEFAULT_USER={3}
      - RABBITMQ_DEFAULT_PASS={4}
  console:
    build: ../services/console
    ports:
      - "{8}:443"
    depends_on:
      - api
  api:
    build: ../services/api
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
  core:
    build: ../services/core
    depends_on:
      - mq
      - db
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
  dotnet-build:
    build: ../services/dotnet-build
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
""".format(config["FACTION_PATH"], config["POSTGRES_USERNAME"], config["POSTGRES_PASSWORD"],
           config["RABBIT_USERNAME"], config["RABBIT_PASSWORD"], config["POSTGRES_HOST"],
           config["POSTGRES_DATABASE"], config["RABBIT_HOST"], config["CONSOLE_PORT"],
           config["FLASK_SECRET"], config["API_UPLOAD_DIR"], config["SYSTEM_USERNAME"],
           config["SYSTEM_PASSWORD"])

    with open(docker_compose_file_path, "w+") as compose_file:
        compose_file.write(docker_compose_file_contents)

