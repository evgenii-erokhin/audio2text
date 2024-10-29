FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requorements.txt --no-cache-dir
CMD ["python", "main.py"]