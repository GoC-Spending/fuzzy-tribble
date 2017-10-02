FROM ubuntu:16.04
ENV MYSQLXPB_PROTOBUF_INCLUDE_DIR=/usr/include/google/protobuf \
  MYSQLXPB_PROTOBUF_LIB_DIR=/usr/lib/x86_64-linux-gnu \
  MYSQLXPB_PROTOC=/usr/bin/protoc \
  LC_ALL=C.UTF-8 LANG=C.UTF-8

COPY script/build_container.sh /script/build_container.sh
RUN /script/build_container.sh

COPY script /script
COPY requirements.txt /app/requirements.txt
RUN pip install setuptools==36.5.0
RUN pip install -r /app/requirements.txt

COPY . /app
RUN pip install -e /app/.

WORKDIR /app
