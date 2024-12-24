FROM quay.io/jupyterhub/jupyterhub:latest

RUN pip install --upgrade pip

RUN pip install jupyter

RUN pip install dockerspawner

# 新增多個使用者並設定密碼
# 使用 echo 將使用者與密碼資訊傳遞給 chpasswd
RUN useradd -m -s /bin/bash --uid 1000 PeiMao && \
    useradd -m -s /bin/bash --uid 1001 ichen && \
    useradd -m -s /bin/bash --uid 1002 norm && \
    echo "PeiMao:pppp" | chpasswd && \
    echo "ichen:iiii" | chpasswd && \
    echo "norm:nnnn" | chpasswd

RUN apt-get update && apt-get install -y bash

# 複製初始化腳本到容器內
COPY init_permissions.sh /usr/local/bin/init_permissions.sh
RUN chmod +x /usr/local/bin/init_permissions.sh

# 設置啟動時執行初始化腳本
CMD ["bash", "-c", "/usr/local/bin/init_permissions.sh && jupyterhub --config /srv/jupyterhub/jupyterhub_config.py"]


