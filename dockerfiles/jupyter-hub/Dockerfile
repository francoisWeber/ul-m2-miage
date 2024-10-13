FROM jupyterhub/jupyterhub:main

# USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk python3.11 python3.11-venv python3.11-dev

# Create a symlink to ensure 'python3' points to 'python3.11'
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.11 /usr/bin/python

RUN pip install pyspark==3.5.1 hdfs jupyter jupyter_core pyarrow requests numpy
# Prepare Jupyterhub stuff
RUN pip install jupyterhub 
# Prepare other deps for the workshop
RUN pip install pandas requests elasticsearch mysql-connector-python pyvespa matplotlib

## ## ## System users ## ## ##
WORKDIR /init_users
COPY users.txt . 
COPY user_init.sh .
RUN chmod +x user_init.sh
RUN . /init_users/user_init.sh

## ## ## JUPYTERHUB CONFIGURATION ## ## ##
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
CMD ["jupyterhub", "--config", "/srv/jupyterhub/jupyterhub_config.py"]