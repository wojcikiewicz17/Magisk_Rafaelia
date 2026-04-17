# Dependency Baseline Audit

Este repositório possui uma auditoria automática para detectar dependências obsoletas na trilha de build/release:

- GitHub Actions com versões antigas de `checkout`, `setup-java`, `setup-python`, `setup-android`, `setup-gradle`, `upload-artifact` e `download-artifact`.
- Baseline de Gradle Wrapper (`app/gradle/wrapper/gradle-wrapper.properties`).
- Baseline de Android Gradle Plugin e Kotlin (`app/gradle/libs.versions.toml`).

## Execução local

```bash
python3 .github/scripts/dependency_audit.py
```

## Execução na CI

A auditoria roda no workflow `quality-gates.yml` no job **Dependency Baseline Audit** e falha o pipeline quando encontra baseline obsoleta.
