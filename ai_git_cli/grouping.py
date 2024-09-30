from typing import List, Dict
import openai
import json

def group_changes(changes: List[Dict], config: Dict) -> List[List[Dict]]:
    # Implement AI-powered grouping logic
    openai.api_key = config['ai_provider']['api_key']
    grouped_changes = []
    max_files = config['grouping']['max_files_per_commit']
    combine_similar = config['grouping']['combine_similar_changes']
    temperature = config['commit_style'].get('temperature', 0.7)

    # Prepare prompt for grouping
    prompts = "Group the following Git changes into logical commit sets:\n\n"
    for change in changes:
        prompts += f"- {change['change_type'].capitalize()} in {change['path']}\n"
    prompts += f"\nProvide the groups in JSON format where each group is a list of file paths. Each group should have no more than {max_files} files."

    if combine_similar:
        prompts += " Ensure that similar types of changes are grouped together."

    response = openai.Completion.create(
        engine=config['ai_provider']['model'],
        prompt=prompts,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=temperature,
    )

    try:
        groups = response.choices[0].text.strip()
        grouped_paths = json.loads(groups)  # Safely parse JSON
        for group in grouped_paths:
            group_changes = [change for change in changes if change['path'] in group]
            grouped_changes.append(group_changes)
    except json.JSONDecodeError as e:
        # Fallback: group all changes into one commit
        grouped_changes.append(changes)

    return grouped_changes
