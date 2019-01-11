FROM python:2

WORKDIR /

COPY *.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./watch_linux.py", "./data", "5000" ]