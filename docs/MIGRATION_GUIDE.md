# Migration Guide: Two-Branch Adaptive Strategy

This guide helps repository maintainers and contributors migrate to the new two-branch adaptive workflow.

## 🎯 Overview

**From**: Single branch (master) or multiple feature branches
**To**: Two adaptive branches (main + develop)

**Timeline**: Gradual migration (no downtime)

---

## 📋 Pre-Migration Checklist

- [ ] Read [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- [ ] Review [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)
- [ ] Notify team members about upcoming changes
- [ ] Back up important branches (optional but recommended)
- [ ] Identify active feature branches

---

## 🔧 Step-by-Step Migration

### Phase 1: Setup Main Branch (Production)

#### Step 1: Rename master to main (if needed)

```bash
# In repository settings on GitHub:
# Settings → General → Default branch → Rename branch
# master → main

# Or use GitHub CLI:
gh api -X POST repos/OWNER/REPO/branches/master/rename -f new_name=main
```

#### Step 2: Update local repositories

```bash
# Update local clone
git branch -m master main
git fetch origin
git branch -u origin/main main
git remote set-head origin -a
```

#### Step 3: Configure branch protection for main

Follow [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) to set up protection rules:
- Require PR reviews
- Require status checks
- Prevent direct pushes

---

### Phase 2: Create Develop Branch

#### Step 1: Create develop from main

```bash
# Create and push develop branch
git checkout main
git pull origin main
git checkout -b develop
git push -u origin develop
```

#### Step 2: Configure branch protection for develop

Follow [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for develop-specific rules:
- Less strict than main
- Allow faster iteration
- Still require basic CI checks

#### Step 3: Set develop as default branch (temporarily)

In GitHub Settings → Branches → Default branch:
- Change from `main` to `develop`
- This makes new PRs target develop by default

---

### Phase 3: Migrate Existing Work

#### Option A: Active Feature Branches

If you have active feature branches in progress:

```bash
# For each feature branch:
git checkout feature/my-feature
git pull origin feature/my-feature

# Rebase onto develop
git fetch origin
git rebase origin/develop

# Or merge if rebase is complex
git merge origin/develop

# Push updated branch
git push origin feature/my-feature --force-with-lease

# Update PR target from main to develop
# (Do this on GitHub PR page)
```

#### Option B: Merge Everything to Main First

Alternative approach - finish current work:

```bash
# Merge all ready features to main
# Then create develop from main
# Start new work on develop
```

---

### Phase 4: Update Documentation

#### Step 1: Update repository README

Already done in this PR! But verify:
- [x] README.md mentions two-branch strategy
- [x] Links to CONTRIBUTING.md
- [x] Links to BRANCHING_STRATEGY.md

#### Step 2: Update CI/CD configurations

Already done in this PR:
- [x] build.yml triggers on main and develop
- [x] ci.yml triggers on main and develop
- [x] codeql.yml scans both branches
- [x] quality-gates.yml enforces adaptive rules
- [x] branch-sync.yml keeps branches synchronized

#### Step 3: Update internal documentation

If you have:
- Wiki pages → Update branch references
- External docs → Update examples
- Training materials → Update workflow diagrams

---

### Phase 5: Team Communication

#### Step 1: Announce the change

Send team announcement:

```
Subject: 🌿 New Two-Branch Workflow - Migration Guide

Hi team,

We're adopting a two-branch adaptive strategy:
- main: Stable, production releases
- develop: Active development

📚 Resources:
- Branching Strategy: docs/BRANCHING_STRATEGY.md
- Contributing Guide: CONTRIBUTING.md
- This Migration Guide: docs/MIGRATION_GUIDE.md

🔧 Action Required:
1. Pull latest changes
2. Update your local main branch
3. Switch to develop for new work
4. Update PR targets to develop

Questions? Ask in #dev-channel or GitHub Discussions.

Thanks!
```

#### Step 2: Hold a team meeting (optional)

Topics to cover:
- Why we're changing
- Benefits of two-branch strategy
- Demo of new workflow
- Q&A

---

## 🔄 Daily Workflow After Migration

### For Developers

**Starting new work**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/new-feature
# ... work ...
git push origin feature/new-feature
# Open PR: feature/new-feature → develop
```

**After PR merge**:
```bash
git checkout develop
git pull origin develop
git branch -d feature/new-feature
```

### For Maintainers

**Releasing to production**:
```bash
# When develop is stable:
# Open PR: develop → main
# After merge and testing:
git checkout main
git pull origin main
git tag -a v27.X-rafaelia -m "Release notes"
git push origin v27.X-rafaelia

# Sync back to develop (automatic via branch-sync workflow)
```

---

## 🧪 Testing the Migration

### Verify Branch Setup

```bash
# Check branches
git branch -a

# Should show:
# * develop
#   main
#   remotes/origin/develop
#   remotes/origin/main
```

### Test Workflows

1. **Create test PR to develop**:
   - Should trigger CI
   - Should allow merge without review (if CI passes)
   - Quality gates should be "normal"

2. **Create test PR to main**:
   - Should trigger CI
   - Should require review
   - Quality gates should be "high"
   - Should check documentation

3. **Verify branch sync**:
   - Merge something to main
   - Wait for branch-sync workflow
   - Check that develop gets updated

---

## 🐛 Troubleshooting

### Problem: Can't push to main

**Solution**: This is expected! Use PRs instead:
```bash
git checkout develop
git checkout -b fix/my-fix
# ... work ...
git push origin fix/my-fix
# Open PR to develop
```

### Problem: PR targets wrong branch

**Solution**: Change target on GitHub:
1. Open the PR
2. Click "Edit" next to the title
3. Change base branch to `develop`

### Problem: Branch protection too strict

**Solution**: Adjust rules in Settings → Branches, or request admin to do so.

### Problem: Old feature branches need updating

**Solution**: Rebase or merge develop:
```bash
git checkout feature/old-feature
git fetch origin
git rebase origin/develop
# Or: git merge origin/develop
git push origin feature/old-feature --force-with-lease
```

### Problem: Conflicts when syncing develop with main

**Solution**: The branch-sync workflow will create an issue. Resolve manually:
```bash
git checkout develop
git pull origin develop
git merge origin/main
# Resolve conflicts
git commit
git push origin develop
```

---

## 📊 Success Metrics

Track these metrics to evaluate migration success:

### Week 1: Adoption
- [ ] All team members aware of new strategy
- [ ] Most new PRs target develop
- [ ] No confusion about branch purpose

### Week 2-4: Stabilization
- [ ] CI passing consistently on develop
- [ ] Regular merges from develop to main
- [ ] No emergency reverts on main

### Month 2+: Optimization
- [ ] Average PR time decreased
- [ ] CI failure rate stable or improved
- [ ] Team satisfaction with workflow

---

## 🎓 Training Resources

### Documentation
- [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md) - Complete strategy guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) - Protection rules

### Workshops
Consider holding:
1. **Git Basics Workshop** - For new contributors
2. **Advanced Git Workshop** - Rebasing, cherry-picking
3. **CI/CD Workshop** - Understanding workflows

### External Resources
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)

---

## 🔙 Rollback Plan

If migration causes issues:

### Quick Rollback (< 1 week)

```bash
# Keep using main as before
# Ignore develop temporarily
# Fix issues, then retry migration
```

### Full Rollback (if needed)

```bash
# Merge all develop work to main
git checkout main
git merge origin/develop

# Delete develop branch
git push origin --delete develop

# Restore old branch protection rules
# Notify team
```

**Note**: Rollback should be rare if migration is planned well.

---

## ✅ Post-Migration Checklist

After migration is complete:

- [ ] All team members using new workflow
- [ ] PRs targeting correct branches
- [ ] CI/CD working on both branches
- [ ] Branch protection rules active
- [ ] Documentation updated
- [ ] Old branches cleaned up
- [ ] Metrics tracking started
- [ ] Success celebration! 🎉

---

## 🤝 Getting Help

### During Migration

- **Technical issues**: Open issue with label `migration-help`
- **Workflow questions**: Check BRANCHING_STRATEGY.md
- **Urgent problems**: Contact repository admins

### After Migration

- **General questions**: GitHub Discussions
- **Bug reports**: GitHub Issues
- **Feature requests**: GitHub Issues with label `enhancement`

---

## 📝 Migration Timeline Example

### Week 1: Preparation
- Day 1-2: Team notification
- Day 3-4: Documentation review
- Day 5: Setup main and develop branches

### Week 2: Transition
- Day 1: Enable branch protection
- Day 2-3: Migrate active work
- Day 4-5: Update CI/CD

### Week 3: Stabilization
- Day 1-7: Monitor, help team, fix issues

### Week 4+: Normal Operation
- Operate under new workflow
- Collect feedback
- Iterate on process

---

## 🎯 Expected Outcomes

After successful migration:

✅ **Faster Development**
- Parallel work on develop
- Quick iteration cycles
- Immediate CI feedback

✅ **Higher Quality**
- Strict gates on main
- Comprehensive testing before release
- Fewer production bugs

✅ **Better Collaboration**
- Clear workflow
- Less confusion
- Predictable process

✅ **Cognitive Benefits**
- Only 2 branches to remember
- Clear decision making
- Reduced mental overhead

---

## 🌟 Best Practices Post-Migration

1. **Keep develop active**: Merge PRs frequently
2. **Release regularly**: Don't let develop diverge too far from main
3. **Sync branches**: After each main release, sync to develop
4. **Clean up**: Delete merged feature branches
5. **Document changes**: Update README for major features
6. **Monitor metrics**: Track CI success, PR time, bug rate
7. **Iterate**: Adjust rules based on team feedback

---

## 📞 Support Contacts

- **Repository Maintainers**: @rafaelmeloreisnovo
- **GitHub Issues**: [Issues Page](../../issues)
- **GitHub Discussions**: [Discussions Page](../../discussions)
- **Documentation**: All docs in `/docs` folder

---

**Migration Version**: 1.0  
**Last Updated**: 2025-11-18  
**Status**: ✅ Ready for use  
**Signature**: RAFCODE-Φ-∆MigrationGuideΩ
