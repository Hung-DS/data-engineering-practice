from datetime import datetime, timedelta

from datetime import date
import json
import time
import sys
from airflow import DAG
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from airflow.operators.python import PythonOperator
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
def craw_stock_price(**kwargs):
    to_date = kwargs["to_date"]
    from_date = "2000-01-01"

    stock_price_df = pd.DataFrame()
    stock_code = "DIG"
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context

    # url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{}~date:gte:{}~date:lte:{}&size=9990&page=1".format(stock_code, from_date, to_date)
    url = "https://github.com/thangnch/MiAI_Stock_Predict/raw/master/stock_prices.json"
    print(url)

    from urllib.request import Request, urlopen

    req = Request(url, headers={'User-Agent': 'Mozilla / 5.0 (Windows NT 6.1; WOW64; rv: 12.0) Gecko / 20100101 Firefox / 12.0'})
    x = urlopen(req, timeout=10).read()

    req.add_header("Authorization", "Basic %s" % "ABCZYXX")

    json_x = json.loads(x)['data']

    stock_price_df = pd.concat([pd.DataFrame([stock]) for stock in json_x], ignore_index=True)

    stock_price_df.to_csv("/var/tmp/app/data/stock_price.csv", index=None)
    return True


def train_model():
    # Doc du lieu VCB 2009->2018
    dataset_train = pd.read_csv('/var/tmp/app/data/stock_price.csv')
    training_set = dataset_train.iloc[:, 5:6].values

    # Thuc hien scale du lieu gia ve khoang 0,1
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Tao du lieu train, X = 60 time steps, Y =  1 time step
    X_train = []
    y_train = []
    no_of_sample = len(training_set)

    for i in range(60, no_of_sample):
        X_train.append(training_set_scaled[i - 60:i, 0])
        y_train.append(training_set_scaled[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    # Flatten input for Dense network
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1])

    # Xay dung model Dense thay cho LSTM
    regressor = Sequential()
    regressor.add(Dense(units=50, activation='relu', input_shape=(X_train.shape[1],)))
    regressor.add(Dense(units=25, activation='relu'))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')

    regressor.fit(X_train, y_train, epochs=10, batch_size=32)
    regressor.save("/var/tmp/app/data/stockmodel.h5")
    return True


def email():
    import ssl
    import os
    import base64
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
    ssl._create_default_https_context = ssl._create_unverified_context

    # Đường dẫn đến file cần gửi
    out_csv_file_path = '/var/tmp/app/data/stock_price.csv'

    # Tạo đối tượng email
    message = Mail(
        from_email='ainoodle.tech@gmail.com',
        to_emails='nguyenvanhung081005@gmail.com',
        subject='Your file is here!',
        html_content='<img src="https://miai.vn/wp-content/uploads/2022/01/Logo_web.png"> Dear Customer,<br>Welcome to Mi AI. Your file is in attachment.<br>Thank you!'
    )

    # Đọc file CSV và mã hóa nó dưới dạng base64
    with open(out_csv_file_path, 'rb') as f:
        data = f.read()

    encoded_file = base64.b64encode(data).decode()

    # Tạo attachment
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('data.csv'),
        FileType('text/csv'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        # Lấy API key từ biến môi trường
        SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
        if not SENDGRID_API_KEY:
            raise ValueError("SENDGRID_API_KEY environment variable is not set!")

        # Khởi tạo client SendGrid và gửi email
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        # In ra phản hồi từ SendGrid
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print(datetime.now())
        
    except Exception as e:
        # In ra lỗi nếu có
        print(f"Error: {str(e)}")

    return True

dag = DAG(
    'crawl_to_train',
    default_args={
        'email': ['nguyenvanhung081005@gmail.com'],
        'email_on_failure': True,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A ML training pipline DAG',
    schedule_interval=timedelta(days=1),
    start_date= datetime.today() - timedelta(days=1),
    tags=['thangnc'])


crawl_data = PythonOperator(
    task_id='crawl_data',
    python_callable=craw_stock_price,
    op_kwargs={"to_date": "{{ ds }}"},
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

email_operator = PythonOperator(
    task_id='email_operator',
    python_callable=email,
    dag=dag
)

crawl_data >> train_model_task >> email_operator