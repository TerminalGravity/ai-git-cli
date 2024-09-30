import unittest
from unittest.mock import patch, MagicMock
from ai_git_cli.cli import main

class TestCLI(unittest.TestCase):
    @patch('ai_git_cli.cli.execute_commits')
    @patch('ai_git_cli.cli.generate_commit_message')
    @patch('ai_git_cli.cli.group_changes')
    @patch('ai_git_cli.cli.get_unstaged_changes')
    @patch('ai_git_cli.cli.load_config')
    def test_main_dry_run(self, mock_load_config, mock_get_unstaged_changes, mock_group_changes, mock_generate_commit_message, mock_execute_commits):
        mock_load_config.return_value = {
            'openai': {'api_key': 'test_key', 'model': 'gpt-4'},
            'git': {'user_name': 'Test User', 'user_email': 'test@example.com'},
            'commit_message': {'template': '{type}: {subject}', 'types': ['Feature']}
        }
        mock_get_unstaged_changes.return_value = [
            {'path': 'test.py', 'change_type': 'modified', 'diff': 'diff content'}
        ]
        mock_group_changes.return_value = [
            [{'path': 'test.py', 'change_type': 'modified', 'diff': 'diff content'}]
        ]
        mock_generate_commit_message.return_value = [
            {'message': 'Feature: Update test.py functionality', 'files': ['test.py']}
        ]

        test_args = ['ai-git-cli', '--dry-run']
        with patch('sys.argv', test_args):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_any_call("Dry run mode enabled. The following commits would be executed:")
                mock_print.assert_any_call("Message: Feature: Update test.py functionality")
                mock_print.assert_any_call("Files: test.py\n")
                mock_execute_commits.assert_not_called()

if __name__ == '__main__':
    unittest.main()