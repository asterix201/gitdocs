FROM python:3.8-alpine

RUN adduser -D gitdocs

WORKDIR /home/gitdocs

COPY requirements.txt requirements.txt
RUN apk add --no-cache \
        build-base \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip3 install -r requirements.txt && \
    pip3 install gunicorn && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev

COPY app app
COPY gitdocs.py config.py ./

ENV FLASK_APP gitdocs.py

RUN chown -R gitdocs:gitdocs ./
USER gitdocs

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", ":8080", "-w", "4", "gitdocs:app"]
