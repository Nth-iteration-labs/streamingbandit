#FROM python:3.5-alpine
FROM python:3.5-jessie
ADD ./ /sb/
WORKDIR /sb/

RUN pip install --upgrade pip

RUN pip install .

WORKDIR /sb/app/

CMD ["python3", "./app.py"]