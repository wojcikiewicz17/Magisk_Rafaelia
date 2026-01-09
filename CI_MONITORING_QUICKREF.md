# Cartão de Referência Rápida: Monitoramento CI/CD ARM64

## 🔍 Ver Status dos Checks

### No Navegador
```
https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

### Via Linha de Comando (GitHub CLI)
```bash
# Instalar gh (uma vez)
# Linux: sudo apt install gh
# macOS: brew install gh

# Autenticar
gh auth login

# Ver últimas execuções
gh run list --limit 10

# Ver detalhes de uma execução
gh run view <run-id>

# Ver logs
gh run view <run-id> --log

# Baixar artefatos
gh run download <run-id>
```

---

## 📊 Workflows Principais

| Workflow | O Que Faz | Quando Roda |
|----------|-----------|-------------|
| **build.yml** | Compilação completa (macOS + Linux + Windows) | Push/PR para master |
| **ci.yml** | Pipeline RAFAELIA (native + Android + testes) | Push/PR para master |
| **quality-gates.yml** | Checks de qualidade de código | PR para master |
| **codeql.yml** | Análise de segurança | Push/PR/Schedule |

---

## ✅ Interpretando Status

| Símbolo | Status | Ação |
|---------|--------|------|
| ✅ | Passou | Tudo OK! |
| ❌ | Falhou | Veja logs e corrija |
| 🟡 | Em progresso | Aguarde |
| ⚪ | Pulado | Normal se opcional |
| 🔄 | Reenviado | Tentando novamente |

---

## 🐛 Erros Comuns em CI

### 1. Build Failure (build.yml)

**Sintomas:**
```
❌ build.yml → build → Build release
```

**Como Ver:**
1. Clique no ❌ vermelho
2. Clique em "build"
3. Clique em "Build release"
4. Veja o erro no final

**Correções Comuns:**
```bash
# Erro de sintaxe Rust
nano native/src/...
git commit -am "fix: syntax error"
git push

# Erro de dependência
python3 build.py ndk
python3 build.py -v native
```

---

### 2. Test Failure (ci.yml)

**Sintomas:**
```
❌ ci.yml → android-build → Build APK
```

**Como Ver:**
1. Clique no workflow falhado
2. Veja "android-build" job
3. Expanda "Build APK using build.py"

**Correções Comuns:**
```bash
# Teste local primeiro
python3 build.py -v app

# Se passar, erro pode ser de ambiente CI
# Verifique .github/ci.prop
cat .github/ci.prop
```

---

### 3. Quality Gate Failure (quality-gates.yml)

**Sintomas:**
```
❌ quality-gates.yml → code-quality → Check Python files
```

**Como Ver:**
1. Veja qual job falhou
2. Corrija o problema de qualidade

**Correções Comuns:**
```bash
# Erro de sintaxe Python
python3 -m py_compile build.py

# Erro em script shell
bash -n scripts/meu_script.sh

# Erro de documentação
# Adicione arquivos faltantes mencionados
```

---

### 4. CodeQL Failure (codeql.yml)

**Sintomas:**
```
❌ codeql.yml → Analyze
```

**Como Ver:**
1. Veja alertas de segurança
2. Corrija vulnerabilidades

**Correções Comuns:**
- Corrigir código inseguro
- Adicionar validação de entrada
- Usar funções seguras

---

## 🔄 Workflow de Correção

```
┌─────────────────────┐
│ PUSH para GitHub    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Workflows executam  │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐    ┌────────┐
│ Passou │    │ Falhou │
└────────┘    └────┬───┘
                   │
                   ▼
           ┌───────────────┐
           │ Ver logs      │
           └───────┬───────┘
                   │
                   ▼
           ┌───────────────┐
           │ Corrigir      │
           └───────┬───────┘
                   │
                   ▼
           ┌───────────────┐
           │ PUSH novamente│
           └───────────────┘
```

---

## 📝 Comandos Úteis

### Antes de Fazer Push

```bash
# Teste tudo localmente
python3 build.py -v native  # Código nativo
python3 build.py -v app     # APK
python3 -m py_compile *.py  # Sintaxe Python

# Veja o que vai ser commitado
git status
git diff

# Commit e push
git add .
git commit -m "fix: descrição clara"
git push origin sua-branch
```

### Depois do Push

```bash
# Monitore via CLI
gh run watch

# Ou via navegador
# https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

---

## 🎯 Checklist Pré-Push

Antes de fazer `git push`:

- [ ] Compilou localmente: `python3 build.py -v all`
- [ ] Testou apenas nativo: `python3 build.py -v native`
- [ ] Verificou Python: `python3 -m py_compile build.py`
- [ ] Verificou shell scripts: `bash -n script.sh`
- [ ] Commit message claro e descritivo
- [ ] Branch correto: `git branch`

---

## 🚨 Quando Pedir Ajuda

Abra uma issue se:

1. ✅ Testou localmente e passou
2. ❌ CI falha mas você não entende o erro
3. 📝 Tentou as correções deste guia
4. 📋 Tem os logs completos para compartilhar

**Template:**
```markdown
**Problema:** CI falha em [workflow]
**Branch:** [nome-da-branch]
**Commit:** [hash do commit]
**Link do run:** [URL do GitHub Actions]
**Log:**
```
[Cole aqui]
```
```

---

## 🔗 Links Rápidos

- **Actions**: https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
- **Guia Completo**: [GUIA_COMPILACAO_ARM64_TROUBLESHOOTING.md](GUIA_COMPILACAO_ARM64_TROUBLESHOOTING.md)
- **English Guide**: [ARM64_COMPILATION_TROUBLESHOOTING_GUIDE.md](ARM64_COMPILATION_TROUBLESHOOTING_GUIDE.md)
- **README**: [README.MD](README.MD)

---

**Dica:** Salve este cartão nos favoritos! 🔖
