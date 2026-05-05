# Auditoria de Build, Release, CI e Integração Nativa — 2026-05-05

## Escopo e regra aplicada

- Repositório auditado: `Magisk_Rafaelia`.
- Condição especial solicitada:
  - `Vectras-VM-Android`: não aplicável, porque este não é o repositório selecionado.
  - `termux-app-rafacodephi`: não aplicável, porque este não é o repositório selecionado.
- Modo desta entrega: auditoria, classificação e relatório. Nenhuma correção estrutural de build/release foi implementada nesta etapa.

## Classificação executiva

| ID | Severidade | Classe | Estado | Evidência | Impacto |
| --- | --- | --- | --- | --- | --- |
| RAFA-BUILD-001 | Crítica | Ambiente / Android SDK | Confirmado localmente | `./app/gradlew -p app tasks --all --no-daemon` falha por ausência de `ANDROID_HOME`/`app/local.properties`. | Impede avaliação local de tarefas Gradle e qualquer APK local neste ambiente. |
| RAFA-BUILD-002 | Crítica | Divergência de NDK | Confirmado por fonte | Gradle declara `ndkVersion = "29.0.13846066"`, `build.py` usa ONDK `r29.2`, workflows instalam `ndk;29.2.11058015` e depois executam `build.py ndk`. | Alto risco de caminho de NDK inconsistente entre Gradle, ONDK e CI. |
| RAFA-BUILD-003 | Crítica | Workflow unsigned desalinhado com projeto | Confirmado por fonte | `build-unsigned-apk.yml` usa JDK 17, SDK 34/build-tools 34 e `./app/gradlew -p "$MODULE"`, enquanto o projeto exige JDK 21, compileSdk/buildTools 36 e módulo real `:apk`. | Workflow tende a falhar ou montar artefato errado; não preserva fonte de verdade do build oficial. |
| RAFA-BUILD-004 | Alta | Assinatura / release | Confirmado por fonte | O workflow unsigned assina opcionalmente depois do build com secrets, mas não usa o contrato `config.prop`/`keyStore*` do build oficial. | Release oficial e trilha unsigned ficam semanticamente separados, dificultando rastreabilidade e políticas de assinatura. |
| RAFA-BUILD-005 | Alta | Ordem de execução nativa | Confirmado por fonte | `setupCoreLib()` exige `native/out/<abi>` com binários antes de empacotar JNI; workflows alternam entre Gradle direto e `build.py`. | Build de app sem etapa nativa prévia colapsa em `sync*JniLibs`. |
| RAFA-BUILD-006 | Alta | Matriz ABI e riscv64 | Confirmado por fonte | `build.py` exclui `riscv64` do default; `Buildnew.yml` inclui `riscv64` na matriz. | CI testa alvo experimental fora da baseline default, aumentando falsos negativos. |
| RAFA-BUILD-007 | Média | Upload de artefatos | Confirmado por fonte | Workflows fazem upload de `out`, APK individual, símbolos e relatórios, mas com nomes e trilhas divergentes. | Artefatos existem em vários formatos sem contrato único de consumo. |
| RAFA-BUILD-008 | Média | Qualidade de workflows | Confirmado localmente | YAML dos workflows é parseável por Ruby/Psych. | Sintaxe YAML não é o bloqueio primário; os bloqueios são contrato, ambiente e coerência. |

## Causas-raiz encontradas

1. **Fonte de verdade fragmentada para toolchain Android.**
   - Gradle define `compileSdkVersion(36)`, `buildToolsVersion = "36.0.0"`, `ndkPath = "$sdkDirectory/ndk/magisk"` e `ndkVersion = "29.0.13846066"`.
   - `build.py` define ONDK `r29.2`, valida `$ANDROID_HOME/ndk/magisk/ONDK_VERSION` e usa o NDK organizado como caminho real.
   - `build-unsigned-apk.yml` instala SDK/build-tools 34 e JDK 17, divergindo da configuração Gradle.

2. **Contrato de release oficial e contrato unsigned não estão alinhados.**
   - O caminho oficial `build.py app` chama Gradle no projeto `app`, usa `-PconfigPath=<config>` e move `apk-release.apk` para `out/app-release.apk`.
   - O workflow unsigned chama Gradle diretamente com `-PskipSigning`, procura APK em `${MODULE}/build/outputs/apk`, e não passa por `build.py` nem pelo mesmo contrato de artefatos.

3. **Build Gradle direto ignora pré-condição nativa.**
   - `setupCoreLib()` sincroniza `magiskboot`, `magiskinit`, `magiskpolicy`, `magisk`, `libinit-ld.so` e `libbusybox.so` para JNI.
   - A tarefa aborta se a quantidade esperada de binários nativos não existir, com mensagem para construir binários primeiro.
   - Qualquer workflow que pule `python3 build.py native` ou use módulo incorreto falha antes de produzir APK confiável.

4. **Ambiente local de auditoria não possui SDK Android configurado.**
   - `ANDROID_HOME` e `ANDROID_SDK_ROOT` estão vazios.
   - Gradle falhou antes de listar tarefas por ausência de SDK/local.properties.
   - Portanto, nenhum APK foi gerado neste ambiente durante a auditoria.

5. **Matriz ABI inclui alvo experimental sem separação explícita.**
   - A baseline de `build.py` exclui `riscv64` do conjunto default.
   - Um workflow de multiarquitetura inclui `riscv64` junto com ARM/ARM64/x86/x86_64, sem trilha experimental isolada.

## Classificação por subsistema

### Android / Gradle

- Estado: **bloqueado localmente por SDK ausente**.
- Fonte de verdade atual: `app/buildSrc/src/main/java/Setup.kt` para SDK/JDK/NDK Gradle; `build.py` para orquestração.
- Risco: chamadas Gradle diretas em workflows podem ignorar orquestração nativa e assinatura.

### NDK / C / C++ / Rust

- Estado: **contrato parcialmente definido, mas divergente**.
- `build.py` é a trilha mais completa para ONDK, Rust e `ndk-build`.
- Workflows instalam NDK padrão e depois baixam ONDK; isso precisa ser tratado como decisão explícita, não duplicação casual.

### JNI / ABI

- Estado: **pré-condição forte**.
- `:core` exige binários por ABI antes do empacotamento.
- ARM32 (`armeabi-v7a`) e ARM64 (`arm64-v8a`) são suportados pelo mapa de ABIs, mas não foram compilados neste ambiente por ausência do SDK/NDK configurado.

### Release / assinatura

- Estado: **separação insegura de contratos**.
- A trilha unsigned existe como workflow separado, mas não demonstra equivalência com a trilha oficial de release.
- A assinatura opcional via `apksigner` no workflow unsigned não substitui o contrato oficial `config.prop`/Gradle/build.py para release rastreável.

### GitHub Actions / artefatos

- Estado: **artefatos configurados, mas não normalizados**.
- Há uploads de `out`, APKs, símbolos, logs, snapshots e relatórios.
- Falta um contrato único declarando nomes, conteúdo mínimo e matriz de assinatura/ABI.

## Comandos executados e resultados

| Comando | Resultado |
| --- | --- |
| `git status --short` | Sem alterações antes da auditoria. |
| `find .. -name AGENTS.md -print` | Nenhum `AGENTS.md` encontrado no escopo. |
| `rg --files -g 'build.gradle*' -g 'settings.gradle*' -g 'gradlew' -g 'gradle.properties' -g '.github/workflows/**' -g 'AndroidManifest.xml' -g 'CMakeLists.txt' -g 'Cargo.toml'` | Identificou projeto Android em `app/`, CMake em `native/` e Cargo em `native/src/`/`tools/`. |
| `python3 -m py_compile build.py` | Passou. |
| `python3 build.py --help` | Passou e listou ações disponíveis. |
| `./app/gradlew -p app tasks --all --no-daemon` | Falhou: SDK location not found; exige `ANDROID_HOME` ou `app/local.properties`. |
| `ruby -e 'require "yaml"; Dir[".github/workflows/*.{yml,yaml}"].sort.each { ... }'` | Passou: todos os workflows `.yml`/`.yaml` parsearam como YAML. |

## Artefatos e APKs

- APK unsigned gerado nesta auditoria: **não**.
- APK signed gerado nesta auditoria: **não**.
- ARM32 (`armeabi-v7a`) compilado nesta auditoria: **não**.
- ARM64 (`arm64-v8a`) compilado nesta auditoria: **não**.
- Bloqueio verificado: ausência de `ANDROID_HOME`/`ANDROID_SDK_ROOT` e ausência de `app/local.properties` neste ambiente.
- Artefatos configurados em workflows: `out`, APKs, símbolos, logs, snapshots, relatórios de governança/performance.

## Recomendações para próxima etapa de implementação

1. Definir uma única fonte de verdade para JDK, SDK, build-tools e ONDK, consumida por `build.py`, Gradle e workflows.
2. Transformar a trilha unsigned em modo de validação explícito, sem substituir release oficial assinado.
3. Fazer workflows chamarem `build.py` para build nativo + app, exceto em tarefas declaradamente de lint/metadata.
4. Separar `riscv64` em matriz experimental ou removê-lo da matriz release padrão.
5. Normalizar artefatos: `app-debug.apk`, `app-release-unsigned.apk`, `app-release-signed.apk`, símbolos, logs e manifest JSON com ABI, commit, assinatura e checksums.
6. Só avançar para compilação completa depois de provisionar SDK/ONDK compatível com as versões declaradas.

## Bloqueios restantes

- SDK Android não configurado localmente.
- ONDK `r29.2` não validado localmente em `$ANDROID_HOME/ndk/magisk`.
- Sem keystore de release para gerar APK assinado oficial.
- Sem emulador/dispositivo para validar instalação/execução em ARM32/ARM64.
