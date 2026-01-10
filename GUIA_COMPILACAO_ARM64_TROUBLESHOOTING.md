# Guia Completo: Compilação ARM64 com Resolução de Erros

## 🎯 Objetivo

Este guia mostra **passo a passo** como compilar o Magisk_Rafaelia para ARM64 e como **acompanhar e corrigir** cada erro que aparecer nos checks do GitHub Actions.

---

## 📋 Pré-requisitos

### Requisitos do Sistema

```bash
# Verifique se você tem os requisitos
python3 --version  # Precisa ser 3.8 ou superior
java -version      # Precisa ser Java 17 ou 21
git --version      # Precisa ser 2.x ou superior
```

### Ferramentas Necessárias

- **Linux**: Ubuntu 20.04+ ou similar
- **macOS**: macOS 11+ (Big Sur ou superior)
- **Windows**: WSL2 com Ubuntu ou use o ambiente nativo

---

## 🚀 Parte 1: Configuração Inicial

### Passo 1: Clonar o Repositório

```bash
# Clone com todos os submódulos
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# Verifique que está no branch correto
git branch
```

### Passo 2: Configurar para ARM64

```bash
# Crie o arquivo de configuração
cat > config.prop << 'EOF'
# Configuração para ARM64 apenas
abiList=arm64-v8a
EOF

# Verifique que foi criado corretamente
cat config.prop
```

### Passo 3: Instalar o NDK do Magisk

```bash
# Baixa e instala o ONDK (Organized NDK)
python3 build.py ndk

# Isso vai:
# - Baixar o ONDK r29.2
# - Extrair em ./ndk-arm64
# - Configurar o ambiente Rust
# - Verificar as ferramentas
```

**Se der erro aqui:**
- Erro de rede: Verifique sua conexão e tente novamente
- Erro de permissão: Execute `chmod +x build.py`
- Python não encontrado: Instale Python 3.8+

---

## 🔨 Parte 2: Compilação Local

### Passo 4: Primeira Tentativa de Compilação

```bash
# Compile em modo debug com saída verbosa
python3 build.py -v all

# Isso vai:
# 1. Compilar código nativo (C++/Rust) para arm64-v8a
# 2. Compilar o app Android (APK)
# 3. Empacotar tudo em out/app-debug.apk
```

### Passo 5: Acompanhar a Compilação

A compilação tem várias etapas. Observe a saída:

```
✅ PASSO 1: Building Rust modules
   - Compiling base...
   - Compiling core...
   - Compiling boot...
   
✅ PASSO 2: Building C++ components
   - Building magisk
   - Building magiskboot
   - Building magiskinit
   - Building magiskpolicy
   
✅ PASSO 3: Building Android app
   - Gradle sync
   - Building APK
   
✅ PASSO 4: Packaging
   - Copying binaries
   - Creating APK
```

---

## 🐛 Parte 3: Resolução de Erros Comuns

### Erro 1: NDK não encontrado

**Sintoma:**
```
Error: Android NDK not found
```

**Solução:**
```bash
# Reinstale o NDK
python3 build.py ndk

# Se persistir, configure manualmente
export ANDROID_NDK_HOME="$PWD/ndk-arm64"
```

---

### Erro 2: Erro de compilação Rust

**Sintoma:**
```
error[E0425]: cannot find function `something` in this scope
```

**Solução:**
```bash
# Limpe o build anterior
python3 build.py clean

# Atualize o Rust no NDK
python3 build.py ndk

# Tente novamente
python3 build.py -v native
```

---

### Erro 3: Gradle falha ao baixar dependências

**Sintoma:**
```
Could not resolve all dependencies
Connection timeout
```

**Solução:**
```bash
# Configure proxy (se necessário)
export GRADLE_OPTS="-Dhttp.proxyHost=... -Dhttp.proxyPort=..."

# OU use cache local do Gradle
./app/gradlew --refresh-dependencies

# Tente build de novo
python3 build.py -v app
```

---

### Erro 4: Erro de memória durante compilação

**Sintoma:**
```
error: LLVM ERROR: out of memory
The system cannot find the file specified
```

**Solução:**
```bash
# Limite os jobs paralelos
export MAKEFLAGS="-j4"  # Ajuste conforme sua RAM

# Configure Gradle para usar menos memória
export GRADLE_OPTS="-Xmx2g -XX:MaxMetaspaceSize=512m"

# Compile
python3 build.py -v all
```

---

### Erro 5: Permissões incorretas

**Sintoma:**
```
Permission denied: './build.py'
```

**Solução:**
```bash
# Corrija permissões
chmod +x build.py
find . -name "*.sh" -exec chmod +x {} \;
find . -name "*.py" -exec chmod +x {} \;
```

---

## 📊 Parte 4: Acompanhar Checks do GitHub Actions

### Passo 1: Ver Status dos Workflows

```bash
# Veja seus commits recentes
git log --oneline -5

# Faça push da sua branch
git push origin sua-branch

# No navegador, vá para:
# https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

### Passo 2: Identificar Qual Check Falhou

Os workflows principais são:

1. **build.yml** - Compilação completa
2. **ci.yml** - Pipeline RAFAELIA completo
3. **quality-gates.yml** - Verificações de qualidade
4. **codeql.yml** - Análise de segurança

**Onde ver:**
- ✅ Verde = Passou
- ❌ Vermelho = Falhou
- 🟡 Amarelo = Em progresso
- ⚪ Cinza = Não executado

### Passo 3: Ver Logs de Erro

**No GitHub:**
1. Clique no check que falhou (X vermelho)
2. Clique no job que falhou
3. Expanda a etapa que tem erro
4. Leia o erro completo

**Exemplo de log de erro:**
```
Run python3 build.py -v all
Building Rust modules...
error: could not compile `core`
  |
45 | let result = something()?;
  |              ^^^^^^^^^ not found in this scope
```

### Passo 4: Baixar Logs Completos

```bash
# Use o GitHub CLI (opcional)
gh run list --limit 5
gh run view <run-id>
gh run download <run-id>
```

---

## 🔄 Parte 5: Ciclo de Correção

### Fluxo Iterativo

```
1. COMPILAR localmente
   ↓
2. FALHOU?
   ├─ SIM → Veja o erro, corrija, volte ao passo 1
   └─ NÃO → Continue
   ↓
3. COMMIT suas mudanças
   ↓
4. PUSH para GitHub
   ↓
5. ACOMPANHE os checks
   ↓
6. CHECKS PASSARAM?
   ├─ SIM → Sucesso! 🎉
   └─ NÃO → Veja logs, corrija, volte ao passo 3
```

### Exemplo Prático

```bash
# 1. Teste local
python3 build.py -v native
# ❌ Erro encontrado em rafaelia_audit.rs

# 2. Corrija o arquivo
nano native/src/core/rafaelia_audit.rs
# Faça a correção necessária

# 3. Teste novamente
python3 build.py -v native
# ✅ Passou!

# 4. Teste build completo
python3 build.py -v all
# ✅ Passou!

# 5. Commit
git add native/src/core/rafaelia_audit.rs
git commit -m "fix: corrige erro de compilação em rafaelia_audit"

# 6. Push
git push origin sua-branch

# 7. Acompanhe no GitHub Actions
# https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

---

## 🔍 Parte 6: Debugging Avançado

### Ver Exatamente O Que Está Sendo Compilado

```bash
# Modo ultra-verboso
python3 build.py -v all 2>&1 | tee build.log

# Depois analise o log
grep -i "error" build.log
grep -i "warning" build.log
grep "APP_ABI" build.log  # Confirma ARM64
```

### Verificar Binários Gerados

```bash
# Liste binários ARM64
ls -lh native/out/arm64-v8a/

# Verifique a arquitetura
file native/out/arm64-v8a/magisk
# Deve mostrar: ELF 64-bit LSB executable, ARM aarch64

# Verifique símbolos
nm native/out/arm64-v8a/magisk | grep rafaelia
```

### Testar em Dispositivo Real

```bash
# Conecte seu dispositivo Android ARM64
adb devices

# Push do binário
adb push native/out/arm64-v8a/magisk /data/local/tmp/
adb shell chmod +x /data/local/tmp/magisk

# Teste
adb shell /data/local/tmp/magisk --version
```

---

## 📱 Parte 7: Instalação do APK

### Depois de Compilar com Sucesso

```bash
# APK estará em:
ls -lh out/app-debug.apk

# Instale no dispositivo
adb install out/app-debug.apk

# OU para reinstalar
adb install -r out/app-debug.apk

# OU copie para o celular
adb push out/app-debug.apk /sdcard/Download/
# Depois instale manualmente pelo gerenciador de arquivos
```

---

## 🎯 Parte 8: Checklist de Verificação

Antes de fazer commit/push, verifique:

- [ ] `python3 build.py -v native` passou sem erros
- [ ] `python3 build.py -v all` passou sem erros
- [ ] APK foi gerado em `out/app-debug.apk`
- [ ] Verificou que é ARM64: `file native/out/arm64-v8a/magisk`
- [ ] Testou instalação em dispositivo (opcional)
- [ ] Commit message é descritivo
- [ ] Push foi feito para branch correto

---

## 💡 Dicas Pro

### 1. Compilação Incremental

```bash
# Compile apenas o que mudou
python3 build.py -v native  # Só código nativo
python3 build.py -v app     # Só APK
```

### 2. Build Release (Otimizado)

```bash
# Para produção
python3 build.py -r all

# Gera out/app-release.apk (menor e mais rápido)
```

### 3. Limpar Quando Necessário

```bash
# Limpe build artifacts
python3 build.py clean

# Limpe tudo incluindo NDK (última opção)
rm -rf ndk-arm64 out native/out
python3 build.py ndk
```

### 4. Configuração para CI

```bash
# Use .github/ci.prop para CI
# Já configurado para ARM64:
cat .github/ci.prop
# abiList=arm64-v8a
```

---

## 🆘 Suporte

### Recursos Úteis

- **README Principal**: [README.MD](README.MD)
- **Guia de Compilação**: [COMPILAR_ARM64.md](COMPILAR_ARM64.md)
- **Como Obter APK**: [COMO_OBTER_APK.md](COMO_OBTER_APK.md)
- **Guia de Contribuição**: [CONTRIBUTING.md](CONTRIBUTING.md)

### Onde Pedir Ajuda

1. **Issues no GitHub**: Descreva seu erro com logs completos
2. **Pull Requests**: Mostre o que tentou fazer
3. **Discussions**: Para perguntas gerais

### Template de Issue para Erro de Compilação

```markdown
**Descrição do Erro:**
[Descreva o que aconteceu]

**Ambiente:**
- OS: [Linux/macOS/Windows]
- Python: [versão]
- Java: [versão]

**Comando Executado:**
```bash
python3 build.py -v all
```

**Log de Erro:**
```
[Cole o log completo aqui]
```

**O Que Já Tentei:**
- [ ] Limpei build com `build.py clean`
- [ ] Reinstalei NDK com `build.py ndk`
- [ ] Verifiquei config.prop
- [ ] Outros: [descreva]
```

---

## ✅ Conclusão

Agora você tem um guia completo para:
1. ✅ Configurar ambiente para ARM64
2. ✅ Compilar localmente
3. ✅ Identificar e corrigir erros
4. ✅ Acompanhar checks do GitHub Actions
5. ✅ Iterar até sucesso

**Próximo passo:** Comece pelo [Passo 1](#passo-1-clonar-o-repositório)!

---

**Magisk_Rafaelia** - Compilação ARM64 Simplificada 🚀
