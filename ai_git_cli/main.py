import sys
import git
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from ai_git_cli.config import load_config
from ai_git_cli.grouping import group_changes
from ai_git_cli.commit_message import generate_commit_message
from ai_git_cli.commit_execution import execute_commits, amend_commit_history
import argparse

def commit_command(args):
    console = Console()
    try:
        config_path = args.config if hasattr(args, 'config') and args.config else 'configs/config.yaml'
        config = load_config(config_path)
        repo = git.Repo('.')
        
        # Get unstaged changes
        diffs = repo.index.diff(None)
        if not diffs:
            console.print("[bold red]No unstaged changes to commit.[/bold red]")
            return
        
        # Display unstaged changes
        console.print("[bold]Unstaged changes for analysis:[/bold]")
        changes = []
        for diff in diffs:
            change_type = 'Modified' if diff.change_type == 'M' else diff.change_type
            changes.append({'path': diff.a_path, 'change_type': change_type})
            console.print(Panel(str(diff), title=f"{change_type}: {diff.a_path}", expand=False))

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
                new_message = Prompt.ask("Enter your commit message")
                commit['message'] = new_message
            elif action == "skip":
                commit_messages.remove(commit)

        # Confirm and execute commits
        proceed = Prompt.ask("\nProceed with these commits?", choices=["y", "n"], default="y").lower()
        if proceed != 'y':
            console.print("[bold red]Commit process aborted.[/bold red]")
            return

        if args.dry_run:
            console.print("[bold yellow]Dry run enabled. No commits were created.[/bold yellow]")
            return

        try:
            execute_commits(commit_messages, config)
            console.print("[bold green]Commits created successfully.[/bold green]")
        except ValueError as e:
            console.print(f"[bold red]Configuration error: {str(e)}[/bold red]")
        except RuntimeError as e:
            console.print(f"[bold red]Git error: {str(e)}[/bold red]")

        # Amend Commit History if requested
        amend_choice = Prompt.ask("Do you want to amend the commit history? [y/n]", choices=["y", "n"], default="n").lower()
        if amend_choice == 'y':
            while True:
                user_input = Prompt.ask("How many commits back do you want to amend? [default: 1]", default="1")
                try:
                    num_commits = int(user_input)
                    if num_commits < 1:
                        raise ValueError
                    break
                except ValueError:
                    console.print("[bold red]Please enter a valid positive integer.[/bold red]")

            try:
                amend_commit_history(repo_path='.', num_commits=num_commits)
            except Exception as e:
                console.print(f"[bold red]An error occurred while amending commits: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        console.print("[yellow]Please report this issue to the developers.[/yellow]")

def analyze_command(args):
    console = Console()
    config = load_config('configs/config.yaml')
    repo = git.Repo('.')
    
    # Get unstaged changes
    diffs = repo.index.diff(None)
    if not diffs:
        console.print("[bold red]No unstaged changes to analyze.[/bold red]")
        return

    # Display unstaged changes
    console.print("[bold]Unstaged changes for analysis:[/bold]")
    changes = []
    for diff in diffs:
        change_type = 'Modified' if diff.change_type == 'M' else diff.change_type
        changes.append({'path': diff.a_path, 'change_type': change_type})
        console.print(f"[cyan]{change_type}[/cyan]: {diff.a_path}")

    # Group changes and generate commit messages
    with console.status("[bold green]Analyzing changes...[/bold green]"):
        groups = group_changes(changes, config)
        commit_messages = generate_commit_message(groups, config)

    # Display analysis results
    table = Table(title="Analysis Results", show_lines=True)
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Files", style="magenta", overflow="fold")
    table.add_column("Suggested Commit Message", style="green", overflow="fold")

    for idx, commit in enumerate(commit_messages, 1):
        table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(commit['files']),
            commit['message']
        )

    console.print(table)

    # Add confirmation step
    confirm = Prompt.ask("Do you want to proceed with these commits?", choices=["y", "n"], default="y")
    if confirm.lower() != "y":
        console.print("[bold yellow]Commit process cancelled.[/bold yellow]")
        return

def display_commit_messages(console, commit_messages, diffs):
    table = Table(title="Proposed Commits", show_lines=True)
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Files", style="magenta", overflow="fold")
    table.add_column("Suggested Commit Message", style="green", overflow="fold")
    table.add_column("Diff Summary", style="yellow", overflow="fold")

    for idx, commit in enumerate(commit_messages, 1):
        diff_summary = []
        for diff in diffs:
            if diff.a_path in commit['files']:
                try:
                    if isinstance(diff.diff, str):
                        diff_content = diff.diff
                    else:
                        diff_content = diff.diff.decode('utf-8')
                    changes = sum(1 for line in diff_content.split('\n') if line.startswith(('+', '-')))
                    diff_summary.append(f"{diff.a_path}: {changes} changes")
                except Exception as e:
                    diff_summary.append(f"{diff.a_path}: Error processing diff")
        
        table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(commit['files']),
            commit['message'],
            "\n".join(diff_summary)
        )

    console.print(table)

def cli_main():
    import argparse

    parser = argparse.ArgumentParser(description="AI-Assisted Git Commit Tool")
    subparsers = parser.add_subparsers(dest='command')

    analyze_parser = subparsers.add_parser('analyze', help='Analyze current diffs')
    analyze_parser.set_defaults(func=analyze_command)

    commit_parser = subparsers.add_parser('commit', help='Split and commit changes with AI-generated messages')
    commit_parser.add_argument('--dry-run', action='store_true', help='Preview commits without applying them')
    commit_parser.add_argument('--config', type=str, help='Path to the configuration file')
    commit_parser.set_defaults(func=commit_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_main()