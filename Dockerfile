FROM python:3.12.6

# Install system dependencies
RUN apt-get update && \
    apt-get install -y locales libbz2-dev libffi-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /community_guard

WORKDIR /community_guard

COPY . /community_guard/

RUN locale-gen pt_BR pt_BR.UTF-8

RUN export LC_ALL=pt_BR.UTF-8

RUN pip install -r requirements.txt
