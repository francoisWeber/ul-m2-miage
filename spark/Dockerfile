# Multi-stage build: Start with Python 3.10 base and install Spark
FROM python:3.10-slim-bookworm

USER root

# Install Java and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    wget \
    procps \
    tini \
    libc6 \
    libpam-modules \
    krb5-user \
    libnss3 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Spark
ENV SPARK_VERSION=3.5.3
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"
ENV PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip:${PYTHONPATH}"

RUN wget -q "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar xzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mv "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" "${SPARK_HOME}" && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

# Install Python packages
RUN pip install --no-cache-dir \
    pyspark==3.5.3 \
    numpy \
    pandas

# Create spark user
RUN groupadd -r spark --gid=185 && \
    useradd -r -g spark --uid=185 spark && \
    mkdir -p /opt/spark/work && \
    chown -R spark:spark /opt/spark

# Set Python environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

WORKDIR /opt/spark/work

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

USER spark

