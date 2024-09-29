# jupyterhub_config.py

# Use PAMAuthenticator to allow system users to login
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.Authenticator.allow_all = True

# Allow PAM to handle system users
c.PAMAuthenticator.open_sessions = False
c.PAMAuthenticator.create_system_users = True
c.Authenticator.admin_users = {'iaas', "francois.weber"}

# Set the port for JupyterHub
c.JupyterHub.bind_url = 'http://:8000'
