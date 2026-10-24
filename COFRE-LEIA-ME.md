# BLOCO PIXEL LIMPO — manual do cofre

> **Este arquivo NÃO vai publicado.** Ele fica só na sua pasta de cofre.
> Se ele subir junto com a página, o clonador lê aqui exatamente o que precisa apagar.

O módulo publicado se chama `app-init.js` e tem cara de arquivo técnico chato de propósito.
Em nenhum lugar dentro dele aparece a palavra pixel-limpo, bloqueio, clone ou proteção.

---

## A REGRA ÚNICA

**Nenhuma tag de rastreamento pode existir no HTML. Nunca.**

Pixel, UTM, Clarity, GA, TikTok — tudo entra pelo `CFG` no topo do `app-init.js`.

Isso vale para:

- pedidos a qualquer IA ("instala o pixel nessa página") → é dentro do bloco, não no `<head>`
- o campo "cole seu pixel aqui" de Vercel, Orchids, Elementor, WordPress → **não usar**
- qualquer snippet que a UTMify, a Meta ou o checkout te entregarem → passa pelo bloco

Uma única tag solta no HTML derruba a proteção inteira.

---

## COMO INSTALAR EM UMA PÁGINA NOVA

**O arquivo `app-init.js` é sempre o mesmo, byte por byte, em todas as páginas.**
Nunca edite o corpo dele. O que muda de página para página são 3 linhas do `CFG`.

1. Copie `app-init.js` para a pasta da página **sem alterar nada**
2. No HTML, logo no começo do `<head>`, coloque **uma linha**:
   ```html
   <script src="app-init.js"></script>
   ```
3. Edite **só estas 3 chaves** no `CFG`:

   ```js
   envs:      ['colandoemontando3d.vercel.app'],   // o domínio DESTA página
   checkouts: ['tilimcheckout.com'],               // o checkout DESTA oferta
   utmify: { utms: true, pixel: '~...' }           // o pixel DESTA página, cifrado
   ```

4. Confira que não sobrou nenhuma tag de tracking solta no HTML

### Regras da lista `envs`

- Liste **domínios exatos**. Um por linha.
- O coringa `*` cobre um único rótulo e serve só para **subdomínio seu**:
  `'*.seudominio.com.br'` libera `loja.seudominio.com.br`.
- **Nunca** use coringa em hospedagem compartilhada. `'*.vercel.app'` autoriza
  o Vercel inteiro — e é exatamente lá que o clonador sobe a cópia de graça.
- `www.` é ignorado automaticamente: `seudominio.com` já cobre `www.seudominio.com`.
- Preview do Vercel **não** entra na lista. Preview não precisa de tracking.

### Ambientes de desenvolvimento

`localhost` e `127.0.0.1` ficam em `devEnvs` e **só funcionam com `debug: true`**.
Em produção eles estão mortos — um clonador rodando o arquivo na máquina dele
não dispara nada.

---

## COMO INSTALAR O PIXEL (o fluxo da UTMify)

```
Meta Ads → cria o Pixel → pega o número
   ↓
UTMify → cola o número lá → ela devolve um código
   ↓
esse código vai para o CFG do app-init.js — NUNCA para o <head>
```

Do código que a UTMify devolve, o que importa é o ID que aparece em
`window.pixelId = "..."`. Esse ID **não entra em texto puro**: ele é cifrado
com o domínio de produção como chave.

### Gerando o valor cifrado

1. No `app-init.js`, mude `debug: false` para `debug: true`
2. Publique e abra a página **no domínio de produção real**
3. No console do navegador:
   ```js
   __ai.pack('COLE_AQUI_O_ID_DA_UTMIFY')
   ```
4. Copie a saída (começa com `~`) e cole em `utmify.pixel`
5. **Volte `debug` para `false`** e publique de novo

> A chave é sempre o domínio em execução — ela não fica guardada no arquivo.
> Por isso o valor cifrado só abre no domínio para o qual foi gerado.

### Mais de um domínio de produção

```js
pixel: ['~valorDoDominioA', '~valorDoDominioB']
```

O módulo testa cada um com o host atual e usa o que abrir.

---

## O QUE ACONTECE EM CADA AMBIENTE

| Onde | Resultado |
|---|---|
| Domínio de produção (com ou sem `www`) | carrega tudo |
| Preview do Vercel | **nada** |
| `localhost` com `debug: false` | **nada** |
| `localhost` com `debug: true` | UTM e Clarity sim, **pixel não** (a cifra não abre fora de produção) |
| Domínio de clone, qualquer hospedagem | **nada** |
| Clone em `.vercel.app` com nome parecido | **nada** |
| Domínio disfarçado (`seudominio.com.evil.com`) | **nada** |
| Página dentro de iframe de outro site | **nada** |
| Clone que apagou a verificação de domínio | scripts sobem, mas o **ID não decifra** — o pixel não inicializa |

13 cenários testados, todos passando. O último é o que mais importa:
**apagar a trava não devolve o ID.**

---

## LIMITES — o que isso NÃO resolve

1. **Nada client-side é 100%.** Quem entende de código e tiver paciência pode
   abrir sua página real, ler o ID já decifrado na memória e fixar no clone dele.
   O objetivo aqui é matar o clonador automático e o preguiçoso — a esmagadora maioria.

2. **O fecho de verdade é o Nível 3.** Preencha `remote: '/api/config'` e crie
   essa função na Vercel validando o header `Origin`. O ID sai do arquivo e passa
   a morar no servidor. Clone recebe `403` e fica sem nada.

3. **Seu pixel atual já vazou.** O ID `69577d17e88d9ea6945100bb` já está dentro
   dos clones que estão no ar agora. A trava protege daqui pra frente — os clones
   antigos continuam disparando. **Tem que criar pixel novo.**

4. **Fora do código, vale mais que qualquer JS:**
   - Meta Events Manager → configurações do pixel → permissões de tráfego / domínios permitidos
   - Painel da UTMify → restrição de domínio, se houver
   - CAPI server-side com `event_id` → evento de verdade sai do servidor, clone não forja

---

## DIAGNÓSTICO

Com `debug: true`, o console mostra:

```
[init] ambiente ok: seudominio.com
[init] utmify utms ok
[init] utmify pixel ok
[init] clarity ok
[init] atribuicao ok {...}
```

Se aparecer `ambiente nao autorizado`, o domínio não está em `envs`.
Se aparecer `utmify pixel: nao configurado`, a cifra não abriu nesse domínio.

**Nunca publique com `debug: true`.**
