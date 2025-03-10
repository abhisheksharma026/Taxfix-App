from loguru import logger

logger.remove()

logger.add('info.log', 
           format="{time} {level} {message}", 
           level="INFO", 
           rotation='1MB', 
           compression='zip',
           backtrace=True,
           diagnose=True)
logger.add('errors.log',
           format="{time} {level} {message}",
           level="ERROR",
           rotation='1MB',
           compression='zip')

