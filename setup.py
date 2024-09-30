from setuptools import setup, find_packages

setup(
    name="ai-git-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "pyyaml",
        "openai",
        "gitpython",
    ],
    entry_points={
        "console_scripts": [
            "ai-git=ai_git_cli.main:cli_main",
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='An AI-powered Git commit message generator and manager.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ai-git-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
