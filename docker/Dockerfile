FROM ubuntu:22.04

ARG USER_ID
ARG GROUP_ID
ARG KERNEL_VERSION


RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Sao_Paulo" \
    apt-get -y install llvm-12 clang-12 libclang-12-dev clang-format-12 libclang1-12 libclang-12-dev libclang-common-12-dev \
    gcc-9 g++-9 \
    python3 python3-dev python3-pip python3-setuptools python3-ipython python-is-python3 \
    ninja-build \
    wget vim binutils git tar zip unzip git cmake linux-tools-common linux-tools-generic linux-tools-${KERNEL_VERSION} texlive-latex-base sudo net-tools libtinfo5 bc

RUN rm /usr/bin/gcc && rm /usr/bin/g++ \
    && ln -s /usr/bin/gcc-9 /usr/bin/gcc \
    && ln -s /usr/bin/g++-9 /usr/bin/g++ \
    && ln -s /usr/bin/clang-12 /usr/bin/clang \
    && ln -s /usr/bin/opt-12 /usr/bin/opt \
    && ln -s /usr/bin/llvm-link-12 /usr/bin/llvm-link \
    && ln -s /usr/bin/llc-12 /usr/bin/llc 

RUN wget https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz \
    && tar -xvzf eigen-3.3.7.tar.gz \
    && rm eigen-3.3.7.tar.gz \
    && mkdir -p eigen-build && cd eigen-build \
    && cmake ../eigen-3.3.7 && make && make install \
    && rm -rf ../eigen-3.3.7 \
    && cd .. && rm -rf eigen-build

ENV CPATH="${CPATH}:/usr/local/include/eigen3/"

RUN git clone https://github.com/IITH-Compilers/IR2Vec.git \
    && cd IR2Vec \
    && mkdir build && cd build \
    && cmake -DLT_LLVM_INSTALL_DIR=/usr -DEigen3_DIR=/usr/local/include/eigen3 ../src \
    && make \
    && make install

RUN ln -s /IR2Vec/build/bin/ir2vec /usr/bin

RUN git clone https://github.com/tudasc/SimAnMo.git \
    && cd SimAnMo \
    && cmake . \
    && make

RUN pip3 install tensorflow \
    && pip3 install tensorboard \
    && pip3 install protobuf \
    && pip install -U compiler_gym \
    && pip3 install cython

RUN ln -s /usr/bin/clang++-12 /usr/bin/clang++

RUN addgroup --gid $GROUP_ID nonroot \
    && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID nonroot \
    && usermod -aG sudo nonroot \
    && echo "nonroot ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers


