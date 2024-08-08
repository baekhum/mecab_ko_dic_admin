FROM ubuntu:latest
ARG USER_NAME
ARG UID
ARG GID

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
RUN apt clean && \
    apt update && \
    apt install -y sudo vim git

RUN echo "UID: $UID"
RUN echo "GID: $GID"
# RUN /bin/bash -c 'if ! getent group $(id -g) ; then groupadd -g $(id -g) mecab_ko_dic_admin; else GID="$(id -g)00"; groupadd -g $GID mecab_ko_dic_admin; fi' && \
RUN if ! getent group $GID ; then groupadd -g $GID $USER_NAME; else GID="${GID}00"; groupadd -g $GID $USER_NAME; fi && \     
    useradd -u $UID -g $GID --create-home --shell /bin/bash $USER_NAME && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt clean && \
    apt install build-essential autogen -y

RUN apt clean && \
    apt install -y wget apt-transport-https gnupg && \
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt update && \
    apt install -y temurin-8-jdk && \
    apt install -y ant ivy && \
    apt install -y gradle

# Set the non-root user as the default user
USER $USER_NAME

# Set the working directory
WORKDIR /home/$USER_NAME/app

# Copy files into the container and set the appropriate permissions
COPY --chown=$USER_NAME:$USER_NAME . /home/$USER_NAME/app
RUN chmod -R 755 /home/$USER_NAME/app 
ENTRYPOINT ["/bin/bash", "-c", "echo Hello, World!; tail -f /dev/null"]