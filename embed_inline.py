import base64
import os
import re

# Paths
HTML_FILE = "index.html"
CSS_FILES = ["css/53144c68c6dcd13a.css", "css/ccd75821ad024a8c.css"]
FONTS_DIR = "fonts"

print("Lendo arquivos de CSS...")
combined_css = ""

for css_path in CSS_FILES:
    if not os.path.exists(css_path):
        print(f"AVISO: {css_path} nao encontrado, pulando.")
        continue
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Encontrar todas as referências de fontes (../fonts/xxx.woff2)
    font_refs = re.findall(r'url\(\.\./fonts/([^)]+\.woff2)\)', css_content)
    print(f"  {css_path}: encontradas {len(font_refs)} referencias de fontes")

    for font_filename in font_refs:
        font_path = os.path.join(FONTS_DIR, font_filename)
        if os.path.exists(font_path):
            with open(font_path, "rb") as ff:
                font_b64 = base64.b64encode(ff.read()).decode("utf-8")
            data_uri = f"data:font/woff2;base64,{font_b64}"
            css_content = css_content.replace(
                f"url(../fonts/{font_filename})",
                f"url({data_uri})"
            )
            print(f"    Embutida fonte: {font_filename}")
        else:
            print(f"    AVISO: Fonte nao encontrada: {font_path}")

    combined_css += css_content + "\n"

print("\nLendo index.html...")
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Remover as tags <link rel="stylesheet"> que apontam para css/
html = re.sub(
    r'<link rel="stylesheet" href="css/[^"]*"[^/]*/?>',
    "",
    html
)

# Embutir o CSS combinado como <style> logo antes do </head>
inline_style_tag = f"<style>\n{combined_css}\n</style>"

if "</head>" in html:
    html = html.replace("</head>", inline_style_tag + "\n</head>")
    print("CSS embutido antes de </head>")
elif "<body" in html:
    html = html.replace("<body", inline_style_tag + "\n<body")
    print("CSS embutido antes de <body> (fallback)")

print("\nSalvando index.html atualizado...")
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\nPronto! O index.html agora e 100% autocontido (CSS + fontes embutidos).")
print(f"Tamanho final do HTML: {os.path.getsize(HTML_FILE) / 1024:.1f} KB")
