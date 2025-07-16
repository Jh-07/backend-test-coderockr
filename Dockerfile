FROM  python:3.12

WORKDIR /app
COPY requirements.txt ./
COPY docker_entrypoint.sh ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["sh","./docker_entrypoint.sh"]
EXPOSE 8000
