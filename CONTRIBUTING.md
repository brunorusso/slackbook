# How to Contribute

Thank you for your interest in contributing to this project! To keep our process organized and ensure all chapters are integrated correctly, please follow the workflow below.

## Contribution Rules

All chapter creation and review work is centralized in the **`new-book`** branch. Please, do not make direct pushes or Pull Requests to the `main` branch.

### 1. Create a new branch
Always create your working branch from the `new-book` branch. For example, if you are going to review chapter 10, create a branch named `chapter-10`.

```bash
# Update your local repository
git fetch origin

# Switch to the new-book branch
git checkout new-book

# Create your new branch from it
git checkout -b chapter-10
```

### 2. Submit a Pull Request

Make the necessary changes in your local editor. Once you finish writing or reviewing, save your progress, commit, and push the changes to your remote branch.

```bash
git add .
git commit -m "Add/Review chapter 10"
git push origin chapter-10
```
