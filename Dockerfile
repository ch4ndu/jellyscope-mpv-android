FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    autoconf automake pkg-config libtool ninja-build python3 python3-venv \
    python3-pip python3-jinja2 python3-jsonschema gperf nasm unzip wget curl \
    git ca-certificates build-essential cmake && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv --system-site-packages /opt/mpv-build \
    && /opt/mpv-build/bin/pip install --no-cache-dir meson==1.6.1
ENV PATH="/opt/mpv-build/bin:${PATH}"
WORKDIR /bundle
