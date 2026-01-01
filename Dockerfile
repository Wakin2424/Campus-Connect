# Base image
FROM python:3.11.9

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONNUNBUFFERED=1\
    PIP_NO_CACHE_DIR=1\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Setting the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Install python dependancies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the project code
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# 8. Define the default startup command
# Use gunicorn for production or runserver for development
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "Campus_Connect.asgi:application"]