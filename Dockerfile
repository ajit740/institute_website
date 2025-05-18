FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies (modify if you have requirements.txt)
RUN pip install --upgrade pip
RUN pip install .

# Command to run app
CMD ["python", "main.py"]
