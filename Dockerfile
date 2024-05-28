FROM --platform=linux/amd64 python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv
RUN apt-get update
RUN apt-get install -y chromium-driver

# Install dependencies
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Run the application:
ADD main.py /main.py
CMD . /opt/venv/bin/activate && exec python /main.py