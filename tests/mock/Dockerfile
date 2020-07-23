# Set the Python base image
FROM python:3

# Set environment variables
ENV HOME /api

################## BEGIN INSTALLATION ######################

# Install Mock Server
RUN pip install --no-cache-dir mock-server

# Create working directory
RUN mkdir -p $HOME

# Set working directory
WORKDIR $HOME

##################### INSTALLATION END #####################

# Expose the http port
EXPOSE 8888/tcp

# Set default command and options
ENTRYPOINT ["/usr/local/bin/mock-server"]
CMD ["--address=0.0.0.0", "--port=8888", "--dir=/api"]
