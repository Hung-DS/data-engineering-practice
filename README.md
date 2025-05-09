1. Kim Đức Trí - 23673721 <br>
2. Nguyễn Văn Hùng - 23668291 <br>
3. Võ Lê Hoàng Minh - 23646891 

----
  # BÁO CÁO KẾT QUẢ LAB8, LAB9

# LAB8 - CASE 1
<p>Kết quả chạy pipeline:</p>

![image](https://github.com/user-attachments/assets/d21d0d33-433a-4c9a-8ecb-166c8663c47b)

> Dữ liệu thu thập từ https://tradingeconomics.com/ được ghi trong file .csv
![image](https://github.com/user-attachments/assets/07086900-b45f-4ddb-bb38-8428d1359b35)


> Sau khi pipeline chạy thành công, log của task visualize_task đã in ra link dashboard:
> - Truy cập tại https://charts.mongodb.com/charts-project-0-octxxbu/public/dashboards/ad6298d8-8fd3-476d-a4c6-c86ee18cc535
---

# LAB8 - CASE 2
<p>Kết quả chạy pipeline:</p>

![Screenshot 2025-05-09 154333](https://github.com/user-attachments/assets/7c9fde2a-aa70-4f04-bff6-7ad76b032d68)

> Thu thập và lưu trữ dữ liệu vào file.csv, chạy thành công các tiến trình

![Screenshot 2025-05-09 154453](https://github.com/user-attachments/assets/dd064ef1-6a20-4c25-82b9-ee6217636dd5)
![Screenshot 2025-05-09 154541](https://github.com/user-attachments/assets/ad98e078-d5d2-4b9e-803c-5f2d1c6fe1c9)



# LAB9
<p>Kết quả chạy pipeline:</p>

![image](https://github.com/user-attachments/assets/24e95350-f4a3-45cc-8467-db25d70f993b)
> Ở lần chạy cuối cùng pipeline đã tự động chạy được từ bài 1 đến bài 7.

**Bài 1:**
![Screenshot 2025-05-08 222639](https://github.com/user-attachments/assets/ef55449c-faae-46ac-8c54-7fbb313a85bf)
> Thu thập được các file dữ liệu từ link trong urls được cho và có https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip bị lỗi nên không thể thu thập dữ liệu từ link này.

**Bài 2:**
![Screenshot 2025-05-08 223412](https://github.com/user-attachments/assets/892f71aa-05a2-4561-bb02-a82ffebb808d)
> Thu thập được dữ liệu từ trang web với các yêu cầu được cho và tìm được `HourlyDryBulbTemperature` với thư viện pandas.

**Bài 3:**
![Screenshot 2025-05-08 223711](https://github.com/user-attachments/assets/4dd976a2-5dd0-4565-a57b-e666b61a0139)
> Truy cập vào trang web và in ra những thông tin của file zip sau khi giải nén.

**Bài 4:** <br>
![image](https://github.com/user-attachments/assets/e8a14b83-fe4b-4196-8f49-df3fc3c32c89)
> Đọc dữ liệu từ các file .json nằm ở các thư mục khác nhau và ghi vào file .csv với các trường dữ liệu từ file .json.

**Bài 5:**
![Screenshot 2025-05-08 230557](https://github.com/user-attachments/assets/9ebdbc94-0dfb-43a3-bd82-249c37ed96ec)
![Screenshot 2025-05-08 231119](https://github.com/user-attachments/assets/12201798-930e-4692-8b58-06d13b402484)
> Dữ liệu được ghi thành công vào các bảng trong Postgres và sử dụng pgAdmin để test truy vấn, kiểm tra dữ liệu được chèn vào có đúng theo các bảng hay không.

**Bài 6:**
![Screenshot 2025-05-09 001609](https://github.com/user-attachments/assets/4c19edb6-26b0-40ab-956a-fc41e96a80d0)
![Screenshot 2025-05-09 001627](https://github.com/user-attachments/assets/611434c3-1235-44b1-9add-a823f9bc43d3)
![Screenshot 2025-05-09 001641](https://github.com/user-attachments/assets/7d19b692-7cad-4dfc-8596-52910873a6bb)
> Giải nén thành công dữ liệu từ file zip, sử dụng pyspark để thực hiện các yêu cầu và lưu mỗi câu trả lời vào file resports.csv

**Bài 7:**
![image](https://github.com/user-attachments/assets/4fd18074-3f80-4ca9-ae42-24bff2e06173)
> Sử dụng pyspark để thực hiện các yêu cầu, hiển thị output của 20 dòng đầu trong file.
