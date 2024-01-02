FROM python:3.10

# Install spaCy dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
                          git \
                          curl \
                          libssl-dev \
                          libffi-dev \
                          python3-dev \
                          python3-pip \
                          python3-setuptools \
                          python3-wheel

# Install spaCy and numerizer
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


WORKDIR /app
COPY . /app

RUN pip install -U spacy && python -m spacy download en_core_web_sm

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "importspacy.py"]
