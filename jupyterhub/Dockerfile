FROM quay.io/jupyterhub/jupyterhub:4.0

# Install system dependencies including Java for PySpark
RUN apt-get update && apt-get install -y \
    sudo \
    passwd \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Python packages for data engineering
RUN pip install --no-cache-dir \
    jupyterlab==4.0.* \
    notebook==7.0.* \
    pyspark==3.5.3 \
    pymysql==1.1.* \
    sqlalchemy==2.0.* \
    redis==5.0.* \
    qdrant-client==1.7.* \
    pyvespa \
    boto3==1.34.* \
    pandas==2.1.* \
    numpy==1.26.* \
    matplotlib==3.8.* \
    seaborn==0.13.* \
    scikit-learn==1.3.* \
    plotly==5.18.* \
    requests==2.31.* \
    ipywidgets==8.1.* \
    fsspec \
    s3fs \
    loguru

# Create necessary directories
RUN mkdir -p /srv/jupyterhub /home

# Copy configuration files
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY create_linux_users.sh /srv/jupyterhub/create_linux_users.sh
COPY entrypoint.sh /srv/jupyterhub/entrypoint.sh

# Make scripts executable
RUN chmod +x /srv/jupyterhub/entrypoint.sh /srv/jupyterhub/create_linux_users.sh

# Set working directory
WORKDIR /srv/jupyterhub

# Expose JupyterHub port
EXPOSE 8000

# Use entrypoint script to create users before starting
ENTRYPOINT ["/srv/jupyterhub/entrypoint.sh"]
