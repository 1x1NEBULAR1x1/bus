FROM python:3.10-alpine

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "proxy.py"]



