import git
from typing import List, Dict
import subprocess
import logging
from rich.console import Console

def execute_commits(commit_messages: List[Dict], config: Dict):
    try:
        repo = git.Repo('.')
        repo.config_writer().set_value("user", "name", config['git']['user_name']).release()
        repo.config_writer().set_value("user", "email", config['git']['user_email']).release()
        
        for commit in commit_messages:
            repo.git.add(commit['files'])
            repo.git.commit('-m', commit['message'])
    except KeyError as e:
        raise ValueError(f"Missing configuration: {str(e)}") from e
    except git.GitCommandError as e:
        raise RuntimeError(f"Git command failed: {str(e)}") from e

def amend_commit_history(repo_path: str, num_commits: int):
    console = Console()
    try:
        # Example: Rebase interactively to amend commit messages
        subprocess.run(['git', 'rebase', '-i', f'HEAD~{num_commits}'], check=True, cwd=repo_path)
        console.print("[bold green]Successfully amended the commit history.[/bold green]")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error amending commit history: {e}")
        console.print(f"[bold red]Failed to amend commit history: {e}[/bold red]")
