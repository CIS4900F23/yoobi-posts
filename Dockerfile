FROM python:3.10.10-slim
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install python-dotenv
EXPOSE 8080
CMD ["./initBackend.sh"]

