"""
Prepare for GitHub push - Windows compatible
"""
import subprocess
import sys

def check_git_remote():
    """Check if git remote is configured"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True, check=True)
        if 'origin' in result.stdout:
            print("✅ Git remote 'origin' exists:")
            print(result.stdout)
            return True
        else:
            print("⚠️  No remote repository configured")
            return False
    except:
        print("⚠️  Could not check git remotes")
        return False

def get_current_branch():
    """Get current git branch"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return "main"

def main():
    print("\n" + "=" * 70)
    print("  GitHub Preparation")
    print("=" * 70 + "\n")
    
    # Check remote
    has_remote = check_git_remote()
    
    # Current branch
    branch = get_current_branch()
    print(f"\nCurrent branch: {branch}")
    
    # Status
    print("\nGit status:")
    try:
        subprocess.run(['git', 'status', '--short'], check=False)
    except:
        pass
    
    print("\n" + "=" * 70)
    print("  Next Steps")
    print("=" * 70 + "\n")
    
    if not has_remote:
        print("1. Create a new repository on GitHub:")
        print("   - Go to https://github.com/new")
        print("   - Name it: face-liveness-detection")
        print("   - Don't initialize with README")
        print("\n2. Add remote:")
        print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
        print("\n3. Push:")
        print(f"   git push -u origin {branch}")
    else:
        print(f"✅ Ready to push!")
        print(f"\nTo push to GitHub:")
        print(f"   git push -u origin {branch}")
    
    print("\nAfter pushing, you can:")
    print("  - Deploy backend (Render/Railway)")
    print("  - Deploy frontend (Vercel)")
    print("  - Follow: DEPLOYMENT_STEPS.md")

if __name__ == "__main__":
    main()

