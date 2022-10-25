FROM python:3.10.8-slim-buster
RUN mkdir /parser
COPY . /parser
RUN pip install -U pip -r parser/requirements.txt --no-cache-dir
CMD ["uvicorn" , "parser.web:app", "--host", "0.0.0.0", "--port", "8765"]
LABEL "version"="1.0"
LABEL "author"="xewus"