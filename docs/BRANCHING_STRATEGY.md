# Estratégia de Dois Branch Adaptativos / Two-Branch Adaptive Strategy

## 🌿 Visão Geral / Overview

**Português**: Esta é a estratégia oficial de branching do Magisk_Rafaelia, implementando um modelo evolutivo de dois branches adaptativos baseado em boas práticas cognitivas.

**English**: This is the official branching strategy for Magisk_Rafaelia, implementing an evolutionary two-branch adaptive model based on cognitive best practices.

---

## 🎯 Filosofia / Philosophy

### Princípios Evolutivos / Evolutionary Principles

```
VAZIO (Empty)
    ↓
VERBO (Action) ──► Development → Testing → Validation
    ↓
CHEIO (Full) ────► Integration → Quality Gates
    ↓
RETRO (Feedback) → Stable Release
    ↓
NOVO VAZIO ──────► Continuous Improvement
```

### Carga Cognitiva Mínima / Minimal Cognitive Load

- **Apenas 2 branches principais** = Simplicidade e clareza
- **Only 2 main branches** = Simplicity and clarity
- **Fluxo previsível** = Redução de erros
- **Predictable flow** = Error reduction

---

## 🌳 Estrutura de Branches / Branch Structure

### 1️⃣ `main` (Produção/Production)

**Propósito / Purpose**: 
- Código estável e pronto para produção
- Stable, production-ready code

**Características / Characteristics**:
- ✅ Todas as verificações passam / All checks pass
- ✅ Build release bem-sucedido / Successful release build
- ✅ Testes completos / Complete tests
- ✅ Documentação atualizada / Updated documentation
- ✅ Security scans passed
- ✅ Code review approved

**Proteções / Protections**:
- ⛔ Push direto proibido / Direct push forbidden
- ✓ Requer pull request / Requires pull request
- ✓ Requer aprovação / Requires approval
- ✓ Requer CI passar / Requires CI to pass
- ✓ Branch atualizado / Up-to-date branch required

**Tags**: Todas as releases são tagueadas aqui / All releases are tagged here
- `v27.0-rafaelia`
- `v27.1-rafaelia`
- etc.

---

### 2️⃣ `develop` (Desenvolvimento/Development)

**Propósito / Purpose**:
- Integração contínua de features
- Continuous feature integration

**Características / Characteristics**:
- 🔄 Integração contínua / Continuous integration
- 🧪 Testes automatizados / Automated testing
- 📊 Análise de qualidade / Quality analysis
- 🔍 Review de código / Code review
- ⚡ Iteração rápida / Fast iteration

**Proteções / Protections**:
- ✓ CI deve passar / CI must pass
- ✓ Build deve ter sucesso / Build must succeed
- ✓ Sem conflitos / No conflicts

**Merge para main**: Quando estável e testado / When stable and tested

---

## 🔄 Fluxo de Trabalho / Workflow

### Desenvolvimento de Features / Feature Development

```
develop
   │
   ├─► feature/nova-funcionalidade
   │        │
   │        ├─ Commits...
   │        ├─ Testes...
   │        └─ CI passa
   │            │
   │            ↓
   └─◄──── Pull Request → develop
             (Review + Merge)
```

### Release para Produção / Release to Production

```
develop (estável/stable)
   │
   │  [Release Preparation]
   │  - Todos testes passam / All tests pass
   │  - Documentação OK / Documentation OK
   │  - Security OK
   │  - Performance OK
   │
   ↓
Pull Request → main
   │
   ├─ Review rigoroso / Rigorous review
   ├─ Aprovação necessária / Approval required
   ├─ CI completo / Complete CI
   │
   ↓
Merge + Tag → v27.X-rafaelia
```

### Hotfix Crítico / Critical Hotfix

```
main
   │
   ├─► hotfix/problema-urgente
   │        │
   │        ├─ Fix mínimo / Minimal fix
   │        ├─ Testes focados / Focused tests
   │        └─ CI rápido / Fast CI
   │            │
   ├─◄──────────┘
   │   (Merge direto para main)
   │   (Direct merge to main)
   │
   └─► Cherry-pick para develop
       (Sincronizar branches)
       (Synchronize branches)
```

---

## 📋 Convenções / Conventions

### Nomes de Branches / Branch Names

**Features**:
```
feature/nome-descritivo
feature/rafaelia-telemetry-enhancement
feature/add-new-module
```

**Fixes**:
```
fix/corrigir-problema
fix/memory-leak-in-audit
fix/build-error-android-14
```

**Hotfixes**:
```
hotfix/seguranca-critica
hotfix/crash-on-startup
```

**Documentação / Documentation**:
```
docs/atualizar-guia
docs/branching-strategy
docs/improve-readme
```

---

## 🤖 Automação / Automation

### CI/CD nos Branches / CI/CD on Branches

#### `develop` Branch

**Triggers**:
- Push para develop
- Pull request para develop

**Actions**:
- ✅ Build debug + release
- ✅ Testes unitários / Unit tests
- ✅ Testes de integração / Integration tests
- ✅ Linting e formatação / Linting and formatting
- ✅ Security scans (CodeQL)
- ✅ Geração de artefatos / Artifact generation

**Frequência**: A cada commit / Every commit

#### `main` Branch

**Triggers**:
- Pull request para main
- Merge para main
- Tags de release

**Actions**:
- ✅ Build completo / Complete build
- ✅ Testes completos / Complete tests
- ✅ Security audit completo / Complete security audit
- ✅ Geração de release APK / Release APK generation
- ✅ Criação de GitHub Release
- ✅ Atualização de documentação / Documentation update
- ✅ Notificações / Notifications

**Frequência**: Em releases / On releases

---

## 🔐 Proteções de Branch / Branch Protections

### Configuração Recomendada / Recommended Configuration

#### Branch `main`:

```yaml
protection_rules:
  required_status_checks:
    strict: true
    contexts:
      - "build-release"
      - "test-suite"
      - "security-scan"
      - "code-review"
  
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: false
  
  enforce_admins: false  # Admins podem fazer hotfix emergencial
  
  restrictions: null  # Qualquer colaborador pode criar PR
  
  required_linear_history: false  # Permite merge commits
  
  allow_force_pushes: false
  allow_deletions: false
```

#### Branch `develop`:

```yaml
protection_rules:
  required_status_checks:
    strict: false  # Mais flexível para desenvolvimento
    contexts:
      - "build-debug"
      - "basic-tests"
  
  required_pull_request_reviews:
    required_approving_review_count: 0  # Auto-merge OK se CI passa
    dismiss_stale_reviews: false
  
  enforce_admins: false
  
  allow_force_pushes: false  # Ainda protegido
  allow_deletions: false
```

---

## 🧠 Práticas Cognitivas / Cognitive Practices

### 1. Redução de Complexidade / Complexity Reduction

**Antes / Before**: Múltiplos branches com nomes inconsistentes
**Depois / After**: 2 branches principais + branches temporários

**Benefício / Benefit**: 
- Menos decisões mentais / Fewer mental decisions
- Fluxo claro / Clear flow
- Onboarding rápido / Fast onboarding

### 2. Feedback Loop Imediato / Immediate Feedback Loop

```
Commit → CI (< 5 min) → Feedback
   ↓
Correção rápida / Quick fix
   ↓
Re-test automático / Automatic re-test
```

### 3. Previsibilidade / Predictability

Todo desenvolvedor sabe:
Every developer knows:
- Onde seu código vai / Where their code goes
- Quando vai para produção / When it goes to production
- Como fazer review / How to do review
- O que CI vai validar / What CI will validate

### 4. Carga Cognitiva Progressiva / Progressive Cognitive Load

**Nível 1 (Simples)**: 
- Criar branch feature
- Fazer commits
- Abrir PR para develop

**Nível 2 (Intermediário)**:
- Review de código
- Resolver conflitos
- Validar CI

**Nível 3 (Avançado)**:
- Preparar release
- Merge para main
- Criar tags

---

## 📊 Métricas Evolutivas / Evolutionary Metrics

### Indicadores de Saúde / Health Indicators

**Velocidade / Velocity**:
- ⏱️ Tempo médio feature → develop: < 3 dias
- ⏱️ Tempo médio develop → main: < 7 dias
- ⏱️ Tempo de build CI: < 15 minutos

**Qualidade / Quality**:
- ✅ Taxa de sucesso CI: > 95%
- 🐛 Bugs em produção: < 5 por release
- 🔄 Taxa de rollback: < 2%

**Adaptabilidade / Adaptability**:
- 🔧 Hotfixes por mês: < 3
- 📈 Melhoria contínua: feedback loops ativos
- 🧪 Cobertura de testes: > 70%

---

## 🚀 Guia Rápido / Quick Guide

### Para Desenvolvedores / For Developers

```bash
# 1. Clonar repositório / Clone repository
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# 2. Criar branch feature a partir de develop
git checkout develop
git pull origin develop
git checkout -b feature/minha-feature

# 3. Desenvolver e commitar
git add .
git commit -m "feat: adicionar funcionalidade X"

# 4. Push e criar PR
git push -u origin feature/minha-feature
# Abrir PR no GitHub: feature/minha-feature → develop

# 5. Após merge, deletar branch local
git checkout develop
git pull origin develop
git branch -d feature/minha-feature
```

### Para Mantenedores / For Maintainers

```bash
# 1. Release de develop para main
git checkout develop
git pull origin develop

# Verificar que tudo está OK
python3 build.py -vr all  # Build completo

# 2. Criar PR develop → main no GitHub

# 3. Após merge, criar tag
git checkout main
git pull origin main
git tag -a v27.1-rafaelia -m "Release 27.1 - RAFAELIA enhancements"
git push origin v27.1-rafaelia
```

---

## 🌐 Sincronização / Synchronization

### Keep develop atualizado / Keep develop updated

```bash
# Sincronizar develop com main periodicamente
git checkout develop
git pull origin develop
git merge origin/main
git push origin develop
```

**Frequência recomendada / Recommended frequency**: 
- Após cada release em main
- Antes de começar nova feature grande

---

## 📚 Referências / References

### Metodologias Aplicadas / Applied Methodologies

1. **Git Flow Simplificado**: 2 branches ao invés de 5
2. **GitHub Flow**: Integração contínua
3. **Trunk-Based Development**: Branches de curta duração
4. **Cognitive Load Theory**: Redução de complexidade
5. **Evolutionary Architecture**: Adaptação contínua

### RAFAELIA Integration

Esta estratégia implementa os princípios RAFAELIA:
This strategy implements RAFAELIA principles:

- **VAZIO**: Branch limpo, pronto para feature
- **VERBO**: Desenvolvimento ativo
- **CHEIO**: Feature completa, testada
- **RETRO**: Review, feedback, melhorias
- **NOVO VAZIO**: Merge, branch deletado, ciclo reinicia

---

## 🔄 Evolução da Estratégia / Strategy Evolution

### Versão Atual / Current Version: 1.0

**Data / Date**: 2025-11-18

**Próximas Melhorias / Next Improvements**:
- [ ] Automatizar criação de branches
- [ ] Dashboard de métricas
- [ ] Integração com Jira/Issues
- [ ] Notification system para releases
- [ ] Bot de merge automático (quando CI passa)

**Feedback**: Contribuições bem-vindas em `/docs/BRANCHING_STRATEGY.md`

---

## 📞 Suporte / Support

**Dúvidas / Questions**:
- GitHub Issues: Tag com `branching-strategy`
- Discussões: GitHub Discussions

**Documentação Relacionada / Related Documentation**:
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [RAFAELIA_FRAMEWORK.md](RAFAELIA_FRAMEWORK.md)
- [BUILD Guide](build.md)

---

**Assinatura / Signature**: RAFCODE-Φ-∆BranchStrategyΩ  
**Filosofia / Philosophy**: VAZIO → VERBO → CHEIO → RETRO  
**Status**: ✅ **ATIVO / ACTIVE**
