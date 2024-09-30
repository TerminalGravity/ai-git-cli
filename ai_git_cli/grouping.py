from typing import List, Dict
import openai

def group_changes(changes: List[Dict], config: Dict) -> List[List[Dict]]:
    # Implement AI-powered grouping logic
    openai.api_key = config['openai']['api_key']
    grouped_changes = []

    # Prepare prompt for grouping
    prompts = "Group the following Git changes into logical commit sets:\n\n"
    for change in changes:
        prompts += f"- {change['change_type'].capitalize()} in {change['path']}\n"
    prompts += "\nProvide the groups in JSON format where each group is a list of file paths."

    response = openai.Completion.create(
        engine=config['openai']['model'],
        prompt=prompts,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.3,
    )

    try:
        groups = response.choices[0].text.strip()
        grouped_paths = eval(groups)  # Caution: eval can be unsafe; consider using json
        for group in grouped_paths:
            group_changes = [change for change in changes if change['path'] in group]
            grouped_changes.append(group_changes)
    except Exception as e:
        # Fallback: group all changes into one commit
        grouped_changes.append(changes)

    return grouped_changes