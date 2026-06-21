from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation
import random

import os

APP_NAME = os.getenv("APP_NAME", "app-a")

prometheus_reader = PrometheusMetricReader()

metrics.set_meter_provider(
    MeterProvider(
        metric_readers=[prometheus_reader]
    )
)

# a partir de meter criamos as métricas
meter = metrics.get_meter(APP_NAME)

request_counter = meter.create_counter(
    name="app_requests_total",
    description="Número de requisiçõs processadas",
    unit="1",
)

def collect_callback(options: CallbackOptions) -> Iterable[Observation]:
    random_value = random.randint(1, 100)
    yield Observation(value=random_value, attributes={"service": APP_NAME})

meter.create_observable_counter(
    name="app_random_number",
    description="Número aleatório entre 1 e 100",
    callbacks=[collect_callback],
)