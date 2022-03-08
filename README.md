# Promotions API

## Project Setup

To clone the project to local, run in terminal:

```shell
$ git clone https://github.com/nyu-devops-sp22/promotions.git
```

To start developing with Visual Studio Code and Docker, navigate to the repo and use ```code``` command

```shell
$ cd promotions
$ code .
```

Then, inside VSCode window, click `Reopen in Container`.

## Running tests

To run the tests, run ```nosetests``` in terminal

```shell
$ nosetests
```

## Running services

To start service, run ```flask run``` in terminal:

```shell
$ flask run
```

You should be able to reach the service at: http://127.0.0.1:8000.

### Promotion routes

Routes | HTTP response | Description
--- | --- | ---
`GET /` | 200 OK | Root URL response
`GET /promotions`  | 200 OK | List all promotions
`GET /promotions/:id` |  200 OK | Get a promotion with specified ID
`POST /promotions` | 201 CREATED | Create a promotion
`DELETE /promotions/:id` | 204 DELETED | Delete a promotion
`PUT  /promotions/:id` | 200 OK | Update a promotion

### Create Promotion

To create a promotion, we use the `POST` HTTP method with the url: `http://localhost:8000/promotions`. The json object that has to be passed in order to create a promotion needs to be of the form: 

```
{
    "name": "10% Sale", 
    "start_date": "01-01-2022 10:10:10",
    "end_date": "04-05-2022 10:10:10",
    "type": "Value",
    "value": 10.0,
    "ongoing": true,
    "product_id": 1
}
```

The HTTP response, in this case would be: 
```
{
    "end_date": "04-05-2022 10:10:10 ",
    "id": 2,
    "name": "10% Sale",
    "ongoing": true,
    "product_id": 1,
    "start_date": "01-01-2022 10:10:10 ",
    "type": "Value",
    "value": 10.0
}
```

### List Promotions

To list all promotions, we use the HTTP method `GET` and the url `http://localhost:8000/promotions`. 

The HTTP response should be similar to the json code below.
```
[
    {
        "end_date": "04-05-2022 10:10:10 ",
        "id": 2,
        "name": "10% Sale",
        "ongoing": true,
        "product_id": 1,
        "start_date": "01-01-2022 10:10:10 ",
        "type": "Value",
        "value": 10.0
    },
    {
        "end_date": "04-05-2022 12:12:01 ",
        "id": 3,
        "name": "20% Sale",
        "ongoing": true,
        "product_id": 3,
        "start_date": "01-01-2022 01:10:10 ",
        "type": "Value",
        "value": 20.0
    }
]
```

### Get Promotion

To get a specific promotion, for example, the promotion with id equal to 2, we can use the `GET` HTTP method with the url `http://localhost:8000/promotions/2`. In this case, the response would be a json object like: 

```
{
    "end_date": "04-05-2022 10:10:10 ",
    "id": 2,
    "name": "10% Sale",
    "ongoing": true,
    "product_id": 1,
    "start_date": "01-01-2022 10:10:10 ",
    "type": "Value",
    "value": 10.0
}

```

### Update promotion

To update a promotion with specified promotion id, we use `PUT` HTTP method with url `http://localhost:8000/promotions/id`. The promotion data is represented as json object in HTTP body like creating promotion. The returned response is a json object which is the updated promotion if the request succeeds.
