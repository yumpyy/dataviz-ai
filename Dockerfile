FROM ubuntu:latest

WORKDIR /dataviz_ai
COPY . .

RUN apt-get update && apt-get -y upgrade
RUN apt-get install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg
RUN apt install texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science tipa

EXPOSE 8000

RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "-c", ".venv/bin/python manage.py runserver"]
