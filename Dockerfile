FROM python:3.10-slim

# Environment config to reduce logs and disable bytecode writing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Run the Django app with Gunicorn
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]
