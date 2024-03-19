FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
COPY ./src /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

CMD ["python", "main.py"]
