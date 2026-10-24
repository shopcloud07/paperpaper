# Não está funcionando? Descubra o porquê

## Jeito rápido (se o módulo já é a versão nova)

Abra a página no ar com `?__chk=1` no fim da URL:

```
https://seudominio.vercel.app/?__chk=1
```

Aperte **F12** → aba **Console**. Vai aparecer um relatório dizendo exatamente
o que está bloqueando.

Sem o `?__chk=1` o módulo é mudo — não vaza nada para quem abrir o console.

---

## Jeito que funciona sempre

Abra a página no ar, **F12** → **Console**, cole isto e aperte Enter:

```js
(async()=>{var h=location.hostname,S=[...document.scripts],t=S.find(s=>/app-init\.js/i.test(s.src||'')),f=null,e='-',p='-';try{var r=await fetch('app-init.js',{cache:'no-store'});if(r.ok)f=await r.text();}catch(x){}if(f){var m=f.match(/envs:\s*\[([\s\S]*?)\]/);e=m?m[1].replace(/\s+/g,' ').trim():'?';var q=f.match(/pixel:\s*('[^']*'|\[[^\]]*\])/);p=q?(q[1]==="''"?'VAZIO':'preenchido'):'?';}console.log(['','=== DIAGNOSTICO ===','1 dominio atual    : '+h,'2 tag no HTML      : '+(t?'SIM  '+t.src:'NAO ENCONTRADA'),'3 arquivo baixou   : '+(f?'SIM ('+f.length+' bytes)':'NAO - 404 ou caminho errado'),'4 dominios no arq. : '+e,'5 pixel no arquivo : '+p,'6 modulo rodou     : '+(window.__appInit?'SIM':'NAO'),'7 window.pixelId   : '+(window.pixelId||'nao definido'),'8 scripts utmify   : '+S.filter(s=>/utmify/.test(s.src||'')).length,'9 tag antiga solta : '+(/window\.pixelId\s*=/.test(document.documentElement.outerHTML)?'SIM (ainda no HTML)':'nao')].join('\n'));})()
```

> O Chrome pode pedir para você digitar `allow pasting` antes de deixar colar.
> Digite, aperte Enter e cole de novo.

---

## Como ler o resultado

| Linha | Se aparecer isso | O problema é |
|---|---|---|
| **2** | `NAO ENCONTRADA` | a linha `<script src="app-init.js"></script>` não está no HTML |
| **3** | `NAO - 404` | o arquivo não está na raiz, ou o nome está errado (`app-init (1).js`) |
| **4** | `'SEU-DOMINIO-AQUI.com'` | você usou o modelo do kit em vez do arquivo gerado |
| **4** | um domínio diferente do da linha 1 | o arquivo foi gerado para outro domínio |
| **5** | `VAZIO` | o arquivo foi gerado sem o pixel |
| **6** | `NAO` | o arquivo não carregou (veja linhas 2 e 3) |
| **7** | `nao definido` com a 6 em `SIM` | a cifra não abriu neste domínio — gere de novo com o domínio certo |
| **9** | `SIM` | sobrou tag antiga no HTML — tem que apagar, senão continua vazando |

### A causa mais comum

Linha 1 e linha 4 **diferentes**.

O módulo só funciona no domínio exato para o qual foi gerado. Se você gerou para
`minhapagina.vercel.app` mas a Vercel publicou em `minhapagina-abc123.vercel.app`,
a trava bloqueia tudo — pixel, Clarity e também a injeção de UTM no checkout.

**Solução:** copie o domínio exato que está na barra do navegador, gere o arquivo
de novo com ele e substitua.

> Confira o domínio **depois** de publicar, não antes. A Vercel às vezes dá uma
> URL diferente da que você imaginou.

---

## Se a UTM não chega no checkout

A injeção de UTM está **dentro** da trava. Se o domínio não bate, ela também não
roda — por isso "não funciona nada" costuma ser um problema só: o domínio.

Se o domínio estiver certo e mesmo assim a UTM não passar, confira a linha dos
`checkouts` no relatório do `?__chk=1`: o domínio do seu botão de compra precisa
estar nessa lista, e é o **domínio**, não o link inteiro.

| Link do botão | O que vai na lista |
|---|---|
| `https://tilimcheckout.com/checkout/abc` | `tilimcheckout.com` |
