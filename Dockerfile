FROM python:3.8

# ADD main.py .
WORKDIR /app

RUN pip install flask 

COPY . /app

CMD ["python", "./pyFiles/app.py"]

