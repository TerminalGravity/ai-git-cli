from typing import List, Dict
import json
import logging
from ai_git_cli.ai_client import get_ai_client
from ai_git_cli.prompts import create_grouping_prompt

def group_changes(changes: List[Dict], config: Dict) -> List[List[Dict]]:
    ai_client = get_ai_client(config)
    temperature = config['commit_style'].get('temperature', 0.7)
    user_feedback = config['custom_instructions'].get('user_feedback', "")
    grouping = config['grouping']

    prompt = create_grouping_prompt(changes, user_feedback, grouping)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that groups Git changes into logical commit sets."},
        {"role": "user", "content": prompt}
    ]
    response = ai_client.get_response(messages, temperature=temperature)
    
    try:
        grouped_changes = json.loads(response)
        return [
            [change for change in changes if change['path'] in group]
            for group in grouped_changes
        ]
    except json.JSONDecodeError:
        # Fallback to a single group if JSON parsing fails
        return [changes]
