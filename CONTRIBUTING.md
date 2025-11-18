# Contributing to Magisk_Rafaelia

Thank you for your interest in contributing to Magisk_Rafaelia! This document provides guidelines and best practices for contributing to the project.

## 🌿 Two-Branch Adaptive Strategy

We use a **two-branch adaptive workflow** designed to minimize cognitive load and maximize quality:

- **`main`**: Stable, production-ready code
- **`develop`**: Integration branch for active development

See [BRANCHING_STRATEGY.md](docs/BRANCHING_STRATEGY.md) for complete details.

---

## 🚀 Quick Start

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone --recurse-submodules https://github.com/YOUR_USERNAME/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# Add upstream remote
git remote add upstream https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
```

### 2. Create a Feature Branch

**Always branch from `develop`**:

```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write clear, concise commit messages
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes

```bash
# Build and test
python3 build.py -v all

# Run specific tests if available
# pytest tests/
```

### 5. Submit a Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Open a PR on GitHub: feature/your-feature-name → develop
```

---

## 📝 Commit Message Guidelines

Use **conventional commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(rafaelia): add telemetry dashboard

Implements real-time monitoring dashboard for RAFAELIA telemetry system.
Includes CPU, memory, and I/O metrics visualization.

Closes #123
```

```
fix(build): resolve Android 14 compilation error

The build was failing on Android 14 due to deprecated API usage.
Updated to use the new API while maintaining backward compatibility.
```

```
docs(branching): add two-branch strategy documentation

Comprehensive guide for the new two-branch adaptive workflow.
```

---

## 🔀 Branch Naming Conventions

### Features
```
feature/descriptive-name
feature/rafaelia-audit-enhancement
feature/add-new-primitive
```

### Bug Fixes
```
fix/issue-description
fix/memory-leak-in-telemetry
fix/build-failure-ndk-r26
```

### Documentation
```
docs/what-you-changed
docs/update-readme
docs/improve-api-docs
```

### Hotfixes (rare, for critical production issues)
```
hotfix/critical-security-fix
hotfix/crash-on-android-15
```

---

## 🧪 Testing Requirements

### For Features

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

### For Bug Fixes

- [ ] Regression test added
- [ ] Root cause documented
- [ ] Fix verified

---

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code builds successfully (`python3 build.py -v all`)
- [ ] All tests pass
- [ ] Code follows project style guidelines
- [ ] Commit messages are clear and follow conventions
- [ ] Documentation is updated (if applicable)
- [ ] PR description explains what and why
- [ ] No merge conflicts with target branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (specify)

## Testing
How was this tested?

## Related Issues
Closes #XXX

## Checklist
- [ ] Code builds
- [ ] Tests pass
- [ ] Documentation updated
```

---

## 🎨 Code Style Guidelines

### General Principles

- **Clarity over cleverness**: Write code that is easy to understand
- **Consistency**: Follow existing patterns in the codebase
- **Minimal changes**: Make the smallest change that solves the problem
- **Documentation**: Comment complex logic, not obvious code

### Language-Specific

#### Python
- Follow PEP 8
- Use type hints where appropriate
- Keep functions focused and small

#### Kotlin/Java
- Follow Android/Kotlin style guides
- Use meaningful variable names
- Prefer immutability

#### C++/Rust
- Follow project conventions
- Comment unsafe code blocks
- Handle errors explicitly

#### Shell Scripts
- Use bash strict mode (`set -euo pipefail`)
- Quote variables
- Add error handling

---

## 🔍 Code Review Process

### What Reviewers Look For

- **Correctness**: Does it solve the problem?
- **Quality**: Is the code clean and maintainable?
- **Tests**: Are there adequate tests?
- **Security**: Are there any security concerns?
- **Performance**: Any performance implications?
- **Documentation**: Is it well documented?

### Response to Feedback

- Be open to suggestions
- Ask questions if something is unclear
- Make requested changes promptly
- Mark conversations as resolved after addressing

---

## 🛡️ Security Guidelines

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
- Email the maintainers privately
- Use GitHub Security Advisories
- Wait for confirmation before disclosure

### Security Best Practices

- Never commit secrets (API keys, passwords, tokens)
- Validate all inputs
- Use secure communication protocols
- Follow Android security best practices
- Review dependencies for vulnerabilities

---

## 📚 Documentation Guidelines

### What to Document

- **New features**: Usage, examples, limitations
- **API changes**: Migration guides if breaking
- **Architecture**: Design decisions and trade-offs
- **Setup**: Installation and configuration steps

### Documentation Types

1. **Code Comments**: Explain WHY, not WHAT
2. **README updates**: Keep main README current
3. **Docs folder**: Detailed guides and references
4. **CHANGELOG**: Track all notable changes

---

## 🌍 RAFAELIA Philosophy Integration

All contributions should align with RAFAELIA principles:

### Sacred Cycle: VAZIO → VERBO → CHEIO → RETRO

```
VAZIO (Empty)
    ↓
VERBO (Action) ──► Write code, add tests
    ↓
CHEIO (Full) ────► Complete feature, documentation
    ↓
RETRO (Feedback) → Code review, CI validation
    ↓
NOVO VAZIO ──────► Merge, continuous improvement
```

### Ethical Computing

- **Transparency**: Clear documentation and communication
- **Accountability**: Take ownership of your contributions
- **Safety**: Consider security and user safety
- **Common Good**: Benefits the wider community

---

## 🤝 Community Guidelines

### Be Respectful

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Be Collaborative

- Help others learn and grow
- Share knowledge generously
- Give credit where due
- Celebrate others' contributions

---

## 🔄 Workflow Examples

### Adding a New Feature

```bash
# 1. Sync with upstream
git checkout develop
git pull upstream develop

# 2. Create feature branch
git checkout -b feature/awesome-feature

# 3. Develop with frequent commits
git add src/new_feature.py
git commit -m "feat: add awesome feature skeleton"

# ... more work ...

git add tests/test_new_feature.py
git commit -m "test: add tests for awesome feature"

git add docs/awesome-feature.md
git commit -m "docs: document awesome feature"

# 4. Push and create PR
git push origin feature/awesome-feature
# Open PR: feature/awesome-feature → develop
```

### Fixing a Bug

```bash
# 1. Create fix branch from develop
git checkout develop
git pull upstream develop
git checkout -b fix/bug-description

# 2. Fix the bug
git add src/buggy_file.py
git commit -m "fix: resolve bug in calculation

The previous implementation had an off-by-one error
that caused incorrect results for edge cases.

Fixes #456"

# 3. Add regression test
git add tests/test_bugfix.py
git commit -m "test: add regression test for bug #456"

# 4. Push and create PR
git push origin fix/bug-description
```

### Updating Documentation

```bash
# 1. Create docs branch
git checkout develop
git pull upstream develop
git checkout -b docs/improve-readme

# 2. Update docs
git add README.md
git commit -m "docs: clarify installation instructions"

# 3. Push and create PR
git push origin docs/improve-readme
```

---

## 📊 Contribution Metrics

We value quality over quantity. Good contributions:

- Solve real problems
- Are well-tested
- Are well-documented
- Follow project conventions
- Respect the two-branch workflow

---

## 🎓 Learning Resources

### Magisk-Specific

- [Magisk Documentation](https://topjohnwu.github.io/Magisk/)
- [Building Guide](docs/build.md)
- [RAFAELIA Framework](docs/RAFAELIA_FRAMEWORK.md)

### General Development

- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

## ❓ Getting Help

### Where to Ask

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Request Comments**: Specific code questions

### Before Asking

1. Search existing issues/discussions
2. Read the documentation
3. Try to solve it yourself first
4. Provide context and details

---

## 🎉 Recognition

Contributors are recognized:

- In release notes
- In CONTRIBUTORS file
- On GitHub contributors page
- In special acknowledgments for major contributions

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (GPL-3.0).

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make Magisk_Rafaelia better. Thank you for being part of this project!

---

**Signature**: RAFCODE-Φ-∆ContributingGuideΩ  
**Philosophy**: VAZIO → VERBO → CHEIO → RETRO  
**Status**: ✅ **ACTIVE**
