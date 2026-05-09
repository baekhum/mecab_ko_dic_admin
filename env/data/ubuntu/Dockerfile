FROM ubuntu:24.04

ARG USER_NAME
ARG UID
ARG GID

ENV DEBIAN_FRONTEND=noninteractive

# 1. 필수 빌드 도구 및 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    autotools-dev \
    automake \
    libtool \
    git \
    vim \
    wget \
    curl \
    sudo \
    openjdk-21-jdk \
    ant \
    ivy \
    && rm -rf /var/lib/apt/lists/*

# 2. 사용자 설정
RUN if ! getent group $GID ; then groupadd -g $GID $USER_NAME; else GID="${GID}00"; groupadd -g $GID $USER_NAME; fi && \
    useradd -u $UID -g $GID --create-home --shell /bin/bash $USER_NAME && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER $USER_NAME
WORKDIR /home/$USER_NAME/app

# 컨테이너가 종료되지 않고 대기하도록 설정
CMD ["/bin/bash", "-c", "tail -f /dev/null"]
