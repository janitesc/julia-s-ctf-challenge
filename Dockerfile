FROM ubuntu:22.04

WORKDIR /challenge
COPY . . 

RUN apt-get update && apt-get install -y python3 gdb binutils tar


RUN chmod +x setup-challenge.py start.sh

ENV FLAG=$FLAG
ARG FLAG
RUN python3 /challenge/setup-challenge.py


# Nothing to actually serve
CMD ["tail", "-f", "/dev/null"]