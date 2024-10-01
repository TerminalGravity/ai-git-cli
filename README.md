# AI-Git-CLI Tool Documentation

## Introduction

The AI-Git-CLI Tool assists developers in creating structured and meaningful Git commit messages using artificial intelligence. It analyzes unstaged changes, groups them logically, generates descriptive commit messages, and automates the commit process.

## Installation

Install the tool via PyPi:

```bash
pip install ai-git-cli
```

## Custom Instructions During Commit

The `AI-Git-CLI` tool now allows you to provide custom instructions or prompts during the commit process. This feature enables the AI to incorporate your specific feedback, resulting in more tailored commit messages and logically grouped changes.

### How to Use

1. **Initiate Commit:**
   Run the commit command as usual:
   ```bash
   ai-git-cli commit [--config configs/config.yaml]
   ```
2. **Provide Custom Instructions:**
   During the commit process, you'll be prompted:
   ```
   Do you want to add any custom instructions for the AI? [y/n]: y
   Enter your custom instructions: Focus on summarizing new features and bug fixes clearly.
   ```
3. **AI-Enhanced Commit:**
   The AI will generate commit messages and group changes based on your provided instructions, ensuring that the commits align with your specific preferences and project needs.

### Benefits

- **Personalized Commit Messages:** Tailor commit messages to reflect the nuances of your project.
- **Improved Change Grouping:** Logical grouping of changes based on your instructions enhances codebase maintainability.
- **Enhanced Workflow:** Integrates seamlessly into your existing Git workflow, providing AI assistance without disrupting your development process.

### Example Interaction

```
ai-git-cli commit --config configs/config.yaml
Unstaged changes:
┏━━━━━━━━━━━━━━━┓
┃ README.md      ┃
┣━━━━━━━━━━━━━━━┫
┃ ...diff details... ┃
┗━━━━━━━━━━━━━━━┛
Do you want to add any custom instructions for the AI? [y/n]: y
Enter your custom instructions: Emphasize performance improvements and code refactoring in the commit messages.
Analyzing and grouping changes...
Generating commit messages...
Proposed Commits
┏━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Group ┃ Files         ┃ Commit Message             ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1     │ README.md     │ refactor: Improved documentation clarity. │
│ 2     │ app.py        │ feat: Enhanced performance in data processing. │
└───────┴───────────────┴─────────────────────────────┘
Commit for files: README.md
Suggested Message: refactor: Improved documentation clarity.
Choose action [accept/edit/skip]: accept
Commit for files: app.py
Suggested Message: feat: Enhanced performance in data processing.
Choose action [accept/edit/skip]: accept
Proceed with these commits? [y/n]: y
Commits created successfully.
Do you want to amend the commit history? [y/n]: n
```

This feature empowers you to guide the AI, ensuring that the generated commits are aligned with your project's specific requirements and your personal or team preferences.