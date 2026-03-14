FROM python:3.13.5

WORKDIR /app

COPY require.txt .
RUN pip install -r require.txt

COPY . .


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]