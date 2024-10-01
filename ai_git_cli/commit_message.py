```python
from typing import List, Dict
from ai_git_cli.ai_client import get_ai_client
from ai_git_cli.config import load_config
from ai_git_cli.prompts import create_commit_message_prompt

def generate_commit_message(groups: List[List[Dict]], config: Dict) -> List[Dict]:
    ai_client = get_ai_client(config)
    temperature = config['commit_style'].get('temperature', 0.7)
    user_feedback = config['custom_instructions'].get('user_feedback', "")

    commit_style = config['commit_style']
    commit_messages = []
    for group in groups:
        prompt = create_commit_message_prompt(group, user_feedback, commit_style)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates Git commit messages."},
            {"role": "user", "content": prompt}
        ]
        message = ai_client.get_response(messages, temperature=temperature)
        commit_messages.append({
            'message': message,
            'files': [change['path'] for change in group]
        })

    return commit_messages
```
