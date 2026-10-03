import os
import re
import urllib.request

HTML_FILE = "index.html"
CSS_FILES = ["css/53144c68c6dcd13a.css", "css/ccd75821ad024a8c.css"]

if not os.path.exists('fonts'):
    os.makedirs('fonts')

font_url_pattern = re.compile(r'(https://paperprime\.vercel\.app)?(/_next/static/media/[a-zA-Z0-9-_\.]+\.woff2)')

def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = font_url_pattern.findall(content)
    unique_fonts = set()
    for full_domain, path in matches:
        unique_fonts.add(path)
        
    print(f"Processing {filepath}: found {len(unique_fonts)} unique fonts")
        
    for font_path in unique_fonts:
        filename = os.path.basename(font_path)
        local_path = f"fonts/{filename}"
        
        if not os.path.exists(local_path):
            download_url = f"https://paperprime.vercel.app{font_path}"
            print(f"Downloading {download_url}...")
            try:
                urllib.request.urlretrieve(download_url, local_path)
            except Exception as e:
                print(f"Failed to download {download_url}: {e}")
                
        abs_url = f"https://paperprime.vercel.app{font_path}"
        
        if filepath.startswith('css'):
            replacement = f"../fonts/{filename}"
        else:
            replacement = f"fonts/{filename}"
            
        content = content.replace(abs_url, replacement)
        content = content.replace(font_path, replacement)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_file(HTML_FILE)
for css in CSS_FILES:
    process_file(css)
    
print("Done processing fonts!")
