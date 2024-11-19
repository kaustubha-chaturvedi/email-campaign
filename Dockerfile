FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# Add a user
RUN adduser --disabled-password --gecos "" myuser

# Set working directory
WORKDIR /code

# Copy project files
COPY . /code/

# Permissions for the code folder
RUN chown -R myuser:myuser /code
RUN chmod -R 775 /code

# Install Apache and mod_wsgi
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        apache2 \
        libapache2-mod-wsgi-py3 \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install virtualenv && mkdir /code/error \ 
    && pip install -r requirements.txt

RUN virtualenv venv && . venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput && deactivate

# Expose ports
EXPOSE 80

# Configure Apache
COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Enable mod_wsgi
RUN a2enmod wsgi

# Set up entrypoint to start Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
