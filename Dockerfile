FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /inrad
COPY requirements.txt /inrad/
RUN pip3 install -r requirements.txt
COPY . /inrad/
RUN chmod +x /inrad/entrypoint.sh
ENTRYPOINT ["/inrad/entrypoint.sh"]
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]