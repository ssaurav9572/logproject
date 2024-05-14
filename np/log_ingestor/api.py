from flask import Flask, request, jsonify
import logging
import yaml
from logger import setup_logger

app = Flask(__name__)

# Load configuration
with open("config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Setup loggers for each log file defined in the config
loggers = {}
for log_file, settings in config['logs'].items():
    loggers[log_file] = setup_logger(log_file, settings['path'], settings['level'])

@app.route('/api/<api_name>', methods=['POST'])
def api_endpoint(api_name):
    data = request.json
    log_file = config['api_to_log'][api_name]
    logger = loggers[log_file]

    log_entry = {
        "level": data.get("level", "info"),
        "log_string": data.get("log_string"),
        "timestamp": data.get("timestamp"),
        "metadata": {
            "source": log_file
        }
    }

    log_method = getattr(logger, log_entry['level'], logger.info)
    log_method(log_entry)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
