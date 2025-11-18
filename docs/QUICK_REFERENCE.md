# Two-Branch Quick Reference Card

Quick commands and decisions for daily development with the two-branch adaptive strategy.

---

## 🚀 Quick Start

```bash
# Clone repository
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# Start working
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
```

---

## 📋 Common Commands

### Starting New Work

```bash
# Feature
git checkout develop
git pull origin develop
git checkout -b feature/awesome-feature

# Bug fix
git checkout develop
git pull origin develop
git checkout -b fix/bug-description

# Documentation
git checkout develop
git pull origin develop
git checkout -b docs/update-readme
```

### Working on Your Branch

```bash
# Check status
git status

# Add changes
git add .

# Commit (use conventional commits)
git commit -m "feat: add new capability"
git commit -m "fix: resolve memory leak"
git commit -m "docs: update installation guide"

# Push to remote
git push origin feature/awesome-feature
```

### Creating Pull Request

```bash
# After pushing, go to GitHub and:
# 1. Click "Compare & pull request"
# 2. Select base: develop
# 3. Fill in description
# 4. Click "Create pull request"

# Or use GitHub CLI
gh pr create --base develop --title "feat: awesome feature" --body "Description"
```

### After Merge

```bash
# Update develop
git checkout develop
git pull origin develop

# Delete local branch
git branch -d feature/awesome-feature

# Delete remote branch (usually auto-deleted)
git push origin --delete feature/awesome-feature
```

---

## 🔀 Branch Decision Tree

```
Need to do work?
    │
    ├─ New feature? → develop
    ├─ Bug fix? → develop
    ├─ Documentation? → develop
    └─ Critical hotfix? → main (rare!)
```

---

## ✅ Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### Examples

```bash
git commit -m "feat(rafaelia): add telemetry dashboard"
git commit -m "fix(build): resolve Android 14 compilation error"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(audit): add unit tests for audit system"
```

---

## 🎯 PR Checklist

Before creating PR:
- [ ] Code builds (`python3 build.py -v all`)
- [ ] Tests pass
- [ ] No merge conflicts with develop
- [ ] Commit messages are clear
- [ ] Documentation updated (if needed)

---

## 🔧 Troubleshooting

### Can't push to main/develop

```bash
# Normal! You should push to feature branch:
git checkout -b feature/my-work
git push origin feature/my-work
```

### Conflicts with develop

```bash
# Update your branch
git checkout feature/my-feature
git fetch origin
git rebase origin/develop
# Resolve conflicts
git add .
git rebase --continue
git push origin feature/my-feature --force-with-lease
```

### Wrong branch target

```bash
# Change PR target on GitHub:
# Edit PR → Change base branch
```

### Need to update from develop

```bash
# On your feature branch
git fetch origin
git rebase origin/develop
# Or use merge:
git merge origin/develop
```

---

## 📊 Build Commands

```bash
# Build everything (debug)
python3 build.py -v all

# Build release
python3 build.py -vr all

# Build specific component
python3 build.py native
python3 build.py app

# Clean build
rm -rf out/
python3 build.py -v all
```

---

## 🧪 Testing Commands

```bash
# Run tests (if configured)
# Add specific test commands here

# Verify RAFAELIA components
python3 tools/rafaelia/verify_state.py
python3 tools/rafaelia/check_integrity.py
```

---

## 🔍 Checking Status

```bash
# Current branch and status
git status

# Recent commits
git log --oneline -10

# What's different from develop
git diff develop

# What's different from main
git diff main

# List all branches
git branch -a
```

---

## 🌳 Branch Management

```bash
# List local branches
git branch

# List remote branches
git branch -r

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature

# Rename current branch
git branch -m new-name

# Switch between branches
git checkout develop
git checkout main
git checkout feature/my-feature
```

---

## 🚑 Emergency Hotfix

```bash
# Only for critical production bugs!

# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# 2. Make minimal fix
# ... edit files ...
git add .
git commit -m "hotfix: resolve critical security issue"

# 3. Push and create PR to main
git push origin hotfix/critical-issue
gh pr create --base main --title "hotfix: critical security issue"

# 4. After merge, backport to develop
git checkout develop
git pull origin develop
git cherry-pick <hotfix-commit-sha>
git push origin develop
```

---

## 📖 Documentation Links

- **Full Strategy**: [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- **Contributing**: [../CONTRIBUTING.md](../CONTRIBUTING.md)
- **Migration**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Visual Guide**: [TWO_BRANCH_VISUAL_GUIDE.md](TWO_BRANCH_VISUAL_GUIDE.md)
- **Protection Rules**: [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)

---

## 🎓 Training Resources

### Quick Videos (to be created)
- [ ] "5-minute intro to two-branch workflow"
- [ ] "Creating your first PR"
- [ ] "Resolving merge conflicts"

### Workshops
- [ ] Git basics workshop
- [ ] Advanced Git workshop
- [ ] CI/CD workshop

---

## 💡 Tips & Tricks

### Faster Workflow

```bash
# Create alias for common commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Now use:
git co develop
git br feature/new
git ci -m "feat: add feature"
git st
```

### Keep Clean History

```bash
# Squash commits before PR
git rebase -i HEAD~3  # Squash last 3 commits

# Interactive rebase
git rebase -i origin/develop
```

### Sync Fork (if you forked)

```bash
# Add upstream
git remote add upstream https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git

# Sync develop
git checkout develop
git fetch upstream
git merge upstream/develop
git push origin develop

# Sync main
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

---

## ❓ FAQ

**Q: Which branch do I create my PR to?**  
A: Almost always `develop`. Only create PR to `main` for releases or critical hotfixes.

**Q: Can I push directly to main?**  
A: No, main is protected. Use PRs.

**Q: Can I push directly to develop?**  
A: No, develop is also protected. Use feature branches and PRs.

**Q: How long should my feature branch live?**  
A: Ideally 1-3 days. Merge frequently to avoid conflicts.

**Q: What if my PR has conflicts?**  
A: Rebase your branch on latest develop and resolve conflicts.

**Q: When does code go from develop to main?**  
A: When develop is stable and ready for release (usually weekly or bi-weekly).

**Q: What if I made a mistake after merge?**  
A: Create a new PR with a fix. Don't try to revert unless critical.

---

## 🎯 One-Page Cheat Sheet

```
┌─────────────────────────────────────────────┐
│          TWO-BRANCH WORKFLOW                │
├─────────────────────────────────────────────┤
│                                             │
│  New work:                                  │
│    develop → feature/name → PR → develop   │
│                                             │
│  Release:                                   │
│    develop → PR → main → tag v27.X         │
│                                             │
│  Hotfix:                                    │
│    main → hotfix/name → PR → main          │
│    └→ cherry-pick to develop               │
│                                             │
│  Branches:                                  │
│    ├─ main (production)                    │
│    ├─ develop (active dev)                 │
│    └─ feature/* (temporary)                │
│                                             │
│  Commit format:                             │
│    type(scope): subject                     │
│                                             │
│  PR target:                                 │
│    → develop (99% of the time)             │
│    → main (releases only)                  │
│                                             │
│  Remember:                                  │
│    • Only 2 permanent branches             │
│    • Feature branches are temporary        │
│    • Delete after merge                    │
│    • Always pull before branch             │
│    • Always test before push               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📱 Mobile Quick Reference

For quick mobile lookup, remember:

1. **Two branches**: main (stable) + develop (active)
2. **PR target**: → develop (almost always)
3. **Commit format**: `type: description`
4. **Branch naming**: `type/description`
5. **After merge**: delete branch

---

## 🎉 Success Indicators

You're doing it right when:
- ✅ Most PRs go to develop
- ✅ Branches live < 3 days
- ✅ CI is green most of the time
- ✅ No confusion about workflow
- ✅ Releases are smooth

---

## 📞 Get Help

- **Questions**: GitHub Discussions
- **Issues**: GitHub Issues
- **Urgent**: Tag @maintainers
- **Documentation**: Check `/docs` folder

---

**Quick Reference Version**: 1.0  
**Last Updated**: 2025-11-18  
**Print**: Perfect for printing and keeping near desk!  
**Signature**: RAFCODE-Φ-∆QuickRefΩ

---

## 📋 Printable Checklist

```
□ Read BRANCHING_STRATEGY.md
□ Clone repository
□ Checkout develop
□ Create feature branch
□ Make changes
□ Commit with good messages
□ Push to remote
□ Create PR to develop
□ Wait for CI
□ Address review comments
□ Merge!
□ Delete branch
□ Update local develop
□ Start next feature
```
