FROM python:3.8-slim

MAINTAINER chaos:life0531@foxmail.com

RUN mkdir /root/pic_bot

ADD . /root/pic_bot

WORKDIR /root/pic_bot

COPY sources.list /etc/apt/

RUN apt-get update && apt-get install libgl1-mesa-glx libglib2.0-dev -y --fix-missing

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/

RUN pip3 install cryptg pysocks -i https://pypi.douban.com/simple/

CMD ["python3", "main.py"]
