FROM quay.io/jupyterhub/jupyterhub:latest

RUN pip install --upgrade pip

RUN pip install jupyter

# 新增多個使用者並設定密碼
# 使用 echo 將使用者與密碼資訊傳遞給 chpasswd
RUN useradd -m -s /bin/bash --uid 1000 PeiMao && \
    useradd -m -s /bin/bash --uid 1001 ichen && \
    useradd -m -s /bin/bash --uid 1002 norm && \
    echo "PeiMao:pppp" | chpasswd && \
    echo "ichen:iiii" | chpasswd && \
    echo "norm:nnnn" | chpasswd