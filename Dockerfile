FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Python, dependencies, and necessary libraries
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
    build-essential libcairo2-dev libpango1.0-dev ffmpeg \
    texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa

# Copy application files into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Create .env file with the API key (this is done after copying files)
ARG GOOGLE_API_KEY
RUN echo "GOOGLE_API_KEY=${GOOGLE_API_KEY}" > .env

# Create a virtual environment and install dependencies
RUN uv sync --frozen

# Expose the port that the app will run on
EXPOSE 8000

# Use the virtual environment's Python in the entrypoint
ENTRYPOINT ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
