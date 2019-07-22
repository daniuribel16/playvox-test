# Playvox Test
 > This is a simple project made up of 3 independant apps, 2 REST API applications built in python and Flask framework and 1 web application coded with React.js that consumes these microservices. Each of them are isolated in a docker container configured in a docker compose file.

## What do I need to run it?

In order to run the project you will need to install the last stable version of docker and docker compose. use the way you prefer to do it [Docker][Docker Install] and [Docker Compose][Docker Compose Install].

```sh
brew install docker
```

```sh
brew install docker-compose
```

## Requirements

The python requirements are listed on requirements.txt file on the folder root.

## Deploy and Run

After cloning this repository, if you are using linux or have "Make" tool available, you can simple type the following command to start the project:

```sh
make install
```

Otherwise you can build and run docker container typing the following commands on root folder:

```sh
docker-compose -f deployments/docker-compose.yml build
```

```sh
docker-compose -f deployments/docker-compose.yml up -d --force-recreate
```

Then simply visit [localhost:3000][App] to open the web!


[Docker Install]:  https://docs.docker.com/install/
[Docker Compose Install]: https://docs.docker.com/compose/install/
[App]: http://127.0.0.1:3000

