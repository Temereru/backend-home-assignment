from ubuntu:focal

SHELL ["/bin/bash", "-c"]

RUN apt -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt -y update && \
    apt -y install python3.8 && \
    apt -y install python3-pip && \
    apt -y install python3-virtualenv

RUN mkdir /app

# Copy the relevant application files
COPY notraffic /app/notraffic
COPY requirements.txt /app/requirements.txt
COPY manage.py /app/manage.py
COPY db.sqlite3 /app/db.sqlite3

RUN useradd -ms /bin/bash app && \
    chown -R app:app /app

USER app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

# Run the application
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate app
CMD python3 manage.py runserver 0.0.0.0:8000