# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev python-dev gcc python3-dev musl-dev 
# Создаем папки для статических файлов
RUN mkdir /usr/public
RUN mkdir /usr/public/static
RUN mkdir /usr/public/media

WORKDIR /usr/src/
# ADD ./backend /usr/src/

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /usr/src/ chmod -R 755 /usr/src/ && chown -R appuser /home  && chown -R appuser /usr/public
ENV PATH="/home/appuser/.local/bin:${PATH}"
USER appuser

# Install pip requirements
ADD ./backend/requirements.txt .
RUN python -m pip install -r requirements.txt
# RUN python manage.py collectstatic

# copy entrypoint.sh
COPY ./entrypoint.sh .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder:ikcikc. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_root.wsgi"]
