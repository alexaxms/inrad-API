FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /inrad
COPY requirements.txt /inrad/
RUN pip3 install -r requirements.txt
COPY . /inrad/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000
CMD ["uwsgi", "--http", ":8000", "--ini", "./uwsgi.ini"]