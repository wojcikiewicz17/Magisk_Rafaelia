# Mapa de origem do sistema de build/release — 2026-05-05

Este documento registra as fontes auditadas antes de qualquer implementação estrutural.

## Fontes primárias

| Área | Arquivo | Papel |
| --- | --- | --- |
| Orquestração principal | `build.py` | Entrada de build nativo, app, stub, teste, clean, ONDK, cargo, clippy, AVD. |
| Configuração Android comum | `app/buildSrc/src/main/java/Setup.kt` | Define compileSdk, buildTools, NDK Gradle, Java/Kotlin target, empacotamento JNI, recursos e assinatura Gradle. |
| Configuração Gradle global | `app/buildSrc/src/main/java/Plugin.kt` | Carrega `gradle.properties`, `config.prop`, commit hash e lista de ABIs. |
| Projeto Gradle | `app/settings.gradle.kts` | Inclui módulos `:apk`, `:core`, `:shared`, `:stub`, `:test`. |
| App principal | `app/apk/build.gradle.kts` | Declara aplicação Android principal e dependências UI/desugaring. |
| Core Android | `app/core/build.gradle.kts` | Biblioteca core que recebe JNI/assets nativos. |
| Propriedades Gradle | `app/gradle.properties` | Define JDK/Gradle runtime, AndroidX e versionCode/stubVersion. |
| Dependências Gradle | `app/gradle/libs.versions.toml` | Catálogo de versões de AGP, Kotlin, AndroidX, libsu e plugins. |
| Configuração local opcional | `config.prop.sample` | Documenta `abiList`, `outdir` e chaves de assinatura. |
| CMake nativo | `native/CMakeLists.txt` | Entrada CMake nativa presente, mas a trilha principal usa `build.py`/`ndk-build`. |
| Android make nativo | `native/src/Android.mk` e `native/src/Application.mk` | Build C/C++ via NDK. |
| Rust nativo | `native/src/Cargo.toml` | Workspace Rust para componentes nativos. |
| Workflow oficial upstream-like | `.github/workflows/build.yml` | Build release/debug, testes e uploads com action local de setup. |
| Workflow Android CI | `.github/workflows/android.yml` | Build debug por `build.py`, upload de APK e logs. |
| Workflow multi-ABI | `.github/workflows/Buildnew.yml` | Matriz ABI, setup SDK/Rust/ONDK, build native/app e upload. |
| Workflow unsigned | `.github/workflows/build-unsigned-apk.yml` | Trilha separada para APK unsigned e assinatura opcional pós-build. |
| Quality gates | `.github/workflows/quality-gates.yml` | Preflight documental, scripts, governança e segurança. |
| Governança | `.github/workflows/governance-check.yml` | Validação de documentos e relatórios de governança. |

## Contratos extraídos

### Build oficial por script

1. `build.py` carrega `config.prop` e `app/gradle.properties`.
2. `build.py native` exige SDK/ONDK e gera `native/out/<abi>`.
3. `build.py app` entra em `app/`, chama Gradle com `:apk:assembleDebug` ou `:apk:assembleRelease` e `-PconfigPath=<config>`.
4. O APK é movido para `out/app-debug.apk` ou `out/app-release.apk`.

### Pré-condição JNI

1. `:core` sincroniza binários de `native/out/<abi>` para `src/<variant>/jniLibs/<abi>`.
2. A lista esperada inclui `magiskboot`, `magiskinit`, `magiskpolicy`, `magisk`, `libinit-ld.so` e `libbusybox.so`.
3. Sem esses binários, a tarefa aborta antes de empacotar o app.

### Assinatura

1. `config.prop.sample` declara `keyStore`, `keyStorePass`, `keyAlias` e `keyPass` como grupo indivisível.
2. `build-unsigned-apk.yml` assina opcionalmente com secrets `RELEASE_KEYSTORE_BASE64`, `RELEASE_KEY_ALIAS`, `RELEASE_STORE_PASS`, `RELEASE_KEY_PASS` usando `apksigner`.
3. Esses contratos precisam ser unificados na próxima etapa para preservar release oficial assinado e validação unsigned separada.

## Dependências externas classificadas

| Item | Classificação | Observação |
| --- | --- | --- |
| Android SDK / cmdline-tools / build-tools | EXTERNAL_DEPENDENCY | Necessário para qualquer Gradle Android local/CI. |
| ONDK `r29.2` | EXTERNAL_DEPENDENCY | Baixado de `topjohnwu/ondk` por `build.py ndk`. |
| Gradle wrapper | VENDORED_BOOTSTRAP | `app/gradlew` controla versão Gradle do projeto. |
| Maven Google/MavenCentral/JitPack | EXTERNAL_DEPENDENCY | Resolvem AGP, Kotlin, AndroidX, libsu e plugins. |
| BusyBox zip | EXTERNAL_DEPENDENCY | Baixado e validado por SHA-256 em `Setup.kt`. |
| Rust toolchain e targets | EXTERNAL_DEPENDENCY | Usados em `native/src` via Cargo. |
| Keystore de release | SECRET_DEPENDENCY | Deve existir só em ambiente seguro de release. |
| Vectras | NOT_APPLICABLE | Nenhuma regra especial aplicada porque o repositório selecionado não é Vectras nem Termux. |

## Estado de conclusão da auditoria

- Auditoria inicial concluída.
- Classificação registrada.
- Documentos de origem gerados.
- Implementação estrutural não iniciada nesta etapa por solicitação explícita de auditoria primeiro.
