from typing import List, Dict
from rich.table import Table
from rich.console import Console
import git
from rich import box

def get_unstaged_changes(repo: git.Repo) -> List[Dict]:
    diffs = repo.index.diff(None)
    changes = []
    for diff in diffs:
        change_type = 'Modified' if diff.change_type == 'M' else diff.change_type
        changes.append({
            'path': diff.a_path,
            'change_type': change_type,
            'diff': diff.diff.decode('utf-8', errors='ignore') if isinstance(diff.diff, bytes) else diff.diff
        })
    return changes

def display_commit_messages(console: Console, commit_messages: List[Dict], diffs: List[git.diff.Diff]) -> List[Dict]:
    table = Table(title="Proposed Commits", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Files", style="magenta", overflow="fold")
    table.add_column("Suggested Commit Message", style="green", overflow="fold")
    table.add_column("Diff Summary", style="yellow", overflow="fold")

    for idx, commit in enumerate(commit_messages, 1):
        diff_summary = []
        for diff in diffs:
            if diff.a_path in commit['files']:
                try:
                    diff_content = diff.diff.decode('utf-8') if isinstance(diff.diff, bytes) else diff.diff
                    changes = sum(1 for line in diff_content.split('\n') if line.startswith(('+', '-')))
                    diff_summary.append(f"{diff.a_path}: {changes} changes")
                except Exception:
                    diff_summary.append(f"{diff.a_path}: Error processing diff")
        
        table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(commit['files']),
            commit['message'],
            "\n".join(diff_summary)
        )

    console.print(table)
    return commit_messages