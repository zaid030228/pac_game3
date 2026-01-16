# Instructions to Push to GitHub

## After creating the repository on GitHub, run these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pacman-game.git

# Rename branch to main (if not already)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Alternative: If you want to use SSH instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/pacman-game.git
git branch -M main
git push -u origin main
```

## If you need to set up Git identity first:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
