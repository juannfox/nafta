FROM python:3.10.4-slim
WORKDIR /usr/src

COPY pyproject.toml ./
COPY requirements.txt ./
RUN pip install --upgrade pip==23.0.1
RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY api ./

EXPOSE 8080/tcp

CMD [ "python", "./main.py" ]