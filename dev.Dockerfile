# dev docker environment for turicreate
FROM python:3.7-slim

WORKDIR /app
COPY app/ /app/
COPY notebooks/. /app/notebooks/

COPY dev_requirements.txt ./

RUN pip3 install -r dev_requirements.txt

#jupyter
EXPOSE 8888

CMD ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--allow-root"]