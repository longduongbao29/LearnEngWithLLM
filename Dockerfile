FROM python:3.10


RUN apt-get update && apt-get install python3-pip -y

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860 
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python","app.py"]