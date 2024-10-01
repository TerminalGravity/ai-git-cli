from typing import List, Dict

def create_commit_message_prompt(group: List[Dict], user_feedback: str, commit_style: Dict) -> str:
    files = "\n".join([f"- {change['change_type'].capitalize()} in {change['path']}" for change in group])
    prompt = f"""Generate a concise and descriptive Git commit message based on the following changes that {user_feedback}:
{files}

Use the {commit_style['format']} format. Provide the commit message in JSON format with 'type' and 'subject' fields."""
    if commit_style['format'] == "conventional":
        prefixes = ", ".join(commit_style['conventional_prefixes'].keys())
        prompt += f" Use one of these prefixes for the 'type' field: {prefixes}."
    return prompt

def create_grouping_prompt(changes: List[Dict], user_feedback: str, grouping: Dict) -> str:
    changes_formatted = "\n".join([f"- {change['change_type'].capitalize()} in {change['path']}" for change in changes])
    prompt = f"Group the following Git changes into logical commit sets that {user_feedback}:\n{changes_formatted}\n\nProvide the groups in JSON format where each group is a list of file paths. Each group should have no more than {grouping['max_files_per_commit']} files."
    if grouping['combine_similar_changes']:
        prompt += " Ensure that similar types of changes are grouped together."
    return prompt
