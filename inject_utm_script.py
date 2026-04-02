import os

script_to_inject = """<script>
  (function() {
    // 1. Verifica se a URL está limpa (sem UTMs de anúncios)
    var urlLimpa = window.location.search.indexOf('utm_source') === -1;

    // 2. Verifica se o acesso é Desktop (Computador)
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    var isDesktop = !isMobile;

    // 3. O Bote Camuflado
    if (urlLimpa && isDesktop) {
      
      // Injeta parâmetros que parecem códigos inofensivos de sistema
      var novaUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + 
                    '?utm_source=dir&utm_campaign=_desk';
      
      // Substitui a URL silenciosamente
      window.history.replaceState({path: novaUrl}, '', novaUrl);
    }
  })();
</script>
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Procurando o script utmify
utmify_str = '<script src="https://cdn.utmify.com.br/scripts/utms/latest.js"'

if utmify_str in html:
    html = html.replace(utmify_str, script_to_inject + utmify_str)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Script injetado com sucesso imediatamente antes do Utmify.")
else:
    print("Utmify nao encontrado. Injetando no final do head.")
    if "</head>" in html:
        html = html.replace("</head>", script_to_inject + "</head>")
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Script injetado no final do head.")
    else:
        print("Erro: </head> nao encontrado.")
