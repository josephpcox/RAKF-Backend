  
FROM python:3.8
MAINTAINER RAKF
WORKDIR .
COPY . .
RUN pip install pipenv
RUN pipenv install 
RUN pipenv shell

CMD ["wsgi.py dev"]