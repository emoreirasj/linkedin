# Guia de uso: agente de LinkedIn

Referência rápida das skills e do fluxo para postar. Abra o Claude Code dentro
desta pasta (`Documents\linkedin`) para as skills ficarem disponíveis.

## As skills

| comando | para quê | acessa o LinkedIn? |
| --- | --- | --- |
| `/li-post` | transforma uma ideia em post: 3 ganchos (de 21 fórmulas) e um rascunho humanizado | não |
| `/li-publish` | publica no seu perfil pela API oficial, só depois do seu "sim" | **sim** |
| `/li-human` | tira marcas de texto de IA e dá nota de 0 a 100 | não |
| `/li-comment` | comentários em posts de outras pessoas (9 tipos, nada de "ótimo post!") | não |
| `/li-reply` | respostas aos comentários dos seus posts, por ordem de importância | não |
| `/li-profile` | nota do perfil (0 a 100, 12 critérios) e reescrita do que perde ponto | não |
| `/li-plan` | plano da semana: o que postar, quando, e 10 pessoas para interagir | não |
| `/li-carousel` | carrossel em PDF: texto de cada slide e capa | não |
| `/li-repurpose` | um vídeo, newsletter ou transcrição vira uma semana de posts | não |
| `/li-dm` | nota de convite (200 caracteres), primeira mensagem e dois follow-ups | não |
| `/li-inbox` | triagem da caixa de entrada: cliente, recrutador, colega, pedido, spam | não |
| `/li-audit` | análise dos posts já publicados: o que funcionou e o que parar de fazer | não |

Nas skills que não acessam o LinkedIn, você cola o conteúdo (post, comentários,
mensagens, perfil) e recebe o texto pronto.

## Como postar

1. **Escreva.** No Claude Code:
   ```
   /li-post <sua ideia, com números e fatos reais>
   ```
   Exemplo: `/li-post reduzi o tempo de resposta a incidentes de 4h para 40min automatizando a triagem na AWS`.

2. **Escolha o gancho.** O Claude mostra 3 opções e escreve o post com uma
   delas. Peça outra se quiser: "usa o gancho 2".

3. **Ajuste.** Peça mudanças em linguagem normal: "mais curto", "tira a
   hashtag", "troca o final". Se aparecer `{{seu número}}`, é um dado que só
   você sabe; complete antes de publicar.

4. **Publique.**
   ```
   /li-publish
   ```
   O Claude mostra o texto final, a conta e o tamanho, e pergunta se pode
   publicar. Responda **sim** para enviar. Qualquer outra resposta não publica.

5. **Confira.** O Claude devolve o link do post. Se o post tiver um link
   externo, coloque-o no primeiro comentário, à mão: o LinkedIn reduz o alcance
   de posts com link no corpo.

### Atalho sem o Claude

Para publicar um texto já pronto direto do PowerShell:

```powershell
python .claude/skills/li-publish/publish.py post rascunho.txt          # só mostra a prévia
python .claude/skills/li-publish/publish.py post rascunho.txt --yes    # publica
```

## Boas práticas

- **Uma ideia por post.** Se tem duas, são dois posts.
- **Números em vez de adjetivos.** "40 minutos" convence mais que "muito mais rápido".
- **Primeira linha é tudo.** O feed corta em ~140 caracteres no celular.
- **No máximo 3 hashtags**, no final.
- **Nada inventado.** Métricas, clientes e resultados têm que ser reais.
- **Consistência > volume.** 3 a 4 posts por semana bem feitos rendem mais que
  um por dia feito às pressas. Use `/li-plan` para montar a semana.

## Configuração (uma vez)

- **Seu estilo:** copie `templates/voice.md` para
  `C:\Users\Dell\.claude\linkedin\voice.md` e preencha, ou cole 3 posts seus e
  peça "escreva meu voice.md a partir destes". Diga que escreve em português.
- **Token da API:** fica em `C:\Users\Dell\.claude\linkedin\token`. Passo a
  passo completo em [configurar-api-linkedin.md](configurar-api-linkedin.md).

## Manutenção

- **Token vence a cada 60 dias.** O atual vence por volta de **7/12/2026**.
  Quando a `/li-publish` der erro 401, gere outro no
  [Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
  (escopos `openid`, `profile`, `w_member_social`) e substitua o arquivo.
- **Teste rápido do token:** `python .claude/skills/li-publish/publish.py whoami`
- **Atualizar o repositório:** `git pull` na pasta.

## O que fica de fora, de propósito

Comentar, curtir, mandar DM e aceitar convites continuam manuais. Automatizar
isso pelo navegador viola os termos do LinkedIn e pode restringir a conta.
Agendamento também não existe na API para perfil pessoal: para postar mais
tarde, rode a `/li-publish` na hora desejada.
