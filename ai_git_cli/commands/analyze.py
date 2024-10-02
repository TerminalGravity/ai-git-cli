from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from ai_git_cli.config.loader import load_config
from ai_git_cli.grouping import group_changes
from ai_git_cli.commit_message import generate_commit_message
from ai_git_cli.utils.git_helper import get_unstaged_changes
from ai_git_cli.utils.logger import setup_logger

def analyze_command(args):
    console = Console()
    logger = setup_logger(__name__)
    try:
        config = load_config(args.config)
        repo = git.Repo('.')
        
        # Get unstaged changes
        diffs = get_unstaged_changes(repo)
        if not diffs:
            console.print("[bold red]No unstaged changes to analyze.[/bold red]")
            return

        # Display unstaged changes
        console.print("[bold]Unstaged changes for analysis:[/bold]")
        changes = []
        for diff in diffs:
            change_type = 'Modified' if diff['change_type'] == 'M' else diff['change_type']
            changes.append({'path': diff['path'], 'change_type': change_type})
            console.print(f"[cyan]{change_type}[/cyan]: {diff['path']}")

        # Analyze and group changes
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
    except Exception as e:
        logger.error(f"An unexpected error occurred during analysis: {e}")
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        console.print("[yellow]Please report this issue to the developers.[/yellow]")
