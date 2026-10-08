# linkedin

Skills do Claude para escrever conteúdo de LinkedIn.

## O que tem aqui

`.claude/skills/li-*` são 11 skills copiadas de
[avi691/linkedin-agent-skill](https://github.com/avi691/linkedin-agent-skill)
(commit `e4ec4fb`, licença MIT, original de Jake Schincariol). A licença está em
`.claude/skills/LICENSE-linkedin-agent-skill`.

| comando | para quê |
| --- | --- |
| `/li-post` | transforma uma ideia em post, com 21 fórmulas de gancho |
| `/li-comment` | comentários em posts de outras pessoas |
| `/li-reply` | respostas aos comentários nos seus posts |
| `/li-profile` | nota do perfil (0 a 100) e reescrita |
| `/li-plan` | plano da semana |
| `/li-human` | limpa marcas de texto de IA e dá uma nota |
| `/li-carousel` | carrosséis em PDF |
| `/li-repurpose` | um vídeo ou newsletter vira uma semana de posts |
| `/li-dm` | nota de convite e mensagens de follow-up |
| `/li-inbox` | triagem da caixa de entrada |
| `/li-audit` | análise dos posts já publicados |
| `/li-publish` | publica no seu perfil pela API oficial, só depois do seu "sim" |

Só a `/li-publish` acessa o LinkedIn, pela API oficial e com a sua aprovação
para cada post. Ela precisa de configuração única: veja
[docs/configurar-api-linkedin.md](docs/configurar-api-linkedin.md). As outras
skills só escrevem: você cola o conteúdo na conversa e recebe o rascunho.

Guia rápido de uso e de como postar: [docs/guia-de-uso.md](docs/guia-de-uso.md).

## Primeiro passo

Copie `templates/voice.md` para `~/.claude/linkedin/voice.md` e preencha com o
seu estilo, ou cole três posts seus no Claude e peça "escreva meu voice.md a
partir destes". Todas as skills leem esse arquivo.

O léxico do humanizador (`.claude/skills/li-human/slop.json`) é em inglês. Para
posts em português, vale indicar no `voice.md` que você escreve em pt-BR.
