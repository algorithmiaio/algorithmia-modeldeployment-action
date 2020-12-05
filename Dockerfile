FROM cschranz/gpu-jupyter

RUN pip3 install algorithmia&& \
    pip3 install algorithmia-api-client 

# COPY src /usr/algorithmia_ci/src
# COPY entrypoint.sh /usr/algorithmia_ci/entrypoint.sh
# USER root
# RUN chmod +x /usr/algorithmia_ci/entrypoint.sh
# ENTRYPOINT ["/usr/algorithmia_ci/entrypoint.sh"]
COPY src /src
COPY entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]