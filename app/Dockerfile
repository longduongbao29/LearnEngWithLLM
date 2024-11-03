# Sử dụng Python base image
FROM python:3.10

# Cài đặt các package cần thiết
RUN apt-get update && apt-get install python3-pip -y

WORKDIR /app

# Sao chép và cài đặt các phụ thuộc
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python","api.py"]



