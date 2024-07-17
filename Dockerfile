FROM python:3

WORKDIR /home/app

COPY requirements.txt ./

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  pip -U
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 

ENV TZ 'Asia/Shanghai'

COPY . .

RUN useradd -ms /bin/bash app

USER app

CMD [ "python", "./run.py" ]