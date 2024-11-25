FROM ubuntu:latest

# Install Python, dependencies, and necessary libraries
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential libcairo2-dev libpango1.0-dev ffmpeg \
    texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa

# Set the working directory
WORKDIR /dataviz_ai

# Copy application files into the container
COPY . .

# Create .env file with the API key (this is done after copying files)
ARG GOOGLE_API_KEY
RUN echo "GOOGLE_API_KEY=${GOOGLE_API_KEY}" > .env

# Create a virtual environment and install dependencies
RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8000

# Use the virtual environment's Python in the entrypoint
ENTRYPOINT ["/dataviz_ai/.venv/bin/python", "manage.py", "runserver"]
