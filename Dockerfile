FROM busybox AS unpack
WORKDIR /unpack
COPY aiomodeus-main.zip /
RUN unzip /aiomodeus-main.zip

FROM python:3.9

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
 
COPY --from=unpack /unpack/ /backend/
COPY ./ /backend/

RUN pip install -r /backend/aiomodeus-main/requirements.txt
RUN pip install ./aiomodeus-main

CMD ["python", "main.py"]