# Fluxograma de Compilação e CI/CD para ARM64

Este documento apresenta diagramas visuais do processo de compilação e monitoramento do Magisk_Rafaelia para ARM64.

---

## 📊 Visão Geral do Processo

```
┌─────────────────────────────────────────────────────────────┐
│                   COMPILAÇÃO ARM64                           │
│                                                              │
│  Desenvolvedor → Código → Build → Testes → CI/CD → APK     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo Completo de Desenvolvimento

```
┌──────────────────┐
│   1. CLONAR      │
│   Repositório    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   2. CONFIGURAR  │
│   config.prop    │
│   arm64-v8a      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   3. INSTALAR    │
│   NDK (ONDK)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   4. COMPILAR    │
│   Localmente     │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│SUCESSO?│ │ ERRO?  │
└───┬────┘ └───┬────┘
    │          │
    │          ▼
    │    ┌──────────────┐
    │    │ 5. CORRIGIR  │
    │    │    Erro      │
    │    └──────┬───────┘
    │           │
    │           └───────┐
    │                   │
    ▼                   ▼
┌────────────────────────────┐
│   6. COMMIT + PUSH         │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│   7. GITHUB ACTIONS        │
│   Workflows Executam       │
└──────────┬─────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐    ┌────────┐
│  ✅    │    │   ❌   │
│PASSOU  │    │ FALHOU │
└───┬────┘    └───┬────┘
    │             │
    │             ▼
    │      ┌──────────────┐
    │      │ 8. VER LOGS  │
    │      └──────┬───────┘
    │             │
    │             ▼
    │      ┌──────────────┐
    │      │ 9. CORRIGIR  │
    │      └──────┬───────┘
    │             │
    │             └────────┐
    │                      │
    ▼                      ▼
┌─────────────────────────────┐
│   10. APK PRONTO! 🎉        │
└─────────────────────────────┘
```

---

## 🏗️ Processo de Compilação Detalhado

```
┌────────────────────────────────────────────────────────┐
│                COMPILAÇÃO LOCAL                        │
└────────────────────────────────────────────────────────┘

  python3 build.py -v all
         │
         ▼
┌────────────────────┐
│  ETAPA 1: RUST     │
│  ─────────────     │
│  • base.so         │ ◄─── Rust sysroot (ONDK)
│  • core.so         │      - arm64-v8a target
│  • boot.so         │      - rafaelia modules
│  • resetprop.so    │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│  ETAPA 2: C++      │
│  ─────────────     │
│  • magisk          │ ◄─── NDK + ndk-build
│  • magiskboot      │      - arm64-v8a ABI
│  • magiskinit      │      - Android API 23+
│  • magiskpolicy    │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│  ETAPA 3: GRADLE   │
│  ─────────────     │
│  • app module      │ ◄─── Android Gradle
│  • stub APK        │      - Build tools 34
│  • Resources       │      - Java 17/21
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│  ETAPA 4: PACKAGE  │
│  ─────────────     │
│  • Copy binaries   │
│  • Sign APK        │
│  • out/app-*.apk   │ ◄─── APK Final
└────────────────────┘
```

---

## 🔍 Arquitetura de Builds Multi-ABI

```
┌─────────────────────────────────────────────────────┐
│              config.prop (Configuração)             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  OPÇÃO 1: Padrão (SEM config.prop)                 │
│  ───────────────────────────────────────────       │
│  abiList = armeabi-v7a, x86, arm64-v8a, x86_64     │
│                                                     │
│  Resultado: 4 conjuntos de binários                │
│  Tempo: ~4x mais lento                              │
│  APK: ~30% maior                                    │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  OPÇÃO 2: ARM64 apenas (COM config.prop) ✅        │
│  ────────────────────────────────────────────      │
│  abiList = arm64-v8a                                │
│                                                     │
│  Resultado: 1 conjunto de binários                 │
│  Tempo: Baseline (mais rápido)                     │
│  APK: Menor (~30% redução)                          │
│  Dispositivos: Modernos (RMX3834, etc)             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚦 Estados do GitHub Actions

```
┌───────────────────────────────────────────────────┐
│          WORKFLOW STATUS DIAGRAM                  │
└───────────────────────────────────────────────────┘

   Push/PR
      │
      ▼
┌───────────────┐
│  Triggered    │  ⚪ Cinza - Aguardando
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Queued       │  🟡 Amarelo - Na fila
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Running      │  🟡 Amarelo - Executando
└───────┬───────┘
        │
    ┌───┴───┐
    │       │
    ▼       ▼
┌────────┐ ┌────────┐
│Success │ │ Failed │
│   ✅   │ │   ❌   │
└────────┘ └───┬────┘
               │
               ▼
        ┌──────────────┐
        │ View Logs    │
        │ Fix Issues   │
        │ Retry Build  │
        └──────────────┘
```

---

## 📋 Workflows Principais

```
┌───────────────────────────────────────────────────────────┐
│                   build.yml                               │
├───────────────────────────────────────────────────────────┤
│  Trigger: Push/PR para master                             │
│  Runner: macOS-15                                         │
│  Jobs:                                                    │
│    1. build           → Compilação completa              │
│    2. test-build      → Windows + Linux                  │
│    3. avd-test        → Testes em emulador               │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                   ci.yml                                  │
├───────────────────────────────────────────────────────────┤
│  Trigger: Push/PR para master                             │
│  Runner: ubuntu-latest                                    │
│  Jobs:                                                    │
│    1. native-build        → Binários nativos             │
│    2. android-build       → APK Android                  │
│    3. android-instrumented → Testes instrumentados       │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                quality-gates.yml                          │
├───────────────────────────────────────────────────────────┤
│  Trigger: PR para master                                  │
│  Runner: ubuntu-latest                                    │
│  Jobs:                                                    │
│    1. code-quality        → Lint Python/Shell            │
│    2. documentation-check → Docs obrigatórios            │
│    3. build-validation    → Valida build.py              │
│    4. security-check      → Scan de segurança            │
│    5. governance-compliance → ativar.txt v999            │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                  codeql.yml                               │
├───────────────────────────────────────────────────────────┤
│  Trigger: Push/PR + Schedule                              │
│  Runner: ubuntu-latest                                    │
│  Jobs:                                                    │
│    1. analyze → Análise de segurança CodeQL              │
└───────────────────────────────────────────────────────────┘
```

---

## 🐛 Mapa de Erros Comuns

```
┌────────────────────────────────────────────────────────┐
│              ERRO                    SOLUÇÃO            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  NDK not found               →  build.py ndk          │
│                                                        │
│  Rust compilation error      →  build.py clean        │
│                                 build.py ndk          │
│                                                        │
│  Gradle dependency fail      →  ./gradlew --refresh   │
│                                                        │
│  Out of memory               →  GRADLE_OPTS=-Xmx2g    │
│                                 MAKEFLAGS=-j4         │
│                                                        │
│  Permission denied           →  chmod +x build.py     │
│                                 chmod +x *.sh         │
│                                                        │
│  CI build fails (local OK)   →  Check .github/ci.prop │
│                                 Review workflow logs  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 Checklist de Verificação

```
PRÉ-COMMIT
  ├─ ☐ Compilou localmente sem erros
  ├─ ☐ Testou: python3 build.py -v native
  ├─ ☐ Testou: python3 build.py -v all
  ├─ ☐ APK gerado em out/app-debug.apk
  ├─ ☐ Verificou arch: file native/out/arm64-v8a/magisk
  └─ ☐ Commit message descritivo

PRÉ-PUSH
  ├─ ☐ git status (sem arquivos inesperados)
  ├─ ☐ git diff (revisou mudanças)
  ├─ ☐ Branch correto
  └─ ☐ Pronto para CI

PÓS-PUSH
  ├─ ☐ Monitora workflows em /actions
  ├─ ☐ Se falhar: vê logs, corrige, repete
  └─ ☐ Se passar: APK disponível em artifacts
```

---

## 🔗 Navegação dos Documentos

```
README.MD
    │
    ├─► COMPILAR_ARM64.md (PT)
    │   └─► Guia rápido
    │
    ├─► BUILD_ARM64.md (EN)
    │   └─► Quick guide
    │
    ├─► GUIA_COMPILACAO_ARM64_TROUBLESHOOTING.md (PT) ⭐
    │   └─► Guia completo com resolução de erros
    │
    ├─► ARM64_COMPILATION_TROUBLESHOOTING_GUIDE.md (EN) ⭐
    │   └─► Complete guide with error resolution
    │
    ├─► CI_MONITORING_QUICKREF.md (PT) ⭐
    │   └─► Referência rápida para CI/CD
    │
    └─► ARM64_COMPILATION_WORKFLOW_DIAGRAM.md (PT/EN) ⭐
        └─► Este documento - Fluxogramas visuais
```

---

## 📱 Exemplo de Caso de Uso

### Cenário: Primeira Compilação ARM64

```
DIA 1 - SETUP
  09:00 │ git clone --recurse-submodules ...
  09:05 │ cd Magisk_Rafaelia
  09:05 │ cat > config.prop << 'EOF' ... (arm64-v8a)
  09:06 │ python3 build.py ndk
  09:15 │ ✅ NDK instalado

DIA 1 - PRIMEIRA TENTATIVA
  09:16 │ python3 build.py -v all
  09:18 │ ❌ Erro: rafaelia_audit.rs:45 - not found
  09:20 │ nano native/src/core/rafaelia_audit.rs
  09:25 │ (corrige o erro)
  09:26 │ python3 build.py -v native
  09:30 │ ✅ Native passou!
  09:31 │ python3 build.py -v all
  09:45 │ ✅ Build completo OK!

DIA 1 - CI/CD
  09:46 │ git add .
  09:46 │ git commit -m "fix: rafaelia audit error"
  09:47 │ git push origin minha-branch
  09:48 │ GitHub Actions iniciou
  10:00 │ ✅ build.yml passou
  10:15 │ ✅ ci.yml passou
  10:20 │ ✅ quality-gates.yml passou
  10:30 │ ✅ Todos checks passaram!

DIA 1 - RESULTADO
  10:31 │ APK disponível em artifacts
  10:35 │ adb install out/app-debug.apk
  10:36 │ ✅ Instalado no dispositivo!
  10:40 │ 🎉 SUCESSO!
```

---

## 🆘 Quando Usar Cada Guia

```
┌─────────────────────────────────────────────────────┐
│  SITUAÇÃO                        USE                │
├─────────────────────────────────────────────────────┤
│  Primeira vez compilando      → BUILD_ARM64.md      │
│  Erro durante compilação      → TROUBLESHOOTING.md  │
│  CI/CD falhou                 → QUICKREF.md         │
│  Quer entender o processo     → WORKFLOW_DIAGRAM.md │
│  Precisa de APK rápido        → OBTER_APK_RAPIDO.md │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Conclusão

Estes diagramas fornecem uma visão visual clara de:
- ✅ Processo completo de compilação
- ✅ Fluxo de trabalho CI/CD
- ✅ Estados dos workflows
- ✅ Resolução de erros
- ✅ Navegação da documentação

**Use este documento como referência visual** ao seguir os guias de troubleshooting!

---

**Magisk_Rafaelia** - Documentação Visual Completa 📊
