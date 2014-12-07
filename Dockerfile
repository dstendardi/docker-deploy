FROM google/python-runtime

RUN apt-get install -y openssh-client git \
  && pip install -U pip \
  && pip install --upgrade git+git://github.com/signalfuse/maestro-ng@4c06a8336a8224f3838377bf20eef8f104a64e0c
