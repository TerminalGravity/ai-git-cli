import openai
from typing import List, Dict

def generate_commit_message(groups: List[List[Dict]], config: Dict) -> List[Dict]:
    commit_messages = []
    openai.api_key = config['openai']['api_key']
    commit_template = config['commit_message']['template']
    commit_types = config['commit_message']['types']

    for group in groups:
        files = [change['path'] for change in group]
        types = list(set([change['change_type'] for change in group]))
        type_selected = types[0] if types else 'Update'

        # Prepare prompt for commit message
        prompt = (
            "Generate a concise and descriptive Git commit message based on the following changes:\n\n"
        )
        for change in group:
            prompt += f"- {change['change_type'].capitalize()} in {change['path']}\n"
        prompt += "\nCommit message:"

        response = openai.Completion.create(
            engine=config['openai']['model'],
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0].text.strip()

        # Apply template
        commit_type = commit_types[0] if commit_types else 'Update'
        formatted_message = commit_template.format(
            type=commit_type,
            subject=message
        )

        commit_messages.append({
            'message': formatted_message,
            'files': files
        })

    return commit_messages