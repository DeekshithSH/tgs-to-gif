FROM python:3.9-alpine
MAINTAINER Ed Asriyan <ed-asriyan@protonmail.com>

RUN apk update && \
    apk --no-cache add \
        build-base \
        git \
        gcc \
        g++ \
        cmake \
        libstdc++ \
        python3 \
        py3-pip \
        py-pip && \
        pip install --ignore-installed conan;

RUN git clone https://github.com/Samsung/rlottie.git && (cd rlottie && cmake CMakeLists.txt && make && make install) && rm -fr rlottie

WORKDIR /app
ADD conanfile.txt .
RUN conan install .

ADD CMakeLists.txt .
ADD zstr ./zstr
ADD gif ./gif
ADD main.cpp .

ADD requirements.txt .
ADD TGBot ./TGBot

RUN pip3 install -r requirements.txt

RUN cmake CMakeLists.txt && make && mv bin/tgs_to_gif /usr/bin/tgs_to_gif

CMD python3 -m TGBot
