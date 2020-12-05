#from ubuntu:20.04
FROM cschranz/gpu-jupyter

# RUN apt-get update && apt-get install -y \
#     git \
#     python3 \
#     python3-setuptools \
#     python3-pip

# RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
# RUN apt-get install unzip
# RUN apt-get -y install python3
# RUN apt-get -y install python3-pip

RUN pip3 install algorithmia&& \
    pip3 install algorithmia-api-client&& \
    # pip3 install jupyter&& \
    pip3 install nbformat&& \
    pip3 install nbconvert[execute]

COPY src /src
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
#RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]
