# Demo Kit — Green Jobs Brasil

Este kit reúne materiais prontos para apresentação, captura de telas e roteiro curto para reuniões com clientes e parceiros.

## Conteúdo

- DEMO_SCRIPT_7MIN.md — roteiro guiado (7–10 min)
- ONEPAGER_CLIENTES.md — one-pager com proposta de valor
- outputs/ — pasta onde ficam screenshots e PDF gerados
- scripts auxiliares:
  - scripts/demo_playbook.ps1 — orquestra a demo (deps, seed, API, abas)
  - scripts/demo_capture.ps1 — captura screenshots e gera PDF do playbook

## Pré-requisitos

- Windows + PowerShell
- Python 3.13 instalado e API rodando em 127.0.0.1:8002
- Navegador Chromium disponível (Chrome ou Microsoft Edge)

## Passo a passo rápido

1) Preparar e iniciar a demo (inclui seed):

```powershell
cd "C:\Users\Bruno\Empresas Verdes"
powershell -ExecutionPolicy Bypass -File .\scripts\demo_playbook.ps1
```

2) Capturar screenshots e PDF automaticamente:

```powershell
# Salva em docs\demo-kit\outputs
powershell -ExecutionPolicy Bypass -File .\scripts\demo_capture.ps1
```

3) Apresentar usando o Playbook Visual:

- http://127.0.0.1:8002/demo-playbook

## Dicas

- Se a porta 8002 estiver ocupada, feche processos Python e rode novamente.
- Caso falte alguma dependência, use `-ReinstallDeps` no `demo_playbook.ps1`.
- Você pode trocar a porta com `-Port 8010` nos scripts.
