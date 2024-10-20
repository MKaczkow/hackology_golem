# Use a base image
FROM python:3.10-slim

# Set environment variables
ENV AGENT_URL=http://localhost:80

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your service files
COPY src/agent/ /app/agent/
COPY src/schema/ /app/schema/
COPY src/service/ /app/service/
COPY src/client/ /app/client/
COPY src/streamlit_app.py /app/streamlit_app.py

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 8502

# Run supervisor to start both services
CMD ["/usr/bin/supervisord"]
