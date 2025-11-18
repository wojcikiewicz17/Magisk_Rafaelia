# Archived Workflows / Workflows Arquivados

## 📦 Propósito / Purpose

**English**: This directory contains workflows that have been archived because they are:
- Not applicable to the current project (cloud deployments we don't use)
- Potentially dangerous (force-merge)
- Redundant with other workflows

**Português**: Este diretório contém workflows que foram arquivados porque são:
- Não aplicáveis ao projeto atual (deployments cloud que não usamos)
- Potencialmente perigosos (force-merge)
- Redundantes com outros workflows

---

## 🗂️ Arquivos Arquivados / Archived Files

### ⚠️ Perigosos (Removidos da Ativação) / Dangerous (Removed from Activation)

**force-merge.yml**
- **Motivo**: Viola proteções de branch, permite merges forçados não seguros
- **Reason**: Violates branch protections, allows unsafe forced merges
- **Status**: Mantido para referência, mas nunca deve ser ativado
- **Status**: Kept for reference but should never be activated

### ☁️ Cloud Deployments (Não Utilizados) / Cloud Deployments (Not Used)

**alibabacloud.yml**
- Deployment para Alibaba Cloud
- Não usado neste projeto

**aws.yml**
- Deployment para AWS
- Não usado neste projeto

**azure-functions-app-java.yml**
- Deployment de Azure Functions (Java)
- Não usado neste projeto

**azure-functions-app-python.yml**
- Deployment de Azure Functions (Python)
- Não usado neste projeto

**azure-webapps-java-jar.yml**
- Deployment de Azure Web Apps (Java JAR)
- Não usado neste projeto

**azure-webapps-python.yml**
- Deployment de Azure Web Apps (Python)
- Não usado neste projeto

**google.yml**
- Deployment para Google Cloud
- Não usado neste projeto

**gatsby.yml**
- Build Gatsby site
- Não aplicável (não é site Gatsby)

**nextjs.yml**
- Build Next.js site
- Não aplicável (não é site Next.js)

---

## 🔄 Restauração / Restoration

**English**: If any of these workflows become necessary in the future:

```bash
# To restore a workflow:
git mv .github/workflows/.archived/WORKFLOW_NAME.yml .github/workflows/
git commit -m "chore: restore WORKFLOW_NAME workflow"
```

**Português**: Se algum destes workflows se tornar necessário no futuro:

```bash
# Para restaurar um workflow:
git mv .github/workflows/.archived/WORKFLOW_NAME.yml .github/workflows/
git commit -m "chore: restaura workflow WORKFLOW_NAME"
```

---

## ⛔ Não Restaurar / Do Not Restore

**force-merge.yml** should NEVER be restored without:
1. Extensive security review
2. Strong justification
3. Approval from project maintainers
4. Proper safeguards implemented

**force-merge.yml** NUNCA deve ser restaurado sem:
1. Revisão extensa de segurança
2. Justificativa forte
3. Aprovação dos mantenedores do projeto
4. Salvaguardas apropriadas implementadas

---

## 📚 Referências / References

- [WORKFLOW_ORGANIZATION.md](../../docs/WORKFLOW_ORGANIZATION.md) - Guia completo de organização
- [BRANCHING_STRATEGY.md](../../docs/BRANCHING_STRATEGY.md) - Estratégia de branches

---

**Last Updated**: 2025-11-18  
**Archived By**: Repository consolidation effort  
**Documentation**: See docs/WORKFLOW_ORGANIZATION.md
