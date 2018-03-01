FROM python:3.6.4-jessie

RUN pip install docker-py \
  feedparser \
  nosexcover \
  prometheus_client \
  pycobertura \
  pylint \
  pyflakes \
  pycodestyle \
  pytest \
  pytest-cov \
  requests \
  setuptools \
  sphinx

RUN wget -qO /usr/local/bin/qcoverage \
  https://github.com/qnib/qcoverage/releases/download/v0.1/qcoverage_v0.1_Linux \
  && chmod +x /usr/local/bin/qcoverage
