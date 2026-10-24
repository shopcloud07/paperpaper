# Página nova — passo a passo

Copie **esta pasta inteira** para dentro de qualquer projeto novo. Ela carrega
tudo que é preciso saber — você não precisa lembrar de nada.

---

## ANTES: existem DOIS arquivos `app-init.js`

É a confusão mais comum. Eles são diferentes e ficam em lugares diferentes:

| Qual | Onde fica | Preenchido? | Vai pro ar? |
|---|---|---|---|
| **O modelo** | `bloco-pixel-limpo/app-init.js` | não, fica em branco pra sempre | **não** |
| **O seu** | na raiz, ao lado do `index.html` | sim, com seu domínio e pixel | **sim** |

**Você nunca substitui o modelo.** Ele fica em branco pra você reusar nas
próximas páginas. O arquivo que você baixa do gerador vai pra **raiz da página**.

---

## OS 7 PASSOS

### 1. Faça a página normalmente
Sem pixel, sem UTMify, sem Clarity, sem nada de rastreamento no HTML.

### 2. Copie o kit para dentro do projeto
A pasta `bloco-pixel-limpo/` inteira.

### 3. Copie 3 arquivos do kit para a RAIZ do projeto

| Arquivo | Para quê |
|---|---|
| `CLAUDE.md` | faz qualquer IA em pasta nova já saber as regras |
| `.gitignore` | impede o kit de chegar ao **GitHub** |
| `.vercelignore` | impede o kit de chegar ao **site** |

### 4. Descubra o domínio REAL
Publique a página primeiro, do jeito que estiver, e **copie o domínio exato da
barra do navegador**.

> A Vercel às vezes publica numa URL diferente da que você imaginou. Se você
> gerar o arquivo com o domínio errado, a trava bloqueia tudo — pixel, Clarity
> e UTM.

### 5. Gere o arquivo
Abra o `gerador.html` (duplo clique, funciona offline) e preencha:

- **Domínio** — o exato do passo 4
- **Pixel da UTMify** — cole o código inteiro, sem editar (funciona no formato
  novo codificado e no antigo)
- **Clarity** — opcional, pode colar o script inteiro
- **Checkouts** — um domínio por linha (só o domínio, não o link)

Clique em **Gerar arquivo**.

### 6. Os DOIS passos que o gerador mostra

**Passo 1 — cole a linha no `<head>` do HTML**

```html
<script src="app-init.js"></script>
```

Tem que ser a primeira coisa dentro do `<head>`:

```html
<head><script src="app-init.js"></script>
  <meta charset="utf-8">
  ...
```

> **Este é o passo que mais se esquece — e sem ele NADA funciona.**
> O arquivo fica parado na pasta e ninguém manda ele rodar. Sem pixel, sem
> Clarity, sem UTM no checkout. Já aconteceu duas vezes.

**Passo 2 — baixe o `app-init.js`**

Ele cai na pasta **Downloads**. Recorte e cole na **raiz da página**, ao lado
do `index.html`.

> Se você baixar duas vezes, o Windows salva como `app-init (1).js`.
> Renomeie para `app-init.js` exato, senão a página não acha o arquivo.

### 7. Publique e confirme

Abra a página no ar com `?__chk=1` no fim da URL:

```
https://seudominio.vercel.app/?__chk=1
```

**F12 → Console.** Tem que aparecer:

```
host na lista    : SIM
fora de iframe   : SIM
pixel abre aqui  : SIM
```

Se aparecer `NAO` em alguma linha, veja o `DIAGNOSTICO.md`.

Sem o `?__chk=1` o módulo é mudo — não entrega nada pra quem abrir o console.

---

## CONFERÊNCIA FINAL

| Teste | Esperado |
|---|---|
| **Ctrl+U** e procurar o número do seu pixel | **não aparece** |
| Console: `window.pixelId` | mostra o ID |
| Console: `fbq` | uma função |
| Meta Pixel Helper | mostra o pixel |
| Clicar no botão de compra | UTMs na URL do checkout |

---

## SE PUBLICAR VIA GITHUB

**O repositório precisa ser PRIVADO.** Num repositório público qualquer pessoa
dá `git clone` e leva sua página inteira, e ainda lê o `COFRE-LEIA-ME.md`, que
explica como desarmar a proteção.

Ao criar: marque **Private**. Já criou público? Settings → General → Danger Zone
→ Change visibility.

Repositório privado **não** tira o site do ar. A Vercel lê o código privado e
publica numa URL pública. Código fechado, site aberto.

---

## A REGRA QUE NÃO PODE SER QUEBRADA

**Nenhuma tag de rastreamento no HTML. Nunca.** Tudo entra pelo gerador.

Isso inclui o campo "cole seu pixel aqui" de Vercel, Orchids, Elementor e
WordPress — não use, ele injeta a tag crua e derruba a proteção inteira.

---

## REAPROVEITANDO EM OUTRAS PÁGINAS

Copie o kit **sempre da pasta original**, nunca de uma cópia antiga.

Como saber se um `app-init.js` está atualizado: abra e procure por `__chk`.
**Não achou = versão antiga**, com a cifra fraca. Regenere pelo gerador atual.

---

## OS ARQUIVOS

| Arquivo | Para quê | Vai publicado? |
|---|---|---|
| `app-init.js` (raiz) | o módulo preenchido | **sim** |
| `app-init.js` (kit) | modelo em branco | não |
| `gerador.html` | monta o arquivo de cada página | não |
| `CLAUDE.md` | ensina as regras a qualquer IA | não |
| `.gitignore` / `.vercelignore` | impedem o kit de vazar | não |
| `COFRE-LEIA-ME.md` | manual completo e limites | não |
| `DIAGNOSTICO.md` | o que fazer quando não funciona | não |
| `COMECE-AQUI.md` | este arquivo | não |

**Só o `app-init.js` da raiz vai para o ar.**
