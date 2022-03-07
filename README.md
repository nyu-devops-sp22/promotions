### Instructions on running tests:

To run the tests, First
```shell
$ git clone https://github.com/nyu-devops-sp22/promotions.git
$ cd promotions
$ code .
```
Then, inside VSCode window, click `Reopen in Container`. Afterward, run the tests
```shell
$ nosetests
```

### Instructions on running services:

To start service, use flask run in terminal:

```shell
$ flask run
```

You should be able to reach the service at: http://127.0.0.1:8000.

#### Promotions
Routes | HTTP response | Description
--- | --- | ---
`GET /` | 200 if succeeds | Root URL response
`GET /promotions`  | 200 if succeeds | List all promotions
`GET /promotions/:id` |  200 if succeeds | Get a promotion with specified ID
`POST /promotions` | 201 if succeeds | Create a promotion
`DELETE /promotions/:id` | 204 if succeeds | Delete a promotion
`PUT  /promotions/:id` | 200 if succeeds; 404 if not exist | Update a promotion
