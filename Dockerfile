FROM python:3.12 

WORKDIR /project 

COPY order_management/ /project/order_management/
COPY requirements.txt /project/requirements.txt
COPY docker-run.sh /project/docker-run.sh

RUN pip install -r requirements.txt 

WORKDIR /project/order_management

RUN chmod +x /project/docker-run.sh

ENTRYPOINT ["/project/docker-run.sh"]