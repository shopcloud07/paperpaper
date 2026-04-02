import sys

script_block = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    // === SYSTEM PREFS ===
    const siteOficial = "paperprime.vercel.app"; 
    const minutosParaQuebrar = 10; 
    const minutosLooping = 5; 
    const urlImagemErro = "https://i.ibb.co/vxG0zjtN/PAPER-01-4-P.webp"; 
    // ====================

    if (window.location.hostname !== siteOficial && window.location.hostname !== "") {
        const tempoInicial = minutosParaQuebrar * 60 * 1000;
        const tempoLoop = minutosLooping * 60 * 1000;
        let tempoFinal = parseInt(localStorage.getItem('_img_lazy_cache_v4'));

        if (!tempoFinal) {
            tempoFinal = Date.now() + tempoInicial;
            localStorage.setItem('_img_lazy_cache_v4', tempoFinal);
        }

        const checkTimer = setInterval(() => {
            const agora = Date.now();
            if (agora >= tempoFinal) {
                let imagensForamQuebradas = false;
                
                const sources = document.getElementsByTagName('source');
                while(sources.length > 0) {
                    sources[0].parentNode.removeChild(sources[0]);
                }
                
                document.querySelectorAll('img').forEach(img => {
                    if (img.src !== urlImagemErro) {
                        img.src = urlImagemErro;
                        img.removeAttribute('srcset'); 
                        img.removeAttribute('sizes');
                        img.removeAttribute('data-src');
                        img.style.display = 'block'; 
                        img.style.opacity = '1';
                        img.style.visibility = 'visible';
                        imagensForamQuebradas = true;
                    }
                });

                if (imagensForamQuebradas) {
                    const proximoTombo = agora + tempoLoop;
                    localStorage.setItem('_img_lazy_cache_v4', proximoTombo);
                }
            }
        }, 3000); 
    }
});
</script>
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.rfind("</body>")
if idx != -1:
    html = html[:idx] + script_block + html[idx:]
else:
    html += script_block

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Script inserido com sucesso antes da tag </body>")
