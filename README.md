# Promotions API

### Running tests:

To run the tests, use `nosetests`

```shell
$ nosetests
```

### Running services:

To start service, use flask run in terminal:

```shell
$ flask run
```

You should be able to reach the service at: http://127.0.0.1:8000.

#### Promotions

Routes | HTTP response | Description
--- | --- | ---
`GET /promotions`  | 200 if succeeds | List all promotions
`GET /promotions/:id` |  200 if succeeds | Get a promotion with specified ID
`POST /promotions` | 201 if succeeds | Create a promotion
`DELETE /promotions/:id` | 204 if succeeds | Delete a promotion
`PUT  /promotions/:id` | 200 if succeeds; 404 if not exist | Update a promotion

### Create Promotion

To create a promotion, we use the `POST` HTTP method with the url: `http://localhost:5000/promotions`. The json object that has to be passed in order to create a promotion needs to be of the form: 

```
{
    "name": "10% Sale",
    "code": "sale10",
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

To list all promotions, we use the HTTP method `GET` and the url `http://localhost:5000/promotions`. 

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

To get a specific promotion, for example, the promotion with id equal to 2, we can use the `GET` HTTP method with the url `http://localhost:5000/promotions/2`. In this case, the response would be a json object like: 

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