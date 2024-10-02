import unittest
from unittest.mock import patch, MagicMock
from ai_git_cli.commands.commit import commit_command
from ai_git_cli.commands.analyze import analyze_command

class TestAI_Git_CLI(unittest.TestCase):
    @patch('ai_git_cli.commands.commit.execute_commits')
    @patch('ai_git_cli.commands.commit.generate_commit_message')
    @patch('ai_git_cli.commands.commit.group_changes')
    @patch('ai_git_cli.commands.commit.get_unstaged_changes')
    @patch('ai_git_cli.config.load_config')
    def test_commit_command_success(self, mock_load_config, mock_get_unstaged_changes, mock_group_changes, mock_generate_commit_message, mock_execute_commits):
        mock_load_config.return_value = {
            'ai_provider': {'api_key': 'test_key', 'model': 'gpt-4'},
            'git': {'user_name': 'Test User', 'user_email': 'test@example.com'},
            'commit_style': {'format': 'conventional'},
            'grouping': {'max_files_per_commit': 5, 'combine_similar_changes': True},
            'logging': {'level': 'INFO', 'file': 'ai_git_commit.log', 'enable_console': True}
        }
        mock_get_unstaged_changes.return_value = [
            {'path': 'test.py', 'change_type': 'modified', 'diff': 'diff content'}
        ]
        mock_group_changes.return_value = [
            [{'path': 'test.py', 'change_type': 'modified', 'diff': 'diff content'}]
        ]
        mock_generate_commit_message.return_value = [
            {'message': 'feat: Update test.py functionality', 'files': ['test.py']}
        ]

        args = MagicMock()
        args.config = 'configs/config.yaml'
        args.dry_run = False

        with patch('rich.console.Console.print') as mock_print:
            commit_command(args)
            mock_execute_commits.assert_called_once()

    @patch('ai_git_cli.commands.analyze.get_unstaged_changes')
    @patch('ai_git_cli.commands.analyze.generate_commit_message')
    @patch('ai_git_cli.commands.analyze.group_changes')
    @patch('ai_git_cli.config.load_config')
    def test_analyze_command_no_changes(self, mock_load_config, mock_group_changes, mock_generate_commit_message, mock_get_unstaged_changes):
        mock_load_config.return_value = {}
        mock_get_unstaged_changes.return_value = []
        args = MagicMock()
        args.config = 'configs/config.yaml'

        with patch('rich.console.Console.print') as mock_print:
            analyze_command(args)
            mock_print.assert_any_call("[bold red]No unstaged changes to analyze.[/bold red]")

if __name__ == '__main__':
    unittest.main()