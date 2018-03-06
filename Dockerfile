FROM python:2.7-alpine

RUN pip install datadog

ADD log_stats.py log_stats.py
ADD orbi orbi

ENTRYPOINT ["python", "log_stats.py"]