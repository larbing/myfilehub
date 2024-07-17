FROM python:3

WORKDIR /home/app

COPY requirements.txt ./

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  pip -U
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 


ENV TZ 'Asia/Shanghai'

COPY . .

ENV UPLOAD_PATH /data
ENV SHARE_HOST http://192.168.200.151:8081
RUN rm robyn.env


CMD [ "python", "./run.py" ]