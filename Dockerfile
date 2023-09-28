FROM python:3.8
ADD ./fastAPI/requirements.txt /requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8088
CMD ["python3", "main.py"]