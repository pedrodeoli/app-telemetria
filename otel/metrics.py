import psutil
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation
import random
import psutil

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

active_requests_gauge = meter.create_gauge(
    name="app_active_requests",
    description="Número de requisições ativas",
    unit="1",
)

process = psutil.Process()
# Função para obter o uso de memória do processo
def get_memory_usage(options: CallbackOptions) -> Iterable[Observation]:
    mem_usage = process.memory_percent()
    yield Observation(value=mem_usage, attributes={"service": APP_NAME})

memory_gauge = meter.create_observable_gauge(
    name="app_memory_usage",
    description="Uso de memória do processo",
    unit="percent",
    callbacks=[get_memory_usage],
)

# Função para obter o uso de CPU do processo
def get_cpu_usage(options: CallbackOptions) -> Iterable[Observation]:
    cpu_usage = process.cpu_percent(interval=0.1)
    yield Observation(value=cpu_usage, attributes={"service": APP_NAME})

cpu_gauge = meter.create_observable_gauge(
    name="app_cpu_usage",
    description="Uso de CPU do processo",
    unit="percent",
    callbacks=[get_cpu_usage],
)