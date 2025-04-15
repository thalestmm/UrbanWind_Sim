import requests
import json

import logging
import yaml
import time
import random

class RequestGenerator:
    def __init__(self, config) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.info("Starting Request Generator")

        self.min_value = config['RANGE_MIN']
        self.max_value = config['RANGE_MAX']
        self.interval = config['INTERVAL_SECONDS']
        self.url = config['URL']

    @staticmethod
    def post_value(value, url, comment):
        payload = {
            'value': round(value, 1),
            'epoch': int(time.time()),
        }
        r = requests.post(url, json=payload)
        if comment:
            logging.info(f"Payload: {json.dumps(payload)}")
            logging.info(r.text)

    def execute(self, post = True, get = True, comment=False) -> None:
        while True:
            time.sleep(self.interval)
            value = random.uniform(self.min_value, self.max_value)
            try:
                if post:
                    self.post_value(value, self.url + "/reading", comment)
            except Exception as e:
                logging.error(f"POST error: {e}")
            try:
                if get:
                    r = requests.get(self.url + "/update-chart")
                    if comment:
                        logging.info(r.text)
            except Exception as e:
                logging.error(f"GET error: {e}")

if __name__ == "__main__":
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    rg = RequestGenerator(config)
    rg.execute(post = True, get = False)
