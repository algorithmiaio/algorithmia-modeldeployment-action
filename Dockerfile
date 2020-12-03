from nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y \
    git \
    python3.7 \
    python3-setuptools \
    python3-pip

RUN pip3 install algorithmia&& \
    pip3 install algorithmia-api-client&& \
    pip3 install jupyter&& \
    pip3 install nbformat&& \
    pip3 install nbconvert[execute]

COPY src /src
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
