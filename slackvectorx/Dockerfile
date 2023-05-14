# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster
USER  slackvectorx
# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to working directory
COPY . /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Run the command to start your application
CMD ["python", "main.py"]
