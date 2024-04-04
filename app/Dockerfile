FROM python:3.11.7

WORKDIR /usr/src/application

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . ./app

ENV PYTHONPATH=/usr/src/application

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0" , "--port", "8000"]