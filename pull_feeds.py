from app import db, app
from datetime import datetime
from feeder.feed import Feed
import requests


logger = app.logger


def run():
    logger.info("Start Feed pull")
    f = Feed()
    results = f.process_all(force_run=True)
    logger.info("pulled all feeds")
    logger.info("Task finished: total inserted %i" % len(results))

run()

