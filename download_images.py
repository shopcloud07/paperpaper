import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

if not os.path.exists("images"):
    os.makedirs("images")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r'https://i\.ibb\.co/[^"\'\s\?)]+'
urls = set(re.findall(pattern, html))

print(f"Encontradas {len(urls)} URLs unicas do ibb.co no HTML.")

success_count = 0
for url in urls:
    filename = url.split('/')[-1]
    local_path = os.path.join("images", filename)
    
    if not os.path.exists(local_path):
        print(f"Baixando {filename}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
            success_count += 1
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
    else:
        success_count += 1

    # Substituir no HTML pela rota relativa
    # Lidando com possiveis encodings ou escapes no HTML nao e necessario, pois extraimos a URL limpa.
    # Porem as URLs no HTML podem estar exatas.
    html = html.replace(url, f"images/{filename}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Sucesso: {success_count} de {len(urls)} imagens.")
print("HTML atualizado com caminhos locais!")
