import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "level": record.levelname.lower(),
            "log_string": record.getMessage(),
            "timestamp": record.created,
            "metadata": {
                "source": record.name
            }
        }
        return json.dumps(log_entry)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(JsonFormatter())
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
