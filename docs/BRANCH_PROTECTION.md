# Branch Protection Configuration Guide

This document provides the recommended branch protection rules for the two-branch adaptive strategy.

## 🔒 Protection Rules

### For `main` Branch

**Purpose**: Protect stable, production-ready code with strict quality gates.

#### Required Status Checks

```yaml
Require branches to be up to date before merging: ✅ Enabled
Status checks that are required:
  - build-release (from build.yml)
  - quality-gates / Code Quality Check
  - quality-gates / Documentation Check
  - quality-gates / Build Validation
  - quality-gates / Security Check
```

#### Pull Request Reviews

```yaml
Require pull request reviews before merging: ✅ Enabled
Required approving reviews: 1
Dismiss stale pull request approvals when new commits are pushed: ✅ Enabled
Require review from Code Owners: ❌ Disabled (optional)
```

#### Additional Restrictions

```yaml
Require conversation resolution before merging: ✅ Enabled
Require signed commits: ❌ Disabled (optional, but recommended)
Require linear history: ❌ Disabled (allows merge commits)
Allow force pushes: ❌ Disabled
Allow deletions: ❌ Disabled
```

#### Enforcement

```yaml
Do not allow bypassing the above settings: ❌ Disabled
  (Allows admins to bypass for emergency hotfixes)
```

---

### For `develop` Branch

**Purpose**: Enable rapid iteration while maintaining basic quality standards.

#### Required Status Checks

```yaml
Require branches to be up to date before merging: ❌ Disabled
  (More flexible for parallel development)
Status checks that are required:
  - build-debug (from build.yml)
  - quality-gates / Code Quality Check
  - quality-gates / Build Validation
```

#### Pull Request Reviews

```yaml
Require pull request reviews before merging: ❌ Disabled
  (Allows self-merge if CI passes)
Required approving reviews: 0
```

#### Additional Restrictions

```yaml
Require conversation resolution before merging: ❌ Disabled
Require signed commits: ❌ Disabled
Require linear history: ❌ Disabled
Allow force pushes: ❌ Disabled
Allow deletions: ❌ Disabled
```

#### Enforcement

```yaml
Do not allow bypassing the above settings: ❌ Disabled
```

---

## 🛠️ How to Configure (GitHub UI)

### Step 1: Access Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** (top navigation)
3. Click **Branches** (left sidebar)

### Step 2: Add Branch Protection Rule for `main`

1. Click **Add rule** or **Add branch protection rule**
2. In **Branch name pattern**, enter: `main`
3. Configure according to the settings above for `main`
4. Click **Create** (or **Save changes**)

### Step 3: Add Branch Protection Rule for `develop`

1. Click **Add rule** again
2. In **Branch name pattern**, enter: `develop`
3. Configure according to the settings above for `develop`
4. Click **Create**

---

## 📝 Configuration as Code (GitHub API)

You can also configure these rules using the GitHub API or Terraform.

### Using GitHub API

```bash
# Configure main branch protection
curl -X PUT \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": [
        "build-release",
        "quality-gates / Code Quality Check",
        "quality-gates / Documentation Check",
        "quality-gates / Build Validation",
        "quality-gates / Security Check"
      ]
    },
    "required_pull_request_reviews": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true
    },
    "enforce_admins": false,
    "restrictions": null,
    "required_linear_history": false,
    "allow_force_pushes": false,
    "allow_deletions": false
  }'

# Configure develop branch protection
curl -X PUT \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/branches/develop/protection \
  -d '{
    "required_status_checks": {
      "strict": false,
      "contexts": [
        "build-debug",
        "quality-gates / Code Quality Check",
        "quality-gates / Build Validation"
      ]
    },
    "required_pull_request_reviews": null,
    "enforce_admins": false,
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false
  }'
```

### Using Terraform

```hcl
# main.tf
resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.node_id
  pattern       = "main"

  required_status_checks {
    strict   = true
    contexts = [
      "build-release",
      "quality-gates / Code Quality Check",
      "quality-gates / Documentation Check",
      "quality-gates / Build Validation",
      "quality-gates / Security Check"
    ]
  }

  required_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews           = true
  }

  enforce_admins         = false
  require_signed_commits = false
  allow_force_pushes     = false
  allow_deletions        = false
}

resource "github_branch_protection" "develop" {
  repository_id = github_repository.repo.node_id
  pattern       = "develop"

  required_status_checks {
    strict   = false
    contexts = [
      "build-debug",
      "quality-gates / Code Quality Check",
      "quality-gates / Build Validation"
    ]
  }

  enforce_admins     = false
  allow_force_pushes = false
  allow_deletions    = false
}
```

---

## 🔄 Updating Protection Rules

### When to Update

- **After adding new required workflows**: Add them to status checks
- **After team growth**: Adjust review requirements
- **After security incidents**: Tighten restrictions
- **Based on metrics**: If quality drops, add more gates

### Best Practices

1. **Start permissive, then tighten**: Begin with minimal restrictions and add more as needed
2. **Document changes**: Update this file when you change rules
3. **Communicate with team**: Announce rule changes in advance
4. **Monitor impact**: Track metrics before and after changes
5. **Be consistent**: Apply similar rules across similar projects

---

## 📊 Monitoring Compliance

### Key Metrics to Track

- **PR merge time**: Average time from PR open to merge
- **CI failure rate**: Percentage of failed CI runs
- **Manual override frequency**: How often admins bypass rules
- **Review participation**: Number of reviewers per PR
- **Hotfix frequency**: Number of emergency bypasses

### Tools

- **GitHub Insights**: Built-in repository insights
- **GitHub API**: Query protection rule violations
- **Custom dashboards**: Build using GitHub API data

---

## 🚨 Emergency Procedures

### Critical Hotfix Process

When a critical bug needs immediate fix on `main`:

1. **Create hotfix branch from main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-issue
   ```

2. **Make minimal fix**: Only fix the critical issue, nothing else

3. **Test thoroughly**: Even in emergency, test the fix

4. **Create PR to main**: Follow normal PR process if possible

5. **Admin override if necessary**: If truly urgent and CI will take too long

6. **Backport to develop**:
   ```bash
   git checkout develop
   git cherry-pick <hotfix-commit>
   git push origin develop
   ```

7. **Post-mortem**: Document what happened and how to prevent it

---

## ✅ Verification

After setting up branch protection:

### Test `main` Protection

1. Try to push directly to main (should fail):
   ```bash
   git checkout main
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test direct push"
   git push origin main  # Should be rejected
   ```

2. Create a PR and verify:
   - Required status checks are enforced
   - Review is required
   - Can't merge without passing CI

### Test `develop` Protection

1. Try to push directly to develop (should fail):
   ```bash
   git checkout develop
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test direct push"
   git push origin develop  # Should be rejected
   ```

2. Create a PR and verify:
   - Can merge without review (if CI passes)
   - Basic status checks are enforced

---

## 📚 References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Last Updated**: 2025-11-18  
**Version**: 1.0  
**Signature**: RAFCODE-Φ-∆BranchProtectionΩ
