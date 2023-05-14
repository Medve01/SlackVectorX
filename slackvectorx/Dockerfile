# Use an official Python runtime as a parent image
FROM python:slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to working directory
COPY . /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Create and use a new user
RUN useradd -ms /bin/bash slackvectorx
USER  slackvectorx

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s CMD python3 -c 'import sys, urllib.request; sys.exit(urllib.request.urlopen("http://localhost:8080/healthcheck").getcode() != 200)'


# Run the command to start your application
CMD ["python", "main.py"]
