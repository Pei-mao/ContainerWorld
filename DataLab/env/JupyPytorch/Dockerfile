# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/scipy-notebook
FROM $BASE_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Taipei

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install PyTorch with pip (https://pytorch.org/get-started/locally/)
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --extra-index-url=https://pypi.nvidia.com --index-url 'https://download.pytorch.org/whl/cu124' \
    'torch' \
    'torchaudio' \
    'torchvision' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# 安裝其他 Python 套件
RUN pip install \
    pydicom==3.0.1 \
    monai==1.4.0 \
    torchio==0.20.1 \
    albumentations==1.4.17 \
    jupyterlab==4.2.5 \
    numpy==1.26.4 \
    scipy==1.14.1 \
    matplotlib==3.7.5 \
    opencv-python-headless==4.10.0.84 \
    nibabel==5.2.1 \
    nilearn==0.10.4 \
    dipy==1.9.0 \
    antspyx==0.5.4 \
    SimpleITK==2.4.0 \
    tqdm==4.66.1 \
    faiss-cpu==1.9.0.post1 \
    langchain==0.3.9 \
    langchain-openai==0.2.10 \
    langchain_community==0.3.8

RUN pip install https://github.com/htylab/tigerbx/archive/refs/tags/v0.1.18.tar.gz

USER root
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER jovyan

# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html#dockerfiles
ENV NVIDIA_VISIBLE_DEVICES="all" \
    NVIDIA_DRIVER_CAPABILITIES="compute,utility"

# Puts the nvidia-smi binary (system management interface) on path
# with associated library files to execute it
ENV PATH="${PATH}:/usr/local/nvidia/bin" \
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/nvidia/lib64"

# 設定工作目錄
WORKDIR /NFS