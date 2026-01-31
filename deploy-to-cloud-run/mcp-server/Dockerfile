# Use Python 3.11 slim for a small footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
# We include 'mcp' with the [http] extra if your version requires it, 
# otherwise basic 'mcp' usually covers it.
RUN pip install --no-cache-dir mcp requests

# Copy local code to the container image.
COPY weather-server.py .

# Run the web service on container startup.
# Cloud Run expects the app to listen on 0.0.0.0
CMD ["python", "weather-server.py"]