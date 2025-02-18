import os
import pwd
import stat
import sys
import shutil

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']

c.DockerSpawner.extra_host_config = {
    "runtime": "nvidia",
    "device_requests": [
        {"Driver": "nvidia", "Count": -1, "Capabilities": [["gpu"]]}
    ],
    "shm_size": "8gb"
}

#c.DockerSpawner.image = "peimao/env/pytorch-notebook"
c.DockerSpawner.allowed_images = {
    "pytorch-gpu": "peimao/env/pytorch-notebook",
    "tensorflow-cpu": "jupyter/tensorflow-notebook"
}
c.DockerSpawner.remove_containers = True
c.Spawner.default_url = '/lab'



from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]
c.JupyterHub.admin_access = True
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin', 'PeiMao', 'ichen', 'norm', 'Peggy', 'Wendy', 'Henry', 'Wu', 'Lulu'}

c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
c.LocalAuthenticator.create_system_users = False



#shutdown the server after no activity for an hour
c.ServerApp.shutdown_no_activity_timeout = 60 * 60
#shutdown kernels after no activity for 30 minutes
c.MappingKernelManager.cull_idle_timeout = 30 * 60
#check for idle kernels every two minutes
c.MappingKernelManager.cull_interval = 2 * 60


# 設定 Notebook 目錄
#c.DockerSpawner.notebook_dir = '/NFS/{username}'.format(username="{username}")
c.DockerSpawner.notebook_dir = '/NFS'

# 設定 Volume 掛載，確保 {username} 會被正確替換
c.DockerSpawner.volumes = {
    "/NFS": "/NFS"
}
#c.DockerSpawner.volumes = {k.format(username="{username}") : v.format(username="{username}") for k, v in c.DockerSpawner.volumes.items()}



c.JupyterHub.cookie_secret_file = '/persist/jupyterhub_cookie_secret'
c.JupyterHub.db_url = '/persist/jupyterhub.sqlite'