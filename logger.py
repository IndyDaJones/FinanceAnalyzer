import logging

#Doing some basic logger configuration
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %I:%M:%S %p')
logger = logging.getLogger("MAIN")

def info(text):
    logger.info(text)
