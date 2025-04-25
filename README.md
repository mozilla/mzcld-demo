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

## Configuration

Environment variables you can set:

<dl>
  <dt>`ENVIRONMENT`</dt>
  <dd>The environment this is running in.</dd>

  <dt>`OTEL_COLLECTOR_ENDPOINT`</dt>
  <dd>Host and port for the OpenTelemetry collector to use.</dd>

  <dt>`RUNNING_UNITTESTS`</dt>
  <dd>
    `1` if running unittests. This causes OpenTelemetry to be
    configured using no-op exporters and providers.
  </dd>
</dl>
