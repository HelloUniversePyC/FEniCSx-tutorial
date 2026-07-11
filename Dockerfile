FROM dolfinx/dolfinx:stable

WORKDIR /root/workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    matplotlib \
    scipy
    
# Correct command for idle container
CMD ["sleep", "infinity"] 
