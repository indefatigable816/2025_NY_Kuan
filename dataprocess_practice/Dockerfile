FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . /app

# Install required system packages (for scientific Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --upgrade pip \
    && pip install jupyter notebook \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose Jupyter's port
EXPOSE 8888

# Start Jupyter when the container runs
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
