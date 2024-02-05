FROM python:3.9

WORKDIR /fastapi_app

COPY ./requirements.txt /fastapi_app/back/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi_app/back/requirements.txt

COPY . /fastapi_app/back

COPY ./../db /fastapi_app/db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
