# front/Dockerfile
FROM python:3.9-slim

WORKDIR /fastapi_app/front

COPY ./requirements.txt /fastapi_app/front/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi_app/front/requirements.txt

COPY . /fastapi_app/front

CMD ["streamlit", "run", "./app.py"]
