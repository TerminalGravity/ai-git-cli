import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from ai_git_commit.config import Config, ConfigError
from ai_git_commit.ai_grouping import AIGrouping
from ai_git_commit.commit_message_generator import CommitMessageGenerator
from ai_git_commit.commit_automator import CommitAutomator
from ai_git_commit.diff_analyzer import DiffAnalyzer  # Assuming this exists

def commit_command(args):
    console = Console()
    try:
        config = Config()
    except ConfigError as e:
        console.print(f"[bold red]Configuration Error: {e}[/bold red]")
        sys.exit(1)
    
    analyzer = DiffAnalyzer(config)
    diffs = analyzer.get_unstaged_diffs()
    if not diffs:
        console.print("[bold red]No unstaged changes to commit.[/bold red]")
        sys.exit(0)

    console.print("[bold]Unstaged changes:[/bold]")
    for file, diff in diffs.items():
        console.print(Panel(diff, title=file, expand=False))

    grouping = AIGrouping(config)
    with console.status("[bold green]Analyzing changes...[/bold green]"):
        groups = grouping.group_diffs(diffs)

    generator = CommitMessageGenerator(config)
    table = Table(title="Proposed Commits", show_lines=True)
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Files", style="magenta", overflow="fold")
    table.add_column("Change Count", style="yellow", justify="right")
    table.add_column("Commit Message", style="green", overflow="fold")

    for idx, group in enumerate(groups, 1):
        group['diffs'] = {file: diffs[file] for file in group['files'] if file in diffs}
        suggested_message = generator.generate_message(group['diffs'])
        change_count = sum(len(diff.splitlines()) for diff in group['diffs'].values())
        table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(group['files']),
            str(change_count),
            suggested_message
        )
        group['message'] = suggested_message

    console.print(table)

    # Interactive Review
    for group in groups.copy():
        console.print(f"\n[bold cyan]Commit for files:[/bold cyan] {', '.join(group['files'])}")
        console.print(f"[bold green]Suggested Message:[/bold green] {group['message']}")
        action = Prompt.ask("Choose action", choices=["accept", "edit", "skip"], default="accept").lower()
        if action == "accept":
            continue
        elif action == "edit":
            new_message = Prompt.ask("Enter your commit message")
            group['message'] = new_message
        elif action == "skip":
            groups.remove(group)

    # Display final commits in a table
    final_table = Table(title="Final Commits", show_lines=True)
    final_table.add_column("Group", style="cyan", no_wrap=True)
    final_table.add_column("Files", style="magenta", overflow="fold")
    final_table.add_column("Change Count", style="yellow", justify="right")
    final_table.add_column("Commit Message", style="green", overflow="fold")
    
    for idx, group in enumerate(groups, 1):
        change_count = sum(len(diff.splitlines()) for diff in group['diffs'].values())
        final_table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(group['files']),
            str(change_count),
            group['message']
        )

    console.print(final_table)

    proceed = Prompt.ask("\nProceed with these commits?", choices=["y", "n"], default="y").lower()
    if proceed != 'y':
        console.print("[bold red]Commit process aborted.[/bold red]")
        sys.exit(0)

    if args.dry_run:
        console.print("[bold yellow]Dry run enabled. No commits were created.[/bold yellow]")
        sys.exit(0)

    automator = CommitAutomator(config)
    with console.status("[bold green]Creating commits...[/bold green]"):
        automator.commit_groups(groups)
    console.print("[bold green]Commits created successfully.[/bold green]")

    # Amend history if needed
    while True:
        amend_history = Prompt.ask("Do you want to amend the commit history?", choices=["y", "n"], default="n").lower()
        if amend_history in ['y', 'yes']:
            while True:
                num_commits_input = Prompt.ask("How many commits back do you want to amend?").strip()
                if not num_commits_input:
                    console.print("[yellow]No input provided. Skipping amend.[/yellow]")
                    break
                try:
                    num_commits = int(num_commits_input)
                    automator.amend_history(num_commits)
                    break
                except ValueError:
                    console.print("[red]Please enter a valid number.[/red]")
            break
        elif amend_history in ['n', 'no']:
            break
        else:
            console.print("[red]Invalid input. Please enter 'y' or 'n'.[/red]")

def analyze_command(args):
    console = Console()
    try:
        config = Config()
    except ConfigError as e:
        console.print(f"[bold red]Configuration Error: {e}[/bold red]")
        sys.exit(1)
    
    analyzer = DiffAnalyzer(config)
    diffs = analyzer.get_unstaged_diffs()
    if not diffs:
        console.print("[bold red]No unstaged changes to analyze.[/bold red]")
        sys.exit(0)

    console.print("[bold]Unstaged changes for analysis:[/bold]")
    for file, diff in diffs.items():
        console.print(Panel(diff, title=file, expand=False))

    grouping = AIGrouping(config)
    with console.status("[bold green]Analyzing changes...[/bold green]"):
        groups = grouping.group_diffs(diffs)

    generator = CommitMessageGenerator(config)
    table = Table(title="Analysis Results", show_lines=True)
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Files", style="magenta", overflow="fold")
    table.add_column("Change Count", style="yellow", justify="right")
    table.add_column("Suggested Commit Message", style="green", overflow="fold")

    for idx, group in enumerate(groups, 1):
        group['diffs'] = {file: diffs[file] for file in group['files'] if file in diffs}
        suggested_message = generator.generate_message(group['diffs'])
        change_count = sum(len(diff.splitlines()) for diff in group['diffs'].values())
        table.add_row(
            f"[bold blue]{idx}[/bold blue]",
            ", ".join(group['files']),
            str(change_count),
            suggested_message
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
    commit_parser.set_defaults(func=commit_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli_main()
