FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "Home.py","--server.port=8501"]