import git
from typing import List, Dict

def get_unstaged_changes() -> List[Dict]:
    repo = git.Repo('.')
    diff = repo.index.diff(None)  # Unstaged changes
    changes = []
    for item in diff:
        change = {
            'path': item.a_path,
            'change_type': item.change_type,
            'diff': item.diff.decode('utf-8', errors='ignore')
        }
        changes.append(change)
    return changes