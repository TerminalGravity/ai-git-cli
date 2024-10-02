import argparse
from rich.console import Console
from ai_git_cli.commands.commit import commit_command
from ai_git_cli.commands.analyze import analyze_command
from ai_git_cli.utils.logger import setup_logger

def cli_main():
    console = Console()
    logger = setup_logger(__name__)
    
    parser = argparse.ArgumentParser(description="AI-Assisted Git Commit Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Commit Command Parser
    commit_parser = subparsers.add_parser('commit', help='Split and commit changes with AI-generated messages')
    commit_parser.add_argument('--dry-run', action='store_true', help='Preview commits without applying them')
    commit_parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to the configuration file')
    commit_parser.set_defaults(func=commit_command)
    
    # Analyze Command Parser
    analyze_parser = subparsers.add_parser('analyze', help='Analyze current diffs')
    analyze_parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to the configuration file')
    analyze_parser.set_defaults(func=analyze_command)
    
    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        console.print(f"[bold red]Error: {e}[/bold red]")
        parser.print_help()

if __name__ == "__main__":
    cli_main()