import sys
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('obrigado')
if idx == -1:
    print('obrigado not found')
    sys.exit(0)

a_tag_start = html.rfind('<a ', 0, idx)
a_tag_end = html.find('>', a_tag_start)
a_tag = html[a_tag_start:a_tag_end+1]

new_a_tag = re.sub(r'href="[^"]*"', 'href="https://www.ggcheckout.com.br/checkout/v4/KT3V3LhJz6DttxgTybFl"', a_tag)
html = html[:a_tag_start] + new_a_tag + html[a_tag_end+1:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Substituido com sucesso usando rfind no script')
