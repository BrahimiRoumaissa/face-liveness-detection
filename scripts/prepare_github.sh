#!/bin/bash
# Script to prepare for GitHub push

echo "=================================="
echo "GitHub Preparation"
echo "=================================="

# Check if remote exists
if git remote -v | grep -q origin; then
    echo "✅ Git remote 'origin' already exists"
    git remote -v
else
    echo "⚠️  No remote repository configured"
    echo ""
    echo "To add your GitHub repository:"
    echo "  1. Create a new repository on GitHub"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "  3. Run: git push -u origin main"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added: $repo_url"
    fi
fi

# Check current branch
current_branch=$(git branch --show-current)
echo ""
echo "Current branch: $current_branch"

# Show status
echo ""
echo "Git status:"
git status --short

echo ""
echo "=================================="
echo "Ready to push!"
echo "=================================="
echo ""
echo "To push to GitHub:"
echo "  git push -u origin $current_branch"
echo ""

