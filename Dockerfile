FROM python:3.11

RUN apt update -y && apt install -y python3 python3-pip && apt clean -y

ENV PIP_MIRROR="-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
ENV GENTRADE_CACHE_DIR=/app/cache/

ADD . /app/GenTradeServer
ADD cache /app/cache/

RUN pip install gentrade==0.0.17

ENV PYTHONPATH=/app/GenTradeServer/src/

VOLUME [ "/app/cache/" ]
WORKDIR /app/GenTradeServer/src/

RUN pip install ${PIP_MIRROR} -r /app/GenTrade/requirements.txt
RUN pip install ${PIP_MIRROR} -r /app/GenTradeServer/requirements.txt


EXPOSE 8000

ENTRYPOINT [ "uvicorn", "gentrade_server.main:app", \
             "--host",  "0.0.0.0", \
             "--port", "8000" ]
