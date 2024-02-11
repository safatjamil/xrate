FROM python:3.10-alpine
WORKDIR /
ARG timezone
RUN apk update && apk upgrade
RUN apk add git 
RUN git clone https://github.com/safatjamil/xrate.git
RUN apk add --no-cache tzdata
ENV TZ=$timezone
WORKDIR /xrate
COPY users.yaml /xrate
RUN apk add --no-cache sqlite
RUN sqlite3 /xrate/flask/sql/xrate.db "create table nulltable(id INTEGER PRIMARY KEY, none TEXT)"
RUN apk add py3-pip
RUN pip install -r requirements.txt
RUN python3 flask/sql/init_db.py 

ENV FLASK_APP=/xrate/flask/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
EXPOSE 5000
CMD ["flask", "run"]
