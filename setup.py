import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-git-cli",
    version="0.1.0",
    author="terminalgravity",
    author_email="jrinnfelke@gmail.com",
    description="AI-Assisted Git Commit Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/terminalgravity/ai-git-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "GitPython>=3.1.0",
        "openai>=1.0.0",
        "rich>=12.0.0",
        "PyYAML>=6.0",
        "pydantic>=1.10.0",
        "termcolor>=2.3.0",
    ],
    entry_points={
        'console_scripts': [
            'ai-git-cli=ai_git_cli.cli:cli_main',
        ],
    },
    include_package_data=True,
    package_data={
        'ai_git_cli': ['configs/*.yaml'],
    },
)