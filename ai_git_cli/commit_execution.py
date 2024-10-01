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
        repo = git.Repo(repo_path)
        
        # Start interactive rebase
        repo.git.rebase('-i', f'HEAD~{num_commits}')
        
        console.print("[bold green]Rebase completed successfully.[/bold green]")
        console.print("Please review and save the changes in your default text editor.")
        
        # Wait for user to finish the rebase
        input("Press Enter when you have finished the rebase...")
        
        # Check if rebase is still in progress
        if repo.is_rebase_in_progress():
            console.print("[yellow]Rebase is still in progress. Please complete it manually.[/yellow]")
        else:
            console.print("[bold green]Rebase completed successfully.[/bold green]")
    
    except git.GitCommandError as e:
        console.print(f"[bold red]An error occurred during the rebase: {e}[/bold red]")
        console.print("You may need to resolve conflicts or abort the rebase manually.")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
