FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy shared library first
COPY libs/ ./libs/
RUN pip install -e ./libs

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy migration scripts
COPY . .

# Create non-root user
RUN useradd -m -u 1000 migrator && chown -R migrator:migrator /app
USER migrator

CMD ["python", "migrate.py"]
