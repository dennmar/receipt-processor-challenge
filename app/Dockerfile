FROM python:3.10-alpine

WORKDIR /root

COPY . /root/app
RUN pip3 install -r app/requirements.txt

ENV PORT=8000
EXPOSE 8000

# Use one worker to allow for simple in-memory storage of receipts.
ENTRYPOINT ["gunicorn", "-w", "1", "app.server:app"]