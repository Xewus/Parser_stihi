FROM python:3.10.8-slim-buster
RUN mkdir /app/
RUN mkdir /app/parser/
COPY requirements.txt scrapy.cfg /app/
RUN pip install -U pip -r app/requirements.txt --no-cache-dir
COPY ./parser /app/parser
WORKDIR /app/
CMD ["uvicorn" , "parser.web:app", "--host", "0.0.0.0", "--port", "8000"]
LABEL "version"="1.0"
LABEL "author"="xewus"