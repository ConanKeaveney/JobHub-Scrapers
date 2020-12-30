FROM python:3.8-slim-buster

WORKDIR /usr/src/app/backend/scrapers

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]
