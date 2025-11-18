# Workflow Organization Guide / Guia de Organização de Workflows

## 🎯 Objetivo / Purpose

**Português**: Este documento organiza e consolida os workflows do GitHub Actions, mantendo apenas os essenciais e arquivando redundantes.

**English**: This document organizes and consolidates GitHub Actions workflows, keeping only essential ones and archiving redundant ones.

---

## 📊 Análise de Workflows / Workflow Analysis

### Total de Workflows: 30 arquivos

#### ✅ Essenciais (Manter) / Essential (Keep)

Workflows críticos para o projeto:

**1. build.yml**
- **Propósito**: Build principal do Magisk
- **Triggers**: Push/PR em main e develop
- **Status**: ✅ Configurado para dois branches
- **Ação**: Manter

**2. codeql.yml**
- **Propósito**: Análise de segurança (CodeQL)
- **Triggers**: Push/PR em main e develop, schedule semanal
- **Status**: ✅ Configurado para dois branches
- **Ação**: Manter

**3. branch-sync.yml**
- **Propósito**: Sincronização main → develop após releases
- **Triggers**: Push em main, workflow_dispatch
- **Status**: ✅ Alinhado com estratégia de dois branches
- **Ação**: Manter

**4. ci.yml**
- **Propósito**: Integração contínua
- **Triggers**: Push/PR
- **Status**: Verificar se não duplica build.yml
- **Ação**: Revisar e consolidar com build.yml se duplicado

**5. quality-gates.yml**
- **Propósito**: Gates de qualidade (code quality, docs, security)
- **Triggers**: Push/PR
- **Status**: Essencial para branch protection
- **Ação**: Manter

**6. ethicalcheck.yml**
- **Propósito**: Verificações éticas do projeto
- **Triggers**: Push/PR
- **Status**: Alinhado com módulos de licença
- **Ação**: Manter e atualizar para validar novos módulos

#### ⚠️ Específicos de Plataforma (Avaliar) / Platform-Specific (Evaluate)

**7. android.yml**
- **Propósito**: Build Android específico
- **Status**: Pode duplicar build.yml
- **Ação**: Consolidar com build.yml ou arquivar

**8. c-cpp.yml**
- **Propósito**: Build C/C++
- **Status**: Pode ser redundante com build.yml
- **Ação**: Verificar se necessário separado

**9. cmake-multi-platform.yml**
- **Propósito**: Build CMake multi-plataforma
- **Status**: Pode ser redundante
- **Ação**: Verificar uso real

**10. rust.yml**
- **Propósito**: Build Rust
- **Status**: Se RAFAELIA usa Rust, manter
- **Ação**: Manter se código Rust ativo

#### ❌ Cloud Deploy (Não Aplicável) / Cloud Deploy (Not Applicable)

Workflows para deployment em clouds que não são usados:

**11-18. Cloud Workflows (Arquivar)**:
- alibabacloud.yml
- aws.yml
- azure-functions-app-java.yml
- azure-functions-app-python.yml
- azure-webapps-java-jar.yml
- azure-webapps-python.yml
- google.yml
- gatsby.yml
- nextjs.yml

**Ação**: Mover para `.old/` ou deletar

#### ❓ Outros (Avaliar) / Others (Evaluate)

**19. apisec-scan.yml**
- **Propósito**: Scan de segurança de API
- **Status**: Útil se API exposta
- **Ação**: Manter se relevante, arquivar se não

**20. ci-symbols.yml**
- **Propósito**: Symbols para debugging
- **Status**: Útil para desenvolvimento
- **Ação**: Manter

**21. force-merge.yml**
- **Propósito**: Merge forçado (???)
- **Status**: ⚠️ PERIGOSO - viola proteções de branch
- **Ação**: DELETAR imediatamente

**22. greetings.yml**
- **Propósito**: Mensagens de boas-vindas
- **Status**: Nice to have
- **Ação**: Manter (baixo custo)

**23. label.yml**
- **Propósito**: Auto-labeling de issues/PRs
- **Status**: Útil para organização
- **Ação**: Manter

**24. main.yml**
- **Propósito**: Workflow principal (???)
- **Status**: Verificar conteúdo
- **Ação**: Consolidar com build.yml se duplicado

**25. makefile.yml**
- **Propósito**: Build via Makefile
- **Status**: Pode ser redundante
- **Ação**: Verificar se usado

**26. neuralegion.yml**
- **Propósito**: Security scanning (NeuralEgion)
- **Status**: Duplica CodeQL?
- **Ação**: Avaliar necessidade

**27. python-package-conda.yml**
- **Propósito**: Build Python package
- **Status**: Se build.py é script principal, pode ser redundante
- **Ação**: Avaliar necessidade

**28. stale.yml**
- **Propósito**: Marca issues/PRs inativos
- **Status**: Útil para manutenção
- **Ação**: Manter

**29. summary.yml**
- **Propósito**: Sumário de workflow
- **Status**: Nice to have
- **Ação**: Manter se útil

---

## 🎯 Recomendações de Consolidação / Consolidation Recommendations

### Ação Imediata / Immediate Action

#### 1. Deletar Workflows Perigosos
```bash
# CRÍTICO: Remover force-merge.yml
git rm .github/workflows/force-merge.yml
```

#### 2. Arquivar Workflows de Cloud Deploy
```bash
# Criar diretório de arquivo
mkdir -p .github/workflows/.archived

# Mover workflows não utilizados
git mv .github/workflows/alibabacloud.yml .github/workflows/.archived/
git mv .github/workflows/aws.yml .github/workflows/.archived/
git mv .github/workflows/azure-functions-app-java.yml .github/workflows/.archived/
git mv .github/workflows/azure-functions-app-python.yml .github/workflows/.archived/
git mv .github/workflows/azure-webapps-java-jar.yml .github/workflows/.archived/
git mv .github/workflows/azure-webapps-python.yml .github/workflows/.archived/
git mv .github/workflows/google.yml .github/workflows/.archived/
git mv .github/workflows/gatsby.yml .github/workflows/.archived/
git mv .github/workflows/nextjs.yml .github/workflows/.archived/
```

#### 3. Adicionar .gitignore para .archived
```bash
echo "# Archived workflows (kept for reference)" > .github/workflows/.archived/.gitignore
```

### Ação de Revisão / Review Action

#### Consolidar Builds Duplicados

Se `android.yml`, `c-cpp.yml`, `cmake-multi-platform.yml` duplicam `build.yml`:

```yaml
# Consolidar tudo em build.yml com jobs separados:

jobs:
  build-android:
    # ... Android build ...
  
  build-native:
    # ... C/C++ build ...
  
  build-cmake:
    # ... CMake build ...
```

#### Atualizar ethicalcheck.yml

Adicionar validação dos novos módulos de licença:

```yaml
# .github/workflows/ethicalcheck.yml
steps:
  - name: Validate license modules
    run: |
      # Check all 5 modules exist
      for i in 01 02 03 04 05; do
        if [ ! -f "docs/license-modules/${i}-*.md" ]; then
          echo "Missing license module ${i}"
          exit 1
        fi
      done
      
      # Check LICENSE references modules
      if ! grep -q "MODULE 1: SEMANTIC-LEGAL" LICENSE; then
        echo "LICENSE doesn't reference modules"
        exit 1
      fi
```

---

## 📋 Checklist de Consolidação / Consolidation Checklist

### Fase 1: Segurança / Phase 1: Security
- [ ] Deletar force-merge.yml (CRÍTICO)
- [ ] Verificar permissões de workflows
- [ ] Confirmar proteções de branch ativas

### Fase 2: Limpeza / Phase 2: Cleanup
- [ ] Arquivar workflows de cloud deploy (9 arquivos)
- [ ] Adicionar .gitignore em .archived/
- [ ] Documentar motivo do arquivamento

### Fase 3: Consolidação / Phase 3: Consolidation
- [ ] Revisar ci.yml vs build.yml
- [ ] Revisar android.yml vs build.yml
- [ ] Consolidar builds redundantes
- [ ] Atualizar documentação de workflows

### Fase 4: Atualização / Phase 4: Update
- [ ] Atualizar ethicalcheck.yml para novos módulos
- [ ] Verificar todos workflows usam main + develop
- [ ] Testar workflows essenciais
- [ ] Documentar workflows ativos

---

## 🔧 Workflows Essenciais Finais / Final Essential Workflows

Após consolidação, manter apenas:

```
.github/workflows/
├── build.yml              # ✅ Build principal (consolidado)
├── codeql.yml             # ✅ Análise de segurança
├── branch-sync.yml        # ✅ Sincronização de branches
├── quality-gates.yml      # ✅ Gates de qualidade
├── ethicalcheck.yml       # ✅ Verificações éticas
├── ci-symbols.yml         # ✅ Debug symbols
├── rust.yml               # ✅ Se RAFAELIA usar Rust
├── greetings.yml          # ✅ Boas-vindas (nice to have)
├── label.yml              # ✅ Auto-labeling
├── stale.yml              # ✅ Manutenção de issues
└── .archived/             # 📦 Workflows arquivados
    ├── alibabacloud.yml
    ├── aws.yml
    ├── azure-*.yml
    ├── google.yml
    └── ... (outros não usados)
```

**Total recomendado**: ~10 workflows ativos (de 30)

---

## 📝 Atualizações Necessárias / Required Updates

### Todos os Workflows Ativos

Verificar que todos têm:

```yaml
on:
  push:
    branches: [main, develop]  # Two-branch strategy
  pull_request:
    branches: [main, develop]
```

### ethicalcheck.yml

Adicionar validação de módulos de licença:

```yaml
- name: Check license modules
  run: |
    # Validate all 5 modules exist and are properly formatted
    python3 scripts/validate_license_modules.py
```

### quality-gates.yml

Adicionar validação de documentação:

```yaml
- name: Documentation completeness
  run: |
    # Check that all new modules are referenced in main docs
    ./scripts/check_doc_references.sh
```

---

## 🔄 Processo de Manutenção / Maintenance Process

### Mensal / Monthly

- [ ] Revisar workflows executados
- [ ] Identificar workflows sem uso
- [ ] Atualizar dependências de actions
- [ ] Verificar tempos de execução

### Trimestral / Quarterly

- [ ] Avaliar necessidade de novos workflows
- [ ] Consolidar workflows similares
- [ ] Atualizar documentação
- [ ] Treinar equipe sobre mudanças

### Anual / Yearly

- [ ] Auditoria completa de workflows
- [ ] Benchmark de performance
- [ ] Revisar melhores práticas
- [ ] Planejar melhorias

---

## 📚 Referências / References

### Documentação
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices-for-workflows)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

### Projeto
- [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [CI/CD Documentation](../docs/ci-cd.md) (criar se não existir)

---

## ✅ Critérios para Workflow Essencial / Essential Workflow Criteria

Um workflow é considerado essencial se:

1. **Bloqueia merges**: Requerido para branch protection
2. **Segurança crítica**: CodeQL, security scans
3. **Build/Test**: Valida código funcional
4. **Automação de processo**: Branch sync, release
5. **Qualidade**: Code quality, docs validation

Um workflow pode ser arquivado se:

1. **Não executado**: Sem runs nos últimos 6 meses
2. **Duplicado**: Funcionalidade coberta por outro
3. **Não aplicável**: Cloud deploy não usado
4. **Experimental**: POC que não foi adotado

---

**Signature**: RAFCODE-Φ-∆WorkflowOrgΩ  
**Philosophy**: Simplicidade + Eficiência + Qualidade  
**Status**: ✅ **ACTIVE**  
**Version**: 1.0  
**Last Updated**: 2025-11-18
