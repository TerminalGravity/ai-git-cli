import os
import yaml
from string import Template
import logging
from dotenv import load_dotenv

def load_config(config_path: str = 'configs/config.yaml') -> dict:
    load_dotenv()  # Load environment variables from .env file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    config = substitute_env_variables(config)
    setup_logging(config)
    return config

def substitute_env_variables(config):
    if isinstance(config, dict):
        return {k: substitute_env_variables(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [substitute_env_variables(i) for i in config]
    elif isinstance(config, str):
        template = Template(config)
        try:
            return template.substitute(os.environ)
        except KeyError as e:
            raise ValueError(f"Missing environment variable for config: {e}")
    else:
        return config

def setup_logging(config):
    logging_config = config.get('logging', {})
    level = getattr(logging, logging_config.get('level', 'INFO').upper(), logging.INFO)
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = []
    if logging_config.get('file'):
        file_handler = logging.FileHandler(logging_config['file'])
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    if logging_config.get('enable_console', False):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)
    
    if handlers:
        logging.basicConfig(level=level, handlers=handlers)
    else:
        logging.basicConfig(level=level, format=log_format)
