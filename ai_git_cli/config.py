import os
import yaml
from string import Template

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    config = substitute_env_variables(config)
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