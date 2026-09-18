import re

html_path = r"C:\Users\Pichau\.gemini\antigravity\scratch\paperprime\original.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace /_next/ to absolute URL for css and js
content = content.replace('="/_next/', '="https://paperprime.vercel.app/_next/')
content = content.replace('="\\/_next\\/', '="https:\\/\\/paperprime.vercel.app\\/_next\\/')
content = content.replace("='/_next/", "='https://paperprime.vercel.app/_next/")

# Replace images
content = content.replace('/_next/image?url=', 'https://paperprime.vercel.app/_next/image?url=')

# Replace other root relative links
content = content.replace('="/favicon.ico"', '="https://paperprime.vercel.app/favicon.ico"')

# Save to index.html
out_path = r"C:\Users\Pichau\.gemini\antigravity\scratch\paperprime\index.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML converted successfully with image fixes.")
