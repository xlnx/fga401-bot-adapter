FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN \
  pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
  poetry config virtualenvs.in-project true

# cv2
RUN \
  sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
  apt-get update && \
  apt-get install ffmpeg libsm6 libxext6 -y

ADD . /app
WORKDIR /app

RUN \
  poetry install -vvv
