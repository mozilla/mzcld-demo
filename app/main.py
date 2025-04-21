from fastapi import FastAPI
from dockerflow.fastapi import router as dockerflow_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.observability import setup_otel_exporter, setup_structured_logging
from app.routes import router
from app.settings import Settings

settings = Settings()
setup_structured_logging()
setup_otel_exporter("mzcld-demo", settings.otel_collector_endpoint)

# fast api app setup
app = FastAPI()
app.include_router(dockerflow_router)
app.include_router(router)
FastAPIInstrumentor.instrument_app(app)
