import openai
from typing import List, Dict

def generate_commit_message(groups: List[List[Dict]], config: Dict) -> List[Dict]:
    openai.api_key = config['ai_provider']['api_key']
    commit_template = config['commit_style']['format']
    commit_types = config['commit_style']['conventional_prefixes']
    temperature = config['commit_style'].get('temperature', 0.7)

    commit_messages = []

    for group in groups:
        files = [change['path'] for change in group]
        types = list(set([change['change_type'] for change in group]))

        prompt = f"""Generate a concise and descriptive Git commit message based on the following changes:

{chr(10).join([f"- {change['change_type']} in {change['path']}" for change in group])}

Use the {commit_template} format.
{"Use one of these prefixes: " + ", ".join(commit_types.keys()) if commit_template == "conventional" else ""}
"""

        response = openai.ChatCompletion.create(
            model=config['ai_provider']['model'],
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Git commit messages."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )

        message = response.choices[0].message.content.strip()

        commit_messages.append({
            'message': message,
            'files': files
        })

    return commit_messages
