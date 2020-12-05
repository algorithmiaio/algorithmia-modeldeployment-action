FROM cschranz/gpu-jupyter

RUN pip install algorithmia&& \
    pip install algorithmia-api-client 

COPY src /src
COPY entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]