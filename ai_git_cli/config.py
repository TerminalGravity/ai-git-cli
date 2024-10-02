from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional
import os
import yaml
from string import Template
from dotenv import load_dotenv
import logging
from rich.console import Console

class AIProviderConfig(BaseModel):
    name: str
    model: str
    api_key: str

class CommitStyleConfig(BaseModel):
    format: str
    conventional_prefixes: Dict[str, str]
    length: str
    emoji: bool
    temperature: float

class GroupingConfig(BaseModel):
    max_files_per_commit: int
    combine_similar_changes: bool

class CustomInstructionsConfig(BaseModel):
    grouping: str
    message_style: str
    user_feedback: Optional[str] = ""

class UserInterfaceConfig(BaseModel):
    language: str
    color_scheme: str

class GitIntegrationConfig(BaseModel):
    install_hook: bool
    hook_type: str

class AdvancedSettingsConfig(BaseModel):
    token_limit: int

class Config(BaseModel):
    ai_provider: AIProviderConfig
    commit_style: CommitStyleConfig
    grouping: GroupingConfig
    custom_instructions: CustomInstructionsConfig
    user_interface: UserInterfaceConfig
    git_integration: GitIntegrationConfig
    advanced: AdvancedSettingsConfig
    logging: Optional[Dict[str, str]] = None

def load_config(config_path: str = 'configs/config.yaml') -> Config:
    load_dotenv()  # Load environment variables from .env file
    console = Console()
    with open(config_path, 'r') as file:
        config_raw = yaml.safe_load(file)
    config_raw = substitute_env_variables(config_raw)
    try:
        config = Config(**config_raw)
    except ValidationError as e:
        console.print(f"[bold red]Configuration validation error: {e}[/bold red]")
        raise e
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

def setup_logging(config: Config):
    logging_config = config.logging
    if not logging_config:
        logging_config = {
            'level': 'INFO',
            'file': 'ai_git_commit.log',
            'enable_console': True
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