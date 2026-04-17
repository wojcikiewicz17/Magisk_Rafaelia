# Workflow Organization Guide / Guia de Organização de Workflows

## Objetivo

Consolidar build/validação/release em **dois pipelines canônicos** e remover duplicidade operacional.

## Pipelines oficiais (fonte de verdade)

### 1) CI contínua (PR/push)
- **Arquivo**: `.github/workflows/ci.yml`
- **Papel**:
  - validação pré-CI (`scripts/pre_ci_validate.py --skip-slow`)
  - build debug via `build.py -v all`
  - upload obrigatório de artefatos de debug (`out/` + `app/apk/build/outputs`)
- **Triggers oficiais**:
  - `push` para `main` e `develop`
  - `pull_request` para `main` e `develop`
  - `workflow_dispatch` para execução manual de diagnóstico

### 2) Release/manual
- **Arquivo**: `.github/workflows/release.yml`
- **Papel**:
  - build release (`build.py -vr all`)
  - enforcement de política de assinatura para canal oficial
  - verificação de saída sem APK unsigned
  - upload de artefatos de release e símbolos
- **Triggers oficiais**:
  - `workflow_dispatch`
  - `push` em tags `v*`

## Workflows legados desativados

Os workflows abaixo foram retirados do diretório ativo e movidos para `.github/workflows/archive/`:

- `android.yml`
- `Buildnew.yml`
- `build.yml`
- `build-unsigned-apk.yml`
- `build.ymlold`

Essa movimentação desativa execução pelo GitHub Actions e preserva histórico técnico.

## Padrões de versão de actions

Nos pipelines canônicos:

- `actions/checkout@v4`
- `actions/setup-java@v4`
- `actions/setup-python@v5`
- `actions/upload-artifact@v4`

## Política de artifacts

- **CI (`ci.yml`)**: retenção de 14 dias, compressão nível 9, falha se nenhum arquivo for encontrado.
- **Release (`release.yml`)**: retenção de 30 dias, compressão nível 9, falha se nenhum arquivo for encontrado.
- Sempre publicar `out/` e `app/apk/build/outputs` para rastreabilidade de build.

## Estratégia de branch refletida nos workflows

Estratégia ativa:
- `main`: produção
- `develop`: integração contínua

Os workflows canônicos utilizam exclusivamente `main`/`develop` para PR/push contínuos.
