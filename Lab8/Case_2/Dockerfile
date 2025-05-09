FROM apache/airflow:2.3.0-python3.8
USER root
# 1. Cài thư viện Python
COPY requirements.txt /tmp/requirements.txt
# 3. Cài thư viện Python cho Airflow
# ✅ Sửa dòng này: cài từ /tmp/requirements.txt
USER airflow
# 2. Cài thư viện Python cho Airflow
RUN pip install --no-cache-dir -r /tmp/requirements.txt
