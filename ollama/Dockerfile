FROM ollama/ollama:0.1.31

# Check if lspci command is available, install pciutils, and clear the cache
# Check for NVIDIA GPU and install NVIDIA Container Toolkit if present
RUN apt-get update && \
    apt-get install -y pciutils && \
    if lspci | grep -i nvidia; then \
        apt-get install -y --no-install-recommends \
            curl \
            gnupg2 \
            ca-certificates && \
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
        curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
        apt-get update && \
        apt-get install -y nvidia-container-toolkit && \
        systemctl restart docker && \
        nvidia-ctk runtime configure --runtime=docker; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the script to start the server and additional commands
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

# Define the ENTRYPOINT and CMD
ENTRYPOINT ["/usr/local/bin/start.sh"]