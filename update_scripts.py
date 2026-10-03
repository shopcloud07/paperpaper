import re

html_file = 'index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_pixel = """<script>
  window.pixelId = "69577d17e88d9ea6945100bb";
  var a = document.createElement("script");
  a.setAttribute("async", "");
  a.setAttribute("defer", "");
  a.setAttribute("src", "https://cdn.utmify.com.br/scripts/pixel/pixel.js");
  document.head.appendChild(a);
</script>"""

new_utm = """<script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-xcod-sck data-utmify-prevent-subids async defer></script>"""

# Replace pixel
pixel_pattern = re.compile(r'<script>\s*window\.pixelId\s*=\s*"[^"]+";\s*var\s*a\s*=\s*document\.createElement\("script"\);\s*a\.setAttribute\("async"\s*,\s*""\);\s*a\.setAttribute\("defer"\s*,\s*""\);\s*a\.setAttribute\("src"\s*,\s*"https://cdn\.utmify\.com\.br/scripts/pixel/pixel\.js"\);\s*document\.head\.appendChild\(a\);\s*</script>', re.DOTALL)
if pixel_pattern.search(content):
    content = pixel_pattern.sub(new_pixel, content)
    print("Pixel substituido.")
else:
    print("Pixel antigo não encontrado com RegExp exata! Buscando via split simples...")
    # fallback
    if 'window.pixelId' in content:
        content = re.sub(r'<script[^>]*?>[^<]*?window\.pixelId[^<]*?pixel\.js[^<]*?</script>', new_pixel, content, flags=re.DOTALL)
        print("Pixel substituido por fallback.")

# Replace utm
utm_pattern = re.compile(r'<script[^>]*?src=["\']https://cdn\.utmify\.com\.br/scripts/utms/latest\.js["\'][^>]*?></script>', re.DOTALL)
if utm_pattern.search(content):
    content = utm_pattern.sub(new_utm, content)
    print("UTM substituido.")
else:
    print("UTM antigo não encontrado.")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done.")
