# Set the Python base image
FROM python:3

# Set environment variables
ENV USER lanlords
ENV HOME /home/lanlords
ENV EXEC /bin/lanlords

################## BEGIN INSTALLATION ######################

# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

# Copy application code
COPY src/main.py $EXEC
RUN chmod +x $EXEC

# Create the application user
RUN useradd -m -d $HOME $USER

# Switch user and set working directory
USER $USER
WORKDIR $HOME

##################### INSTALLATION END #####################

# Set default command and options
ENTRYPOINT ["/bin/lanlords"]
