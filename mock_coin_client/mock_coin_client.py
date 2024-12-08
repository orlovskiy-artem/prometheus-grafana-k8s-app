import time
import random
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SERVICE_URL = os.getenv('FASTAPI_SERVICE_URL', 'http://fastapi-app-service:8000')

def make_request():
    times = random.randint(1, 10)
    try:
        response = requests.get(f"{SERVICE_URL}/flip-coins?times={times}")
        if response.status_code == 200:
            result = response.json()
            logger.info(
                f"Flipped {times} coins: \
                Heads={result['heads']}, \
                Tails={result['tails']}")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error making request: {str(e)}")

def main():
    logger.info(f"Starting coin flipping mock client, targeting: {SERVICE_URL}")
    while True:
        make_request()
        sleep_time = random.uniform(3, 7)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()