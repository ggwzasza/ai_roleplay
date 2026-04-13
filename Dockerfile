FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

RUN apt-get update -qq && apt-get install -qq -y \
    python3.11 python3-pip python3.11-dev \
    zip unzip openjdk-17-jdk \
    autoconf libtool libffi-dev \
    git curl wget \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython

WORKDIR /app
COPY . .

CMD ["buildozer", "-v", "android", "debug"]
