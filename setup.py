import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="ai-git-cli",
    version="0.1.0",
    packages=find_packages(include=['ai_git_cli', 'ai_git_cli.*']),
    include_package_data=True,
    install_requires=[
        "GitPython>=3.1.0",
        "openai>=1.0.0",
        "rich>=12.0.0",
        "PyYAML>=6.0",
        "pydantic>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-git-cli=ai_git_cli.main:cli_main",
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='An AI-powered Git commit message generator and manager.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ai-git-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)