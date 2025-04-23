# README

MozCloud demo.

## Dev environment

To build containers:

```
make build
or
docker compose build
```

To run webapp in dev mode:
```
make run
or
docker compose up
```

To run webapp in production mode:
```
docker run -d -p 8000:8000 --rm mzcld-demo-web:latest
```

To open up a bash shell inside the web container:
```
docker compose run --rm web shell
```

To run tests:
```
make test
```
