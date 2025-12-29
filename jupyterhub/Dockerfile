FROM quay.io/jupyterhub/jupyterhub:4.0

# Install system dependencies for user management
RUN apt-get update && apt-get install -y \
    sudo \
    passwd \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages for data engineering
RUN pip install --no-cache-dir \
    jupyterlab==4.0.* \
    notebook==7.0.* \
    pyspark==3.5.* \
    pymysql==1.1.* \
    sqlalchemy==2.0.* \
    redis==5.0.* \
    qdrant-client==1.7.* \
    pyvespa==0.41.* \
    boto3==1.34.* \
    pandas==2.1.* \
    numpy==1.26.* \
    matplotlib==3.8.* \
    seaborn==0.13.* \
    scikit-learn==1.3.* \
    plotly==5.18.* \
    requests==2.31.* \
    ipywidgets==8.1.*

# Install dockerspawner for spawning user notebooks
RUN pip install --no-cache-dir \
    dockerspawner==12.1.* \
    jupyterhub-nativeauthenticator==1.2.*

# Create necessary directories
RUN mkdir -p /srv/jupyterhub/config /home


ARG VERSION=1
RUN echo ${VERSION}

# Copy configuration files
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY create_users.py /srv/jupyterhub/create_users.py
COPY create_linux_users.py /srv/jupyterhub/create_linux_users.py
COPY entrypoint.sh /srv/jupyterhub/entrypoint.sh

# Make scripts executable
RUN chmod +x /srv/jupyterhub/entrypoint.sh /srv/jupyterhub/create_linux_users.py

# Copy users.txt if it exists (optional, can be mounted as volume)
# COPY users.txt /srv/jupyterhub/users.txt

# Set working directory
WORKDIR /srv/jupyterhub

# Expose JupyterHub port
EXPOSE 8000


# Use entrypoint script to create users before starting
# ENTRYPOINT ["/srv/jupyterhub/entrypoint.sh"]

