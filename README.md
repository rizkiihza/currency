# Currency API

this API will help user track currency that they want

## Getting Started

### Prerequisites

things that need to be installed:

    - docker
    - docker-compose

### Installing


Build with docker-compose

```
docker-compose up
```


## Running the tests

### Unit testing

docker-compose up will automatically run unit testing but we can run it again

```
docker-compose exec web python manage.py test
```

### Continuous Integration Test (with circleCI)

This repository has circleCI configuration file. It will run in circleCI
everytime there is a commit to the repo

to view the config file

```
vim .circleci/config.yml
```


## Documentation

API documentation:

Class Diagram documentation: 

