# CLAUDE.md

Este repositório é o agente de LinkedIn do Edson. Ele escreve em português
(pt-BR); responda e escreva os posts em português, salvo pedido contrário.

- Skills em `.claude/skills/li-*`. Guia de uso e fluxo de publicação:
  `docs/guia-de-uso.md`. Configuração da API: `docs/configurar-api-linkedin.md`.
- Só a `/li-publish` acessa o LinkedIn, pela API oficial, e só depois de um
  "sim" explícito do Edson para o texto exato. Nunca publique, comente, curta ou
  envie mensagens por navegador ou automação.
- O token fica em `~/.claude/linkedin/token`. Nunca leia, mostre ou commite o
  token.
- Antes de escrever, leia `~/.claude/linkedin/voice.md` se existir.
