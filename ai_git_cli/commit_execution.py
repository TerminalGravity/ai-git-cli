import git
from typing import List, Dict

def execute_commits(commit_messages: List[Dict], config: Dict):
    repo = git.Repo('.')
    repo.config_writer().set_value("user", "name", config['git']['user_name']).release()
    repo.config_writer().set_value("user", "email", config['git']['user_email']).release()

    for commit in commit_messages:
        for file_path in commit['files']:
            repo.index.add([file_path])
        repo.index.commit(commit['message'])