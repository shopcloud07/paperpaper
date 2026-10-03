import os
import re
import urllib.parse

images_dir = "images"
local_files = os.listdir(images_dir)

# Helper function to remove dots, dashes, and spaces for fuzzy matching
def normalize(s):
    # Remove webp extension first to not mess up normalize if we compare slightly different endings
    s = s.replace('.webp', '')
    return re.sub(r'[\-\s\.]', '', s).lower()

local_map = {normalize(f): f for f in local_files if f.endswith('.webp')}

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Pattern to find all ibb.co urls
pattern = r'https://i\.ibb\.co/[^"\'\s\?)]+'
urls = set(re.findall(pattern, html))

matches_found = 0
for url in urls:
    original_filename = url.split('/')[-1]
    norm_filename = normalize(original_filename)
    
    if norm_filename in local_map:
        target_filename = local_map[norm_filename]
        # Must be URL encoded for HTML attributes if it contains spaces
        local_target_raw = f"images/{target_filename}"
        local_target_escaped = urllib.parse.quote(local_target_raw)
        
        # Replace occurrences in regular format
        html = html.replace(url, local_target_escaped)
        html = html.replace(url, local_target_raw) # just in case
        
        # Replace escaped JSON format if used anywhere
        url_escaped_json = url.replace("/", "\/")
        html = html.replace(url_escaped_json, local_target_escaped.replace("/", "\/"))
        
        matches_found += 1
        print(f"[OK] {original_filename} -> {target_filename}")
    else:
        print(f"[FALHA] Sem match local para {original_filename}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nFinalizado! {matches_found} de {len(urls)} URLs substituidas pelo caminho local da pasta images.")
