FROM python:3.10-slim

<<<<<<< HEAD
# Install dependencies
RUN apt-get update && apt-get install -y curl build-essential \
=======
RUN apt-get update && apt-get install -y curl build-essential libpq-dev gcc \
>>>>>>> ff933bb (Rename Dockerfile and fix pip install command)
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

ENV PATH="/root/.cargo/bin:$PATH"

<<<<<<< HEAD
# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies (modify if you have requirements.txt)
RUN pip install --upgrade pip
RUN pip install .

# Command to run app
CMD ["python", "main.py"]
=======
WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> ff933bb (Rename Dockerfile and fix pip install command)
