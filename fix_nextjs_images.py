import re
import urllib.parse

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix common corrupted domains in src
content = content.replace("https://paperprime.vercel.apphttps://paperprime.vercel.app", "https://paperprime.vercel.app")
content = content.replace("https://paperprime.vercel.apphttps://", "https://")

# Regex to strip out Next.js image resizer wrapper and extract the raw URL
# Example: /_next/image?url=https%3A%2F%2Fi.ibb.co...&amp;w=3840&amp;q=75
# To -> https://i.ibb.co/...

def replacer(match):
    # Match group 1 is the URL Encoded ibb.co link
    encoded_url = match.group(1)
    # unquote handles both normal %3A and JSON-escaped versions depending on the exact format, but we will unquote manually if needed
    decoded = urllib.parse.unquote(encoded_url)
    return decoded

# Pattern handles both URL-encoded (&amp; etc) 
pattern = r'(?:https://paperprime\.vercel\.app)?/_next/image\?url=(https(?:%3A|%253A|\\u00253A)(?:%2F|%252F|\\u00252F)(?:%2F|%252F|\\u00252F)i\.ibb\.co[^&]+)(?:&amp;|&|\\u0026)w=\d+(?:&amp;|&|\\u0026)q=\d+'

old_len = len(content)
content, count = re.subn(pattern, replacer, content)
print(f"Removed Next.js Image wrapper from {count} URLs")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"File size changed from {old_len} to {len(content)}")
