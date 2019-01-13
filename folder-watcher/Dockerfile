FROM python:2

ENV FOLDER=./data
ENV TIMEOUT=5000

WORKDIR /

COPY *.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

CMD [ "python", "./watch_linux.py", "${FOLDER}", "${TIMEOUT}" ]