replacements = [
    ("https://i.ibb.co/KjxzKgKC/PAPER-01-3-P.webp", "https://i.ibb.co/mVxpSTK2/PAPER-01-3-P.webp"),
    ("https://i.ibb.co/TBCgR7TY/PAPER-02-P.webp", "https://i.ibb.co/y2g9L4z/PAPER-02-P.webp"),
    ("https://i.ibb.co/hxVtvyX4/PAPER-03-P.webp", "https://i.ibb.co/2YHnJxD7/PAPER-03-P.webp"),
    ("https://i.ibb.co/sp7snLBR/PAPER-04-P.webp", "https://i.ibb.co/0Rbh35Qf/PAPER-04-P.webp"),
    ("https://i.ibb.co/VpMzPqCD/PAPER-05-P.webp", "https://i.ibb.co/Vpj2ZpSD/PAPER-05-P.webp"),
    ("https://i.ibb.co/r2KDPYQs/PAPER-06-P.webp", "https://i.ibb.co/tw31Vy78/PAPER-06-P.webp"),
    ("https://i.ibb.co/0yVgwmwv/PAPER-07-P.webp", "https://i.ibb.co/fzBt2BGW/PAPER-07-P.webp"),
    ("https://i.ibb.co/Dfd9Hdtj/PAPER-08-P.webp", "https://i.ibb.co/spvjSQF5/PAPER-08-P.webp"),
    ("https://i.ibb.co/1f6vSzdv/PAPER-09-P.webp", "https://i.ibb.co/0y00vjdB/PAPER-09-P.webp"),
    ("https://i.ibb.co/Gv0c1X6J/PAPER-10-P.webp", "https://i.ibb.co/fdV5XZ4X/PAPER-10-P.webp"),
    ("https://i.ibb.co/gMZs85JP/PAPER-11-P.webp", "https://i.ibb.co/JwqXpswg/PAPER-11-P.webp"),
    ("https://i.ibb.co/LXDR6779/PAPER-12-P.webp", "https://i.ibb.co/MytSzFw1/PAPER-12-P.webp"),
    ("https://i.ibb.co/whPg9DBk/PAPER-13-P.webp", "https://i.ibb.co/VWwSWyvj/PAPER-13-P.webp"),
    ("https://i.ibb.co/xy7Y0q8/PAPER-14-P.webp", "https://i.ibb.co/ZsgGYhD/PAPER-14-P.webp"),
    ("https://i.ibb.co/WvfXR2z1/PAPER-15-P.webp", "https://i.ibb.co/jkf9n86M/PAPER-15-P.webp"),
    ("https://i.ibb.co/Z1kv7Rb3/PAPER-16-P.webp", "https://i.ibb.co/13Ykcbh/PAPER-16-P.webp"),
    ("https://i.ibb.co/qLSw3KD2/PAPER-17-P.webp", "https://i.ibb.co/tM89wzjx/PAPER-17-P.webp"),
    ("https://i.ibb.co/WvzVPDnW/PAPER-18-P.webp", "https://i.ibb.co/cKJp8zNW/PAPER-18-P.webp"),
    ("https://i.ibb.co/tpYvwD8D/PAPER-19-P.webp", "https://i.ibb.co/wZJgJwHh/PAPER-19-P.webp"),
    ("https://i.ibb.co/hxycsjjP/MODULO-01-VAI-RECEBER-P.webp", "https://i.ibb.co/Rp81wNXQ/MODULO-01-VAI-RECEBER-P.webp"),
    ("https://i.ibb.co/vxRjrGrk/MODULO-02-VAI-RECEBER-P.webp", "https://i.ibb.co/3yMYXDrt/MODULO-02-VAI-RECEBER-P.webp"),
    ("https://i.ibb.co/TB4fV8h2/MODULO-03-VAI-RECEBER-P.webp", "https://i.ibb.co/JwpNSJ9T/MODULO-03-VAI-RECEBER-P.webp"),
    ("https://i.ibb.co/SDyybVhn/PROVA-01-P.webp", "https://i.ibb.co/xqmCD5wF/PROVA-01-P.webp"),
    ("https://i.ibb.co/HfhmZXcF/PROVA-02-P.webp", "https://i.ibb.co/GvFvz7TK/PROVA-02-P.webp"),
    ("https://i.ibb.co/v4RZ2DFg/PROVA-03-P.webp", "https://i.ibb.co/cK8jbnSJ/PROVA-03-P.webp"),
    ("https://i.ibb.co/5gRQ9Ymb/PROVA-04-P.webp", "https://i.ibb.co/DHdtw0pL/PROVA-04-P.webp"),
    ("https://i.ibb.co/4ngSgGCK/PROVA-05-P.webp", "https://i.ibb.co/F4MDbzCn/PROVA-05-P.webp"),
    ("https://i.ibb.co/GY3925r/POUPUP-BAU-P.webp", "https://i.ibb.co/Y7WWNwzg/POUPUP-BAU-P.webp"),
]

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

count_total = 0
for old, new in replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"[OK] Substituida {count}x: ...{old[-30:]}")
    else:
        print(f"[--] Nao encontrada: ...{old[-30:]}")
    count_total += count

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nTotal de substituicoes feitas: {count_total}")
