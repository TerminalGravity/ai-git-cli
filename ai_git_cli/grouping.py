```python
from typing import List, Dict
import json
import logging
from ai_git_cli.ai_client import get_ai_client

def group_changes(changes: List[Dict], config: Dict) -> List[List[Dict]]:
    ai_client = get_ai_client(config)
    max_files = config['grouping']['max_files_per_commit']
    combine_similar = config['grouping']['combine_similar_changes']
    temperature = config['commit_style'].get('temperature', 0.7)

    prompt = create_grouping_prompt(changes, config['custom_instructions'].get('grouping', ""), config['grouping'])

    messages = [
        {"role": "system", "content": "You are a helpful assistant that groups Git changes for commits."},
        {"role": "user", "content": prompt}
    ]

    response = ai_client.get_response(messages, temperature=temperature)

    try:
        groups = json.loads(response)
        return [[change for change in changes if change['path'] in group] for group in groups]
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response for grouping. Falling back to single group.")
        return [changes]
```
