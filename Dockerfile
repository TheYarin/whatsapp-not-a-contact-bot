# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN mkdir /home/appuser
RUN useradd appuser && chown -R appuser /app /home/appuser
USER appuser
ENV PATH=${PATH}:/home/appuser/.local/bin
COPY --chown=appuser . /app

# Install dependencies
RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --deploy --ignore-pipfile

COPY /src /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["pipenv", "run", "python", "./whatsapp_not_a_contact_bot.py"]
