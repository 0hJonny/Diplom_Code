FROM golang:1.22.2-bullseye
EXPOSE 5000
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache /var/cache /var/lib/dpkg && mkdir -p /app/data
WORKDIR /app/data
CMD ["make", "run"]


# Keep the container running and keep the logs showing
# CMD ["/bin/sh","-c","mkdir -p /app/data && tail -f /dev/null"]
