FROM python:3.10-alpine

WORKDIR /root

COPY . /root/app
RUN pip3 install -r app/requirements.txt

ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["gunicorn", "-w", "4", "app.server:app"]