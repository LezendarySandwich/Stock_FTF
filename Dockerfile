FROM python:3.7

# During Development
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
RUN rm  /tmp/requirements.txt
WORKDIR /app

CMD ["python3", "stox_ftf"]