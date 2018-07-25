import logging
import os

logger = logging.getLogger(__name__)
logger.level = logging.INFO
formatter = logging.Formatter('%(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(asctime)s %(message)s')
handler = logging.FileHandler(filename=os.path.dirname(__file__) + '/log')
handler.setFormatter(formatter)
logger.addHandler(handler)
