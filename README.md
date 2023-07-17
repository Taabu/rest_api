Requires docker

Requires a .env in the root folder file with the following content:

```
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
```

run the project with `make run`

run test with `python -m pytest --cov=app`
