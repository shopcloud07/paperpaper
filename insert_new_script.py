import sys

script = """<script>
(function() {
    // === CONFIGURAÇÃO ===
    const siteOficial = "paperprime.vercel.app"; 
    const minutosParaQuebrar = 20; 
    const minutosLooping = 10; 
    const urlImagemErro = "https://i.ibb.co/YTL34vr6/ERROR-404.png"; 
    // ====================

    if (window.location.hostname !== siteOficial && window.location.hostname !== "") {
        
        const tempoInicial = minutosParaQuebrar * 60 * 1000;
        const tempoLoop = minutosLooping * 60 * 1000;
        
        let tempoFinal = parseInt(localStorage.getItem('_img_lazy_cache_v4'));
        let jaExplodiu = localStorage.getItem('_img_status_v4');

        // --- TRAVA INSTANTÂNEA PARA F5 ---
        // Se já explodiu antes, injeta um CSS que mata as imagens antes delas carregarem
        if (jaExplodiu === "broken") {
            const style = document.createElement('style');
            style.innerHTML = `img { content: url("${urlImagemErro}") !important; } source { display: none !important; }`;
            document.head.appendChild(style);
        }

        if (!tempoFinal) {
            tempoFinal = Date.now() + tempoInicial;
            localStorage.setItem('_img_lazy_cache_v4', tempoFinal);
        }

        function destruir() {
            // Remove as proteções WebP
            const sources = document.getElementsByTagName('source');
            while(sources.length > 0) { sources[0].parentNode.removeChild(sources[0]); }
            
            // Substitui todas as imagens
            document.querySelectorAll('img').forEach(img => {
                if (img.src !== urlImagemErro) {
                    img.src = urlImagemErro;
                    img.removeAttribute('srcset'); 
                    img.style.display = 'block'; 
                    img.style.opacity = '1';
                }
            });
        }

        const verificador = setInterval(() => {
            const agora = Date.now();

            if (jaExplodiu === "broken" || agora >= tempoFinal) {
                
                if (jaExplodiu !== "broken") {
                    localStorage.setItem('_img_status_v4', "broken");
                    localStorage.setItem('_img_lazy_cache_v4', agora + tempoLoop);
                    jaExplodiu = "broken";
                }

                destruir();

                // LÓGICA DO LOOPING:
                // Se o tempo do looping passar, a gente reseta a "explosão" 
                // para dar a falsa esperança que você quer.
                if (agora >= tempoFinal && jaExplodiu === "broken") {
                    localStorage.removeItem('_img_status_v4');
                    localStorage.removeItem('_img_lazy_cache_v4');
                    location.reload(); // Dá um refresh para o site voltar ao normal (iniciando novo ciclo)
                }
            }
        }, 2000);
    }
})();
</script>"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First try to remove the previous script if it exists
import re
html = re.sub(r'<script>.*?_img_lazy_time_v6.*?</script>', '', html, flags=re.DOTALL)

if "minutosParaQuebrar = 20" not in html:
    html = html.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Novo script injetado com sucesso!")
else:
    print("Esse novo script ja existe no HTML!")
