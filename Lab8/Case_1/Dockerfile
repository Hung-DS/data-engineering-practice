FROM apache/airflow:2.3.0-python3.8

USER root

# 1. Cài thư viện Python
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# 3. Cài thư viện Python cho Airflow
# Sửa dòng này: cài từ /tmp/requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /tmp/requirements.txt

