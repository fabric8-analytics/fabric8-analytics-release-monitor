FROM registry.centos.org/centos/centos:7
MAINTAINER Tomas Hrcka <thrcka@redhat.com>

ENV LANG=en_US.UTF-8 \
    F8A_WORKER_VERSION=30100bf

RUN useradd coreapi

RUN yum --setopt=tsflags=nodocs install -y epel-release && \
    yum --setopt=tsflags=nodocs install -y gcc python36-pip git wget python36-devel libxml2-devel libxslt-devel python36-pycurl && \
    yum clean all

# Cache dependencies
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip install --upgrade wheel && \
    pip3 install -r /tmp/requirements.txt && \
    pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@${F8A_WORKER_VERSION}

ENV APP_DIR=/release_monitor
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY . .

USER coreapi

CMD ["python3", "run.py"]
