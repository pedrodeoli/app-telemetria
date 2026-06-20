from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

import os

APP_NAME = os.getenv("APP_NAME", "app-a")

prometheus_reader = PrometheusMetricReader()

metrics.set_meter_provider(
    MeterProvider(
        metric_readers=[prometheus_reader]
    )
)

meter = metrics.get_meter(APP_NAME)