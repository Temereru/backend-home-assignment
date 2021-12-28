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

RUN useradd -ms /bin/bash app && \
    chown -R app:app /app

USER app
WORKDIR /app

# Install the python requirements

# Run the application