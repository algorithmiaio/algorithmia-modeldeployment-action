FROM nvidia/cuda:10.2-runtime

RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools

RUN pip3 -q install pip --upgrade

RUN pip3 install algorithmia&& \
    pip3 install algorithmia-api-client&& \
    pip3 install jupyter&& \
    pip3 install nbformat&& \
    pip3 install nbconvert[execute]

COPY src /src
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
