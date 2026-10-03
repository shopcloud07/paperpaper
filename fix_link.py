import re
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# I want to find the <a href="..."> that encapsulates "10,00"
# Usually, it's <a ...href="#"...> ... 10,00 ... </a>
html_new = re.sub(
    r'<a([^>]*?)href="#"([^>]*?>[^<a]*?10,00[^<]*?</a>)', 
    r'<a\1href="https://www.ggcheckout.com.br/checkout/v4/KT3V3LhJz6DttxgTybFl"\2', 
    html, 
    flags=re.IGNORECASE | re.DOTALL
)

if html == html_new:
    print("Nenhuma mudanca feita! Tentando outra forma...")
    # Maybe it's not exactly `#` but empty or something?
    html_new = re.sub(
        r'<a([^>]*?)href="[^"]*"([^>]*?>[^<a]*?10,00[^<]*?</a>)', 
        r'<a\1href="https://www.ggcheckout.com.br/checkout/v4/KT3V3LhJz6DttxgTybFl"\2', 
        html_new, 
        flags=re.IGNORECASE | re.DOTALL
    )

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_new)
print("Pronto! Substituído.")
