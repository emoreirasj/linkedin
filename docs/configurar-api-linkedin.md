# Configurar a API do LinkedIn para a `/li-publish`

Leva uns 15 minutos e só precisa ser feito uma vez. Depois, a cada 60 dias, você
repete o passo 5 para gerar um token novo.

Os posts saem no seu **perfil pessoal**, com o seu nome. A Página de empresa do
passo 1 serve só para registrar o app; nada é postado nela.

## 1. Ter uma Página do LinkedIn

O LinkedIn exige que todo app de desenvolvedor esteja ligado a uma Página.

- Se você já administra alguma Página, use essa.
- Se não, crie uma em <https://www.linkedin.com/company/setup/new/>. Pode ser
  uma página simples com o seu nome ou da sua marca pessoal.

## 2. Criar o app

1. Entre em <https://www.linkedin.com/developers/apps> e clique em **Create app**.
2. Preencha:
   - **App name**: algo como `Claude LinkedIn Edson`
   - **LinkedIn Page**: a Página do passo 1
   - **App logo**: qualquer imagem quadrada
3. Aceite os termos e clique em **Create app**.

## 3. Verificar o app na Página

1. No app, abra a aba **Settings** e clique em **Verify** ao lado da Página.
2. Clique em **Generate URL**, abra o link (logado como administrador da Página)
   e confirme.

## 4. Ativar os produtos

Na aba **Products**, clique em **Request access** em:

- **Share on LinkedIn** (dá a permissão `w_member_social`, para publicar)
- **Sign In with LinkedIn using OpenID Connect** (dá `openid` e `profile`, para
  o script descobrir o seu ID de membro)

Os dois costumam ser liberados na hora. Confira na aba **Auth**, em
**OAuth 2.0 scopes**, se aparecem `openid`, `profile` e `w_member_social`.

## 5. Gerar o token de acesso

1. Abra o gerador oficial: <https://www.linkedin.com/developers/tools/oauth/token-generator>
2. Escolha o seu app.
3. Marque os escopos `openid`, `profile` e `w_member_social`.
4. Clique em **Request access token** e autorize com a sua conta pessoal.
5. Copie o **Access token**. Ele vale 60 dias.

Trate esse token como uma senha: quem tiver ele consegue publicar em seu nome.
Não cole em chat, e-mail ou commit.

## 6. Guardar o token no seu computador

No terminal, no computador onde você usa o Claude Code:

```bash
mkdir -p ~/.claude/linkedin
nano ~/.claude/linkedin/token     # cole o token, salve e feche
chmod 600 ~/.claude/linkedin/token
```

Se preferir variável de ambiente, use `export LINKEDIN_ACCESS_TOKEN=...`; ela tem
prioridade sobre o arquivo. O arquivo fica fora do repositório, então não vai
para o GitHub.

## 7. Testar

Na pasta deste repositório:

```bash
python3 .claude/skills/li-publish/publish.py whoami
```

Deve aparecer o seu nome e um `urn:li:person:...`. Se aparecer erro 401, o token
está errado ou venceu; 403 indica que falta um dos escopos do passo 4.

## 8. Usar

No Claude Code, dentro deste repositório:

1. `/li-post <sua ideia>` para escrever o post.
2. Ajuste até ficar bom.
3. `/li-publish`. O Claude mostra o texto final e pergunta se pode publicar.
   Nada sai sem você responder **sim**.

Para testar sem expor nada, o script tem um modo de pré-visualização que não
envia nada:

```bash
python3 .claude/skills/li-publish/publish.py post rascunho.txt
```

Só com `--yes` no final ele publica de verdade.

## Quando o token vencer

A cada 60 dias a `/li-publish` vai dar erro 401. Repita o passo 5 e substitua o
conteúdo de `~/.claude/linkedin/token`.

## Limites

- Até 3.000 caracteres por post.
- Só texto por enquanto (sem imagem, PDF ou carrossel).
- Hashtags saem como texto (`#tema`), mas podem não virar link clicável.
- O LinkedIn limita 150 chamadas por dia por membro, bem acima do que você vai usar.
- A API não agenda posts em perfil pessoal. Para postar mais tarde, rode a
  `/li-publish` na hora desejada.
