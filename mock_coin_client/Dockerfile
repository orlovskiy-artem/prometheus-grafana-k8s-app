FROM python:3.9.1-slim

WORKDIR /app

# Install requirements
RUN pip install requests

# Copy the script
COPY mock_coin_client.py .

CMD ["python", "mock_coin_client.py"]