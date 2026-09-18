import uuid
import re
import urllib.parse

html_file = 'index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "https://i.ibb.co/JwLMRqvR/PAPER-01-3.png": "https://i.ibb.co/KjxzKgKC/PAPER-01-3-P.webp",
    "https://i.ibb.co/HTtvHYYG/PAPER-02.webp": "https://i.ibb.co/TBCgR7TY/PAPER-02-P.webp",
    "https://i.ibb.co/1Ytv0Hm6/PAPER-03.webp": "https://i.ibb.co/hxVtvyX4/PAPER-03-P.webp",
    "https://i.ibb.co/bR5nX5hp/PAPER-04.webp": "https://i.ibb.co/sp7snLBR/PAPER-04-P.webp",
    "https://i.ibb.co/TBzYK4Pm/PAPER-05.webp": "https://i.ibb.co/VpMzPqCD/PAPER-05-P.webp",
    "https://i.ibb.co/d4KsZ73R/PAPER-06.webp": "https://i.ibb.co/r2KDPYQs/PAPER-06-P.webp",
    "https://i.ibb.co/MxXSV5SF/PAPER-07.webp": "https://i.ibb.co/0yVgwmwv/PAPER-07-P.webp",
    "https://i.ibb.co/qYKr64XT/PAPER-08.webp": "https://i.ibb.co/Dfd9Hdtj/PAPER-08-P.webp",
    "https://i.ibb.co/nNvHDGD9/PAPER-09.webp": "https://i.ibb.co/1f6vSzdv/PAPER-09-P.webp",
    "https://i.ibb.co/k6hSNyFD/PAPER-10.webp": "https://i.ibb.co/Gv0c1X6J/PAPER-10-P.webp",
    "https://i.ibb.co/svxhqgD6/PAPER-11.webp": "https://i.ibb.co/gMZs85JP/PAPER-11-P.webp",
    "https://i.ibb.co/pBBZBrwq/PAPER-12.webp": "https://i.ibb.co/LXDR6779/PAPER-12-P.webp",
    "https://i.ibb.co/vCvWV9Tn/PAPER-13.webp": "https://i.ibb.co/whPg9DBk/PAPER-13-P.webp",
    "https://i.ibb.co/vCPyZpjn/PAPER-14.webp": "https://i.ibb.co/xy7Y0q8/PAPER-14-P.webp",
    "https://i.ibb.co/FkCWjVMh/PAPER-15.webp": "https://i.ibb.co/WvfXR2z1/PAPER-15-P.webp",
    "https://i.ibb.co/4wXv8t7m/PAPER-16.webp": "https://i.ibb.co/Z1kv7Rb3/PAPER-16-P.webp",
    "https://i.ibb.co/cMCL2Ww/PAPER-17.webp": "https://i.ibb.co/qLSw3KD2/PAPER-17-P.webp",
    "https://i.ibb.co/Zp81RFwR/PAPER-18.webp": "https://i.ibb.co/WvzVPDnW/PAPER-18-P.webp",
    "https://i.ibb.co/jBmyD0s/PAPER-19.webp": "https://i.ibb.co/tpYvwD8D/PAPER-19-P.webp",
    "https://i.ibb.co/dJgyXxcj/MODULO-01-VAI-RECEBER.webp": "https://i.ibb.co/hxycsjjP/MODULO-01-VAI-RECEBER-P.webp",
    "https://i.ibb.co/jvymXQ5N/MODULO-02-VAI-RECEBER.webp": "https://i.ibb.co/vxRjrGrk/MODULO-02-VAI-RECEBER-P.webp",
    "https://i.ibb.co/V0BHNRw3/MODULO-03-VAI-RECEBER.webp": "https://i.ibb.co/TB4fV8h2/MODULO-03-VAI-RECEBER-P.webp",
    "https://i.ibb.co/G3n97TZv/prova-01.webp": "https://i.ibb.co/SDyybVhn/PROVA-01-P.webp",
    "https://i.ibb.co/gb0PqN2V/prova-02.webp": "https://i.ibb.co/HfhmZXcF/PROVA-02-P.webp",
    "https://i.ibb.co/BHmXzDZ5/prova-03.webp": "https://i.ibb.co/v4RZ2DFg/PROVA-03-P.webp",
    "https://i.ibb.co/BKvs0ts5/prova-04.webp": "https://i.ibb.co/5gRQ9Ymb/PROVA-04-P.webp",
    "https://i.ibb.co/4RnGyrVn/prova-05.webp": "https://i.ibb.co/4ngSgGCK/PROVA-05-P.webp"
}

total_replaced = 0
for old_url, new_url in replacements.items():
    # Regular Replace
    if old_url in content:
        count = content.count(old_url)
        content = content.replace(old_url, new_url)
        total_replaced += count
        print(f"Replaced {count} instances of {old_url}")
        
    # URL Encoded Replace (e.g. https%3A%2F%2Fi.ibb.co...)
    old_url_encoded = urllib.parse.quote(old_url, safe='')
    new_url_encoded = urllib.parse.quote(new_url, safe='')
    if old_url_encoded in content:
        count_encoded = content.count(old_url_encoded)
        content = content.replace(old_url_encoded, new_url_encoded)
        total_replaced += count_encoded
        print(f"Replaced {count_encoded} instances of {old_url_encoded} (URL Encoded)")

    # HTML Encoded (just in case &amp; or others interfere, but usually URL encoding misses ://)
    
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Total replacements made: {total_replaced}")
