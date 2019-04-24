FROM python:3.7
MAINTAINER "Amane Suzuki <amane.suzu@gmail.com>"
WORKDIR /tmp
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system
ENTRYPOINT ["python", "main.py"]