# Two-Branch Strategy Visual Guide

ASCII diagrams to illustrate the two-branch adaptive workflow.

---

## 🌳 Branch Structure Overview

```
                     PRODUCTION (Stable)
                            ↓
    ┌──────────────────────────────────────────┐
    │                  main                    │ ← Releases, Tags
    │  v27.0    v27.1    v27.2    v27.3       │
    └────▲──────▲──────▲──────▲───────────────┘
         │      │      │      │
         │      │      │      │ PR + Review + CI
         │      │      │      │
    ┌────┴──────┴──────┴──────┴───────────────┐
    │              develop                     │ ← Active Development
    │  ○──○──○──○──○──○──○──○──○──○──○──○    │
    └──▲──▲──▲──▲──▲──▲──▲──▲──────────────────┘
       │  │  │  │  │  │  │  │
       │  │  │  │  │  │  │  └── feature/telemetry
       │  │  │  │  │  │  └───── fix/memory-leak
       │  │  │  │  │  └──────── feature/new-module
       │  │  │  │  └─────────── docs/update-readme
       │  │  │  └────────────── feature/audit-v2
       │  │  └───────────────── fix/build-error
       │  └──────────────────── feature/api-change
       └─────────────────────── refactor/cleanup

              DEVELOPMENT (Active)
```

---

## 🔄 Feature Development Flow

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Create Feature Branch                           │
└─────────────────────────────────────────────────────────┘

    develop
       │
       ├─── git checkout -b feature/my-feature
       │
       ○  feature/my-feature (new branch)

┌─────────────────────────────────────────────────────────┐
│ Step 2: Develop & Commit                                │
└─────────────────────────────────────────────────────────┘

    develop
       │
       │    feature/my-feature
       │         │
       ○─────────○────○────○────○
                 │    │    │    │
              commit1 │    │   test
                   commit2 │
                        docs

┌─────────────────────────────────────────────────────────┐
│ Step 3: Open Pull Request → develop                     │
└─────────────────────────────────────────────────────────┘

    develop
       │                PR #123
       │         ┌───────────────────┐
       ○◄────────┤ feature/my-feature│
       │         └───────────────────┘
       │              │
       │         [✓] CI Passed
       │         [✓] Tests OK
       │         [ ] Review (optional)

┌─────────────────────────────────────────────────────────┐
│ Step 4: Merge to develop                                │
└─────────────────────────────────────────────────────────┘

    develop
       │
       ○────────●  (merged feature)
       │
       │    feature/my-feature (deleted)
       │
```

---

## 🚀 Release to Production Flow

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: develop is Stable                               │
└─────────────────────────────────────────────────────────┘

    main
       │
       ○  (v27.0)
       │
       │
    develop
       │
       ○────●────●────●  (features merged)
            │    │    │
         feat1 feat2 feat3

┌─────────────────────────────────────────────────────────┐
│ Step 2: Create PR develop → main                        │
└─────────────────────────────────────────────────────────┘

    main                      PR #150 (Release v27.1)
       │              ┌────────────────────────────┐
       ○◄─────────────┤         develop            │
       │              └────────────────────────────┘
       │                       │
       │                  [✓] Build Release
       │                  [✓] All Tests
       │                  [✓] Security Scan
       │                  [✓] Documentation
       │                  [✓] Code Review ⭐
       │
    develop
       │
       ○────●────●────●

┌─────────────────────────────────────────────────────────┐
│ Step 3: Merge & Tag                                     │
└─────────────────────────────────────────────────────────┘

    main
       │
       ○────●  (v27.1) ← Tag created
       │    │
       │    └── Merged from develop
       │
       │  [Automatic sync back to develop]
       │           │
       ↓           ↓
    develop
       │
       ○────●────●────●────○  (synced with main)
```

---

## 🔥 Hotfix Flow (Emergency)

```
┌─────────────────────────────────────────────────────────┐
│ Critical Bug in Production                              │
└─────────────────────────────────────────────────────────┘

    main (v27.1)
       │
       ○  ← 🐛 Critical bug discovered!
       │
       ├─── git checkout -b hotfix/critical-fix
       │
       ○  hotfix/critical-fix
          │
          ├── Fix bug (minimal change)
          ├── Test thoroughly
          └── Create PR → main

┌─────────────────────────────────────────────────────────┐
│ Apply Hotfix to main                                    │
└─────────────────────────────────────────────────────────┘

    main (v27.1)          PR #151 (Emergency)
       │              ┌─────────────────┐
       ○◄─────────────┤ hotfix/critical │
       │              └─────────────────┘
       │                     │
       │                [!] Emergency
       │                [✓] CI Pass
       │                [✓] Review (fast)
       │
       ●  (v27.1.1) ← Hotfix merged + tagged
       │

┌─────────────────────────────────────────────────────────┐
│ Backport to develop                                     │
└─────────────────────────────────────────────────────────┘

    main
       │
       ●  (v27.1.1)
       │
       │  git cherry-pick <hotfix-commit>
       │           │
       ↓           ↓
    develop
       │
       ○────●────○  ← Hotfix applied
                │
              (continues development)
```

---

## ⚡ Parallel Development

```
Multiple developers working simultaneously:

    develop
       │
       ├────○────○  feature/telemetry (Dev A)
       │
       ├────○────○────○  feature/new-api (Dev B)
       │
       ├────○  docs/guide (Dev C)
       │
       ○────○────○  develop (base)

All merge back to develop independently:

    develop
       │
       ●  (merged telemetry)
       │
       ●  (merged new-api)
       │
       ●  (merged docs)
       │
       ○  (continues)

No conflicts if working on different areas!
```

---

## 🔒 Quality Gates Visualization

```
┌──────────────────────────────────────────────────────────┐
│                    QUALITY GATES                         │
└──────────────────────────────────────────────────────────┘

Pull Request → develop (Normal Strictness)
───────────────────────────────────────────
   │
   ├─► [✓] Build (debug)
   │
   ├─► [✓] Code Quality
   │
   ├─► [✓] Basic Tests
   │
   └─► [✓] Auto-merge if pass ───► MERGED


Pull Request → main (High Strictness)
───────────────────────────────────────────
   │
   ├─► [✓] Build (release)
   │
   ├─► [✓] Code Quality
   │
   ├─► [✓] All Tests (full suite)
   │
   ├─► [✓] Documentation Check
   │
   ├─► [✓] Security Scan
   │
   ├─► [✓] Code Review (required) ⭐
   │
   └─► [✓] Manual approval ────► MERGED
```

---

## 📊 Branch Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│              BRANCH LIFECYCLE                           │
└─────────────────────────────────────────────────────────┘

Feature Branch:
───────────────
   Create → Develop → Test → PR → Review → Merge → Delete
     ↓         ↓        ↓     ↓      ↓       ↓        ↓
    1hr      2-4 hrs  30min  5min   1hr    instant  instant
    
    Total: 4-8 hours (typical)

develop Branch:
───────────────
   [Permanent] Always exists
        │
        ├── Receives merges
        ├── Continuous integration
        ├── Active development
        └── Never deleted

main Branch:
────────────
   [Permanent] Always exists
        │
        ├── Receives releases
        ├── Tagged versions
        ├── Production-ready
        └── Never deleted
```

---

## 🔄 Sacred Cycle Integration

```
┌──────────────────────────────────────────────────────────┐
│     RAFAELIA Sacred Cycle in Two-Branch Strategy         │
└──────────────────────────────────────────────────────────┘

    VAZIO (Empty)
         ↓
    Create feature branch ─────┐
         ↓                     │
    VERBO (Action)             │ 
         ↓                     │  One cycle
    Develop + Commit           │
         ↓                     │
    CHEIO (Full)               │
         ↓                     │
    Open PR + CI               │
         ↓                     │
    RETRO (Feedback)           │
         ↓                     │
    Review + Merge ────────────┘
         ↓
    NOVO VAZIO (Informed New)
         ↓
    Delete branch, start next feature

Multiple cycles → develop → main release → New cycle
```

---

## 🎯 Decision Tree

```
┌──────────────────────────────────────────────────────────┐
│           WHERE SHOULD MY WORK GO?                       │
└──────────────────────────────────────────────────────────┘

                    Start Here
                        │
                        ↓
            ┌───────────────────────┐
            │  Is it a new feature? │
            └───────────────────────┘
                   │           │
                 Yes           No
                   │           │
                   ↓           ↓
            ┌──────────┐  ┌──────────┐
            │ develop  │  │ Is it a  │
            └──────────┘  │   bug?   │
                          └──────────┘
                               │    │
                             Yes    No
                               │    │
                               ↓    ↓
                          ┌──────────┐  ┌──────────────┐
                          │Critical? │  │Documentation?│
                          └──────────┘  └──────────────┘
                           │        │        │
                         Yes       No      Yes
                           │        │        │
                           ↓        ↓        ↓
                      ┌────────┐ ┌────────┐ ┌────────┐
                      │ main   │ │develop │ │develop │
                      │(hotfix)│ │ (fix)  │ │ (docs) │
                      └────────┘ └────────┘ └────────┘
```

---

## 📈 Workflow Efficiency

```
┌──────────────────────────────────────────────────────────┐
│              TIME TO PRODUCTION                          │
└──────────────────────────────────────────────────────────┘

Traditional Multi-Branch:
─────────────────────────
   feature → integration → staging → pre-prod → production
     ↓            ↓           ↓          ↓          ↓
   2 days      1 day       2 days     1 day     1 day
   
   Total: ~7 days 📅📅📅📅📅📅📅


Two-Branch Adaptive:
─────────────────────
   feature → develop → main
     ↓          ↓        ↓
   1 day     1 day    1 day
   
   Total: ~3 days 📅📅📅 (✓ 57% faster!)


For Hotfixes:
─────────────
   hotfix → main
     ↓        ↓
   2 hours  instant
   
   Total: ~2 hours ⚡ (✓ 98% faster!)
```

---

## 🧠 Cognitive Load Comparison

```
┌──────────────────────────────────────────────────────────┐
│            MENTAL OVERHEAD COMPARISON                    │
└──────────────────────────────────────────────────────────┘

Many Branches (Traditional):
─────────────────────────────
   Decisions to make:
   ├─ Where to branch from? (5 options)
   ├─ What naming convention? (unclear)
   ├─ Where to PR to? (4 options)
   ├─ What CI runs where? (complex)
   └─ When to delete? (manual)
   
   Cognitive Load: ████████████ (12/10 - HIGH) 🤯


Two Branches (Adaptive):
─────────────────────────
   Decisions to make:
   ├─ New work → develop ✓
   ├─ Stable release → main ✓
   └─ Emergency → hotfix → main ✓
   
   Cognitive Load: ███ (3/10 - LOW) 😌
```

---

## 🎨 Color-Coded Workflow

```
Legend:
🟢 = Safe, low risk
🟡 = Caution, review needed
🔴 = Critical, high risk

┌──────────────────────────────────────────────────────────┐
│                 RISK LEVELS                              │
└──────────────────────────────────────────────────────────┘

    🟢 develop Branch
       │
       ├─ Feature branches (🟢 low risk)
       ├─ Quick iteration
       ├─ Auto-merge OK
       └─ Experimental work

              ↓ (PR with full checks)

    🔴 main Branch
       │
       ├─ Production code (🔴 high risk)
       ├─ Manual review required
       ├─ All tests must pass
       └─ Tagged releases only

    🟡 Hotfix
       │
       ├─ Emergency fix (🟡 medium risk)
       ├─ Fast-track to main
       └─ Then backport to develop
```

---

## 📐 Scalability Model

```
┌──────────────────────────────────────────────────────────┐
│         SCALES WITH TEAM SIZE                            │
└──────────────────────────────────────────────────────────┘

Small Team (1-3 devs):
──────────────────────
         develop
            │
         ○──○──○  (simple, direct)
            ↓
          main


Medium Team (4-10 devs):
────────────────────────
         develop
         ╱  │  ╲
        ○   ○   ○  (parallel features)
         ╲  │  ╱
            ↓
          main


Large Team (10+ devs):
──────────────────────
         develop
       ╱  │  │  ╲
      ○   ○  ○   ○  (many parallel streams)
      │   │  │   │
      ●   ●  ●   ●  (sub-teams merge)
       ╲  │  │  ╱
            ↓
          main

Scales gracefully! 📈
```

---

**Visual Guide Version**: 1.0  
**Last Updated**: 2025-11-18  
**Purpose**: Help teams visualize and understand the two-branch workflow  
**Signature**: RAFCODE-Φ-∆VisualGuideΩ
