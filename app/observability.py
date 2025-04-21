import logging
from logging.config import dictConfig
import sys
from typing import Tuple
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    MetricExporter,
    PeriodicExportingMetricReader,
)


from opentelemetry.instrumentation.logging import LoggingInstrumentor
from pythonjsonlogger.json import JsonFormatter

logger = logging.getLogger(__name__)


def get_exporter(
    endpoint: str, console: bool = False
) -> Tuple[SpanExporter, MetricExporter]:
    if console:
        return (ConsoleSpanExporter(), ConsoleMetricExporter())
    return (OTLPSpanExporter(endpoint, True), OTLPMetricExporter(endpoint, True))


def setup_otel_exporter(app_name: str, endpoint: str = "localhost:4317"):
    logger.info("Starting opentelemetry exporter", extra={"endpoint": endpoint})
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

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                    "format": "%(asctime)s %(levelname)s %(message)s %(otelTraceID)s %(otelSpanID)s %(otelTraceSampled)s",
                    "rename_fields": {
                        "levelname": "severity",
                        "asctime": "timestamp",
                        "otelTraceID": "logging.googleapis.com/trace",
                        "otelSpanID": "logging.googleapis.com/spanId",
                        "otelTraceSampled": "logging.googleapis.com/trace_sampled",
                    },
                    "datefmt": " %Y-%m-%dT%H:%M:%SZ",
                }
            },
            "handlers": {
                "console-mozlog": {
                    "level": logging.INFO,
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": sys.stdout,
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["console-mozlog"],
                    "propagate": True,
                    "level": logging.INFO,
                }
            },
        }
    )
