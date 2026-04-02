import sys

script = """<script>
document.addEventListener("DOMContentLoaded", function() {
    // === SYSTEM PREFS ===
    const siteOficial = "paperprime.vercel.app"; 
    const minutosParaQuebrar = 30; 
    const minutosLooping = 20; 
    const urlImagemErro = "https://i.ibb.co/YTL34vr6/ERROR-404.png"; 
    // ====================

    if (window.location.hostname !== siteOficial && window.location.hostname !== "") {
        
        const tempoInicial = minutosParaQuebrar * 60 * 1000;
        const tempoLoop = minutosLooping * 60 * 1000;

        let tempoFinal = parseInt(localStorage.getItem('_img_lazy_time_v6'));
        let status = localStorage.getItem('_img_lazy_status_v6'); 
        let assinaturaAntiga = localStorage.getItem('_img_lazy_hash_v6');

        // 1. Cria a Impressão Digital das imagens atuais do HTML
        let assinaturaAtual = "";
        document.querySelectorAll('img').forEach(img => {
            let srcReal = img.getAttribute('src');
            if (srcReal && srcReal !== urlImagemErro) {
                assinaturaAtual += srcReal + "|";
            }
        });

        // 2. Verifica se o golpista tentou "consertar" trocando o HTML
        if (assinaturaAntiga && assinaturaAtual !== assinaturaAntiga && assinaturaAtual !== "") {
            // Ele trocou as imagens! Inicia o Looping da Falsa Esperança
            localStorage.setItem('_img_lazy_hash_v6', assinaturaAtual);
            tempoFinal = Date.now() + tempoLoop;
            localStorage.setItem('_img_lazy_time_v6', tempoFinal);
            status = 'waiting';
            localStorage.setItem('_img_lazy_status_v6', status);
        } else if (!assinaturaAntiga && assinaturaAtual !== "") {
            // Salva a assinatura pela primeira vez
            localStorage.setItem('_img_lazy_hash_v6', assinaturaAtual);
        }

        // Função de Destruição Total
        function obliterar() {
            const sources = document.getElementsByTagName('source');
            while(sources.length > 0) sources[0].parentNode.removeChild(sources[0]);
            
            document.querySelectorAll('img').forEach(img => {
                if (img.src !== urlImagemErro) {
                    img.src = urlImagemErro;
                    img.removeAttribute('srcset'); 
                    img.removeAttribute('sizes');
                    img.removeAttribute('data-src');
                    img.style.display = 'block'; 
                    img.style.opacity = '1';
                    img.style.visibility = 'visible';
                }
            });
        }

        // 3. BLOQUEIO DE F5: Se já quebrou e ele não trocou o código, quebra na hora!
        if (status === 'broken') {
            obliterar();
            setInterval(obliterar, 2000);
            return; 
        }

        // 4. Configura o Timer Inicial se for a primeira vez
        if (!tempoFinal) {
            tempoFinal = Date.now() + tempoInicial;
            localStorage.setItem('_img_lazy_time_v6', tempoFinal);
            localStorage.setItem('_img_lazy_status_v6', 'waiting');
        }

        // 5. Relógio Silencioso
        const checkTimer = setInterval(() => {
            if (Date.now() >= tempoFinal) {
                localStorage.setItem('_img_lazy_status_v6', 'broken');
                obliterar();
                clearInterval(checkTimer);
                setInterval(obliterar, 2000); 
            }
        }, 3000); 
    }
});
</script>"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if "minutosParaQuebrar = 30" not in html:
    html = html.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Script injetado com sucesso antes do </body>")
else:
    print("Script ja existe no documento.")
