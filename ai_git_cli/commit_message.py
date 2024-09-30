import openai
from typing import List, Dict

def generate_commit_message(groups: List[List[Dict]], config: Dict) -> List[Dict]:
    commit_messages = []
    openai.api_key = config['ai_provider']['api_key']
    commit_template = config['commit_style']['format']
    commit_types = config['commit_style']['conventional_prefixes']
    temperature = config['commit_style'].get('temperature', 0.7)

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
            engine=config['ai_provider']['model'],
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=temperature,
        )
        message = response.choices[0].text.strip()

        # Determine the commit type
        if commit_template == "conventional":
            # Example: feat: add new authentication module
            commit_type_key = types[0] if types else 'chore'
            commit_type = list(commit_types.keys())[list(commit_types.values()).index(commit_type_key.capitalize())] if commit_type_key.capitalize() in commit_types.values() else 'chore'
            formatted_message = f"{commit_type}: {message}"
        else:
            # Handle other formats or custom if needed
            formatted_message = message

        commit_messages.append({
            'message': formatted_message,
            'files': files
        })

    return commit_messages
