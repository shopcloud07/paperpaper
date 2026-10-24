# Regras deste projeto

## Rastreamento: nunca no HTML

Esta página usa o módulo `app-init.js` (o dono chama de **Bloco Pixel Limpo**).

**Nenhuma tag de rastreamento pode ser colocada no HTML. Nunca.**

Isso vale para Meta Pixel, UTMify, UTMs, Microsoft Clarity, Google Analytics,
TikTok Pixel, GTM — qualquer coisa que rastreie.

Tudo entra pelo objeto `CFG`, no topo do `app-init.js`.

### Por quê

A página original deste dono foi clonada por terceiros. O pixel estava em texto
puro no `<head>`, então ia junto na cópia: os clones disparavam PageView e
InitiateCheckout na conta de anúncios dele, a Meta leu aquilo como evento
duplicado e derrubou a entrega. As vendas caíram por causa disso.

Colar uma tag no `<head>` recria exatamente o problema que este módulo existe
para resolver. Uma única tag solta anula a proteção inteira.

### Como o módulo funciona

- `CFG.envs` lista os domínios de produção. Fora deles, **nada** é carregado.
- O ID do pixel fica cifrado (valor começando com `~`), usando o **domínio em
  execução** como chave. A chave não existe guardada no arquivo.
- Resultado: mesmo que alguém clone a página e apague a verificação de domínio,
  o ID não decifra e o pixel não inicializa.

### Quando o dono pedir "instala o pixel"

1. Ele vai mandar o código que a UTMify devolveu (ou só o ID)
2. Extraia o ID. A UTMify tem dois formatos:
   - **antigo**: `window.pixelId = "..."` legível
   - **novo**: carregador codificado — `atob("...")` → base64 → primeiro byte é o
     tamanho da chave, seguem a chave e o payload em XOR → JSON com `url`,
     `attributes` e `globals` (o `pixelId` está nos globals)
3. Cifre com o domínio de produção e coloque em `CFG.utmify.pixel`.
   Se o JSON trouxer `url`/`attributes`, grave em `CFG.utmify.src` e `CFG.utmify.attrs`
4. **Não cole o snippet cru em lugar nenhum**

> A codificação da UTMify não protege contra clone — a chave vai junto no blob.
> Quem prende o pixel ao domínio é este módulo.

Jeito mais fácil: abra o `gerador.html` do kit, preencha e ele monta o arquivo
pronto. Ele também roda um autoteste da cifra.

### Ao editar o app-init.js

- Mexa **só** no bloco `CFG` (topo do arquivo). O corpo é igual em todas as páginas.
- Nunca use coringa em hospedagem compartilhada (`*.vercel.app` autoriza o
  Vercel inteiro — é lá que o clonador hospeda de graça).
- Preview e `localhost` não carregam nada com `debug: false`. É proposital.
- Nunca publique com `debug: true`.
- O arquivo publicado tem nomes neutros de propósito. **Não** adicione comentários
  do tipo "anti-clone", "bloqueio" ou "proteção" — isso entrega o mapa para quem
  abrir o código.

### Arquivos do kit

| Arquivo | Publica? |
|---|---|
| `app-init.js` | sim |
| `gerador.html` | **não** |
| `COFRE-LEIA-ME.md` | **não** |
| `CLAUDE.md` | **não** |

Só o `app-init.js` vai para o ar. O resto é ferramenta interna — se subir junto,
o clonador lê o manual da proteção.
