FROM python:3.9

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
 
COPY ./ /backend/

CMD ["python", "main.py"]