import logging
from logging.config import dictConfig
import sys
from typing import Tuple

# Instrumentation
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Trace things
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)

# Metrics things
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    MetricExporter,
    PeriodicExportingMetricReader,
)

# Logging things
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from pythonjsonlogger.json import JsonFormatter

from app.settings import settings


logger = logging.getLogger(__name__)


def get_exporter(
    endpoint: str, console: bool = False
) -> Tuple[SpanExporter, MetricExporter]:
    if console:
        return (ConsoleSpanExporter(), ConsoleMetricExporter())
    return (OTLPSpanExporter(endpoint, True), OTLPMetricExporter(endpoint, True))


def setup_otel_exporter(app_name: str, endpoint: str):
    if settings.running_unittests == 1:
        # If we're running unittests, skip setting up exporter and provider so
        # it's using the default no-op things
        return

    logger.info(
        "Starting opentelemetry exporter %s", endpoint, extra={"endpoint": endpoint}
    )

    # Service name is required for most backends
    resource = Resource.create(attributes={SERVICE_NAME: app_name})
    span_exporter, metric_exporter = get_exporter(endpoint)

    tracerProvider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(span_exporter)
    tracerProvider.add_span_processor(processor)
    trace.set_tracer_provider(tracerProvider)

    reader = PeriodicExportingMetricReader(metric_exporter)
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)


def setup_structured_logging() -> None:
    LoggingInstrumentor().instrument()

    handler = ["console-pretty" if settings.environment == "dev" else "console-mozlog"]

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                    "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(otelTraceID)s %(otelSpanID)s %(otelTraceSampled)s",
                    "rename_fields": {
                        "levelname": "severity",
                        "asctime": "timestamp",
                        "otelTraceID": "logging.googleapis.com/trace",
                        "otelSpanID": "logging.googleapis.com/spanId",
                        "otelTraceSampled": "logging.googleapis.com/trace_sampled",
                    },
                    "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                },
                "text": {
                    "format": "%(message)s",
                },
            },
            "handlers": {
                "console-mozlog": {
                    "level": logging.INFO,
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": sys.stdout,
                },
                "console-pretty": {
                    "level": logging.INFO,
                    "class": "rich.logging.RichHandler",
                    "formatter": "text",
                },
            },
            "loggers": {
                "app": {
                    "handlers": handler,
                    "propagate": True,
                    "level": logging.INFO,
                },
                "uvicorn": {
                    "handlers": handler,
                    "propagate": True,
                    "level": logging.INFO,
                },
                "fastapi": {
                    "handlers": handler,
                    "propagate": True,
                    "level": logging.INFO,
                },
            },
        }
    )


def instrument_app(app):
    FastAPIInstrumentor.instrument_app(app)
