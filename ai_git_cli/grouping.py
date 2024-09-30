from typing import List, Dict
import openai
import json

def group_changes(changes: List[Dict], config: Dict) -> List[List[Dict]]:
    openai.api_key = config['ai_provider']['api_key']
    max_files = config['grouping']['max_files_per_commit']
    combine_similar = config['grouping']['combine_similar_changes']
    temperature = config['commit_style'].get('temperature', 0.7)

    prompt = f"""Group the following Git changes into logical commit sets:

{chr(10).join([f"- {change['change_type']} in {change['path']}" for change in changes])}

Rules:
1. Each group should have no more than {max_files} files.
2. Group related changes together.
3. {"Combine similar types of changes." if combine_similar else ""}

Provide the groups in JSON format where each group is a list of file paths."""

    response = openai.ChatCompletion.create(
        model=config['ai_provider']['model'],
        messages=[
            {"role": "system", "content": "You are a helpful assistant that groups Git changes for commits."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
    )

    try:
        groups = json.loads(response.choices[0].message.content)
        return [[change for change in changes if change['path'] in group] for group in groups]
    except json.JSONDecodeError:
        # Fallback: group all changes into one commit
        return [changes]
