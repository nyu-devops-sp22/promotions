# Promotions API

[![.github/workflows/tdd.yml](https://github.com/nyu-devops-sp22/promotions/actions/workflows/tdd.yml/badge.svg)](https://github.com/nyu-devops-sp22/promotions/actions/workflows/tdd.yml)
[![.github/workflows/bdd.yml](https://github.com/nyu-devops-sp22/promotions/actions/workflows/bdd.yml/badge.svg)](https://github.com/nyu-devops-sp22/promotions/actions/workflows/bdd.yml)
[![codecov](https://codecov.io/gh/nyu-devops-sp22/promotions/branch/main/graph/badge.svg?token=W0OM0C51G3)](https://codecov.io/gh/nyu-devops-sp22/promotions)
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

## Running Tests

To run the tests, run ```nosetests``` in terminal

```shell
$ nosetests
```

## Running Services

To start service, run ```flask run``` in terminal:

```shell
$ flask run
```

You should be able to reach the service at: http://127.0.0.1:8000.

### Promotion Routes

Routes | HTTP response | Description
--- | --- | ---
`GET /` | 200 OK | Root URL response
`GET /promotions`  | 200 OK | List all promotions
`GET /promotions/:id` |  200 OK | Get a promotion with specified ID
`POST /promotions` | 201 CREATED | Create a promotion
`DELETE /promotions/:id` | 204 DELETED | Delete a promotion
`PUT  /promotions/:id` | 200 OK | Update a promotion
`PUT /promotions/:id/invalidate` | 200 OK | Invalidate a promotion

### Create Promotion

To create a promotion, we use the `POST` HTTP method with the url: `http://localhost:8000/promotions`. The JSON object that has to be passed in order to create a promotion needs to be of the form:

```
{
    "name": "10% Sale", 
    "start_date": "01-01-2022 10:10:10",
    "end_date": "04-05-2022 10:10:10",
    "type": "VALUE",
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
    "type": "VALUE",
    "value": 10.0
}
```

The parameters in the JSON object are defined in the table below.

Name | Type | Description
--- | --- | ---
`name` | string | The name of the promotion that we want to create
`start_date`  | string | The start date of the promotion. The format should be: `%m-%d-%Y %H:%M:%S`. The default timezone is in UTC (+0000). You can provide custom timezone info in format `%m-%d-%Y %H:%M:%S %z` (e.g. `01-01-2022 00:00:00 -0400`).
`end_date` | string | The end date of the promotion. The format should be: `%m-%d-%Y %H:%M:%S`. The default timezone is in UTC (+0000). You can provide custom timezone info in format `%m-%d-%Y %H:%M:%S %z` (e.g. `01-01-2022 00:00:00 -0400`).
`type` | enum(`VALUE`, `PERCENTAGE`, `UNKNOWN`) in string | The type of the promotion. If the type is `VALUE`, then the numerical value in the field `value` specifies the value to be deducted. If type is `PERCENTAGE` then the `value` field specifies the percentage that should be deducted from the price.
`value` | number | Numerical value representing the amount that should be deducted from the product in the promotion. The way the value is calculated is dictated by the `type` field.
`ongoing` | boolean | Specifies the status of the promotion. If true, then the promotion is active, else, the promotion is not active.

### List Promotions

To list all promotions, we use the HTTP method `GET` and the url `http://localhost:8000/promotions`.
The HTTP response should be similar to the JSON code below.
```
[
    {
        "end_date": "04-05-2022 10:10:10 ",
        "id": 2,
        "name": "10% Sale",
        "ongoing": true,
        "product_id": 1,
        "start_date": "01-01-2022 10:10:10 ",
        "type": "VALUE",
        "value": 10.0
    },
    {
        "end_date": "04-05-2022 12:12:01 ",
        "id": 3,
        "name": "20% Sale",
        "ongoing": true,
        "product_id": 3,
        "start_date": "01-01-2022 01:10:10 ",
        "type": "VALUE",
        "value": 20.0
    }
]
```

### Get Promotion

To get a specific promotion, for example, the promotion with id equal to 2, we can use the `GET` HTTP method with the url `http://localhost:8000/promotions/2`. In this case, the response would be a JSON object like: 

```
{
    "end_date": "04-05-2022 10:10:10 ",
    "id": 2,
    "name": "10% Sale",
    "ongoing": true,
    "product_id": 1,
    "start_date": "01-01-2022 10:10:10 ",
    "type": "VALUE",
    "value": 10.0
}

```

### Update Promotion

To update a promotion with specified promotion id, we use `PUT` HTTP method with url `http://localhost:8000/promotions/id`. The promotion data is represented as JSON object in HTTP body like creating promotion. The returned response is a JSON object which is the updated promotion if the request succeeds.

### Delete Promotion

To delete a promotion, use the `DELETE` HTTP method with the url `http://localhost:8000/promotions/id`.

### Invalidate Promotion

To invalidate a promotion with specified promotion id, we use `PUT` HTTP method with url `http://localhost:8000/promotions/id/invalidate`. The ongoing property in new promotion will be set to false and the promotion will be no longer active. The new promotion will be returned as JSON object in HTTP body.