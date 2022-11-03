FROM python:3

LABEL author="Thomas.Miller@fidelissecurity.com"

ENV HALO_API_HOSTNAME='https://api.cloudpassage.com'
ENV HALO_API_PORT='443'
ENV HALO_API_VERSION='v1'
ENV OUTPUT_DIRECTORY='/tmp'
ENV MODULE_NAME='svm'

ARG HALO_API_KEY
ARG HALO_API_KEY_SECRET
ARG OUTPUT_DIRECTORY
ARG HALO_GROUP_ID
ARG MODULE_NAME

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py"]