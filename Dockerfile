FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt /opt/app/

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . /opt/app/

RUN useradd -ms /bin/bash scraper
RUN chown -R scraper:scraper /opt/app

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean \

USER scraper

CMD ["python3", "-m","src.main"]
