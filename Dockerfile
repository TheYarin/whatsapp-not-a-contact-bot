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

# Creating the logs folder in advance because if we let the volume mounting do it, it will be owned by the "root" user and appuser won't have permission to access it.
# This is done here and not, say, right after "WORKDIR /app" because only after "USER appuser" I was able to get the folder created under the correct user & group.
RUN mkdir /app/logs

# Install dependencies
RUN pip install pipenv
COPY --chown=appuser Pipfile* /app/
RUN pipenv install --deploy --ignore-pipfile

COPY --chown=appuser /src /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["pipenv", "run", "python", "./whatsapp_not_a_contact_bot.py"]
