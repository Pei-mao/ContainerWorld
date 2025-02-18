FROM jupyterhub/jupyterhub
 
#Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py .

#Install dependencies (for advanced authentication and spawning)
RUN pip install dockerspawner
RUN pip install jupyter-client
RUN pip install jupyterhub-firstuseauthenticator