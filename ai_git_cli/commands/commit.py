
import git
from rich.console import Console
from rich.prompt import Prompt
from ai_git_cli.config.loader import load_config
from ai_git_cli.grouping import group_changes
from ai_git_cli.commit_message import generate_commit_message
from ai_git_cli.commit_execution import execute_commits, amend_commit_history
from ai_git_cli.utils.git_helper import get_unstaged_changes, display_commit_messages
from ai_git_cli.utils.logger import setup_logger

def commit_command(args):
    console = Console()
    logger = setup_logger(__name__)
    try:
        config = load_config(args.config)
        repo = git.Repo('.')
        
        # Get unstaged changes
        diffs = get_unstaged_changes(repo)
        if not diffs:
            console.print("[bold red]No unstaged changes to commit.[/bold red]")
            return
        
        # Display unstaged changes
        console.print("[bold]Unstaged changes for analysis:[/bold]")
        changes = []
        for diff in diffs:
            change_type = 'Modified' if diff['change_type'] == 'M' else diff['change_type']
            changes.append({'path': diff['path'], 'change_type': change_type})
            console.print(f"[cyan]{change_type}[/cyan]: {diff['path']}")
        
        if not changes:
            console.print("[yellow]No unstaged changes found.[/yellow]")
            return

        # Analyze and group changes
        console.print("[bold green]Analyzing and grouping changes...[/bold green]")
        groups = group_changes(changes, config)

        # Generate commit messages
        console.print("[bold green]Generating commit messages...[/bold green]")
        commit_messages = generate_commit_message(groups, config)

        # Display analysis results
        display_commit_messages(console, commit_messages, diffs)

        # Interactive Review
        for commit in commit_messages.copy():
            console.print(f"\n[bold cyan]Commit for files:[/bold cyan] {', '.join(commit['files'])}")
            console.print(f"[bold green]Suggested Message:[/bold green] {commit['message']}")
            action = Prompt.ask("Choose action", choices=["accept", "edit", "skip"], default="accept").lower()
            if action == "accept":
                continue
            elif action == "edit":
                commit['message'] = Prompt.ask("Enter your commit message")
            elif action == "skip":
                commit_messages.remove(commit)

        # Confirm and execute commits
        proceed = Prompt.ask("\nProceed with these commits?", choices=["y", "n"], default="y").lower()
        if proceed != 'y':
            console.print("[bold red]Commit process aborted.[/bold red]")
            return

        if args.dry_run:
            console.print("[bold yellow]Dry run enabled. The following commits would be executed:[/bold yellow]")
            for commit in commit_messages:
                console.print(f"Message: {commit['message']}\nFiles: {', '.join(commit['files'])}\n")
            return

        try:
            execute_commits(commit_messages, config)
            console.print("[bold green]Commits created successfully.[/bold green]")
        except ValueError as e:
            console.print(f"[bold red]Configuration error: {str(e)}[/bold red]")
        except RuntimeError as e:
            console.print(f"[bold red]Git error: {str(e)}[/bold red]")

        # Amend Commit History if requested
        amend_choice = Prompt.ask("Do you want to amend the commit history?", choices=["y", "n"], default="n").lower()
        if amend_choice == 'y':
            try:
                amend_commit_history(repo_path='.', num_commits=config['grouping']['max_files_per_commit'])
                console.print("[bold green]Successfully amended the commit history.[/bold green]")
            except Exception as e:
                console.print(f"[bold red]An error occurred while amending commits: {e}[/bold red]")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        console.print("[yellow]Please report this issue to the developers.[/yellow]")