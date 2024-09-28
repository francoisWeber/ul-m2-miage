# jupyterhub_config.py

c = get_config()

# Use PAMAuthenticator to authenticate system users
from jupyterhub.auth import PAMAuthenticator

c.JupyterHub.authenticator_class = PAMAuthenticator

c.LocalAuthenticator.create_system_users = True

# Set the JupyterHub IP and port
c.JupyterHub.bind_url = "http://:8000"

# Specify the JupyterHub cookie secret file
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"

# Set the database file for JupyterHub
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"

# Configuration for the JupyterHub spawner
c.Spawner.default_url = "/lab"

# Admin users (replace with actual system user names)
c.Authenticator.admin_users = {"admin_user", "francois.weber"} # mdp : azerty

# Allowed users (replace with actual system user names)
c.Authenticator.whitelist = {
    "ADAM.LUCAS",
    "ALIEINIK.OLHA",
    "ARNOUT.FABRICE",
    "BEDIER.DORIANE",
    "CASTRO.MOUCHERON",
    "COLIN.KEVIN",
    "FRASELLE.NADEGE",
    "KUKSA.OLEKSANDRA",
    "LOPES.VAZ.ALEXIS",
    "REITER.ROMAIN",
    "RICHIER.MARCUS",
    "VINOT.MATHIEU",
    "francois.weber"
}
# ADAM LUCAS lucas.adam1@etu.univ-lorraine.fr
# ALIEINIK OLHA olha.alieinik5@etu.univ-lorraine.fr
# ARNOUT FABRICE fabrice.arnout6@etu.univ-lorraine.fr
# BEDIER DORIANE doriane.bedier9@etu.univ-lorraine.fr
# CASTRO MOUCHERON NICOLE nicole.castro-moucheron6@etu.univ-lorraine.fr
# COLIN KEVIN kevin.colin3@etu.univ-lorraine.fr
# FRASELLE NADEGE nadege.fraselle4@etu.univ-lorraine.fr
# KUKSA OLEKSANDRA oleksandra.kuksa5@etu.univ-lorraine.fr
# LOPES VAZ ALEXIS alexis.lopes-vaz6@etu.univ-lorraine.fr
# REITER ROMAIN romain.reiter2@etu.univ-lorraine.fr
# RICHIER MARCUS marcus.richier8@etu.univ-lorraine.fr
# VINOT MATHIEU mathieu.vinot8@etu.univ-lorraine.fr

