# back/Dockerfile
FROM python:3.9

WORKDIR /fastapi_app/back

COPY ./requirements.txt /fastapi_app/back/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi_app/back/requirements.txt

COPY ./app /fastapi_app/back/app

COPY ./db /fastapi_app/back/db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
