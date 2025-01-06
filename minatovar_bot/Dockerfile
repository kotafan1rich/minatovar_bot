FROM python:3.9

WORKDIR /app

COPY . .

RUN chmod +x /app/docker/bot.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
CMD [ "/app/docker/bot.sh" ]