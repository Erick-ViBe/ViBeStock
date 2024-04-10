# ViBeStock API
Inventory management and expiration dates API

> Python-DjangoRestFramework

## Table of contents
* [Technologies](#technologies)
* [Requirements](#requirements)
* [Setup](#setup)
* [Run Project](#run-project)
* [Run Tests](#run-tests)
* [Documentation](#documentation)
* [Contact](#contact)

<p align='center'>
  <img src="https://d38cf3wt06n6q6.cloudfront.net/tyasuitefront/webgpcs/images/warehouse-management-software.png" width="500" >
</p>

## Technologies
* Python
* Django
* DjangoRestFramework
* Swagger UI
* Postman Documentation

## Requirements to run project
* Docker
* Docker Compose

## Setup
1. Clone and enter the repository:\
`git clone https://github.com/Erick-ViBe/ViBeStock.git`\
`cd ViBeStock`

2. Generates the .env file by copying the template\
`cp .env.template .env`

3. Make sure docker is active:\
`docker info`

## Run Project
* `docker-compose up -d --build`\
* Go to [`http://localhost:8000/docs/`](http://localhost:8000/docs/) to see the Swagger Docs\
* To see the project logs run `docker-compose logs web -f`
### Create Super User
* `docker-compose exec web python manage.py createsuperuser`

## Run Tests
`docker-compose exec web python manage.py test`

## Documentation
Import the `postman_collection.json` file into Postman to view the API documentation and examples.\
Or simply go to the published [documentation](https://documenter.getpostman.com/view/17795524/2sA3BgBawQ)

## Contact
Created by [@ErickViBe](https://erickvibe.xyz/) - feel free to contact me!
