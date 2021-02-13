FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
WORKDIR /code/

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "./entrypoint.sh" ]
