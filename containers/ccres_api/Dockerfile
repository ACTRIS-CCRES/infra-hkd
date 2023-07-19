FROM python:3.10

RUN apt update
RUN apt install -y graphviz graphviz-dev
RUN pip install pygraphviz

COPY ../ccres_api/requirements/ /requirements/

RUN pip install -r /requirements/local.txt
RUN rm -rf /requirements/