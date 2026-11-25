"""Create an original poster asset for the real upload demonstration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "poster-chuyen-tau-cuoi-mua.png"
W, H = 720, 1080
im = Image.new("RGB", (W, H))
px = im.load()
for y in range(H):
    for x in range(W):
        glow = max(0, 1 - ((x - 360) ** 2 / 330 ** 2 + (y - 440) ** 2 / 470 ** 2))
        px[x, y] = (int(8 + 48 * glow), int(17 + 42 * glow), int(31 + 58 * glow))
d = ImageDraw.Draw(im)
d.ellipse((80, 185, 640, 745), outline=(222, 174, 91), width=5)
d.ellipse((144, 249, 576, 681), outline=(136, 117, 86), width=2)
d.line((0, 790, 720, 790), fill=(222, 174, 91), width=5)
d.polygon([(0, 790), (720, 790), (720, 1080), (0, 1080)], fill=(5, 14, 27))
d.line((115, 790, 330, 1080), fill=(230, 190, 110), width=8)
d.line((605, 790, 390, 1080), fill=(230, 190, 110), width=8)
bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 54)
small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
for label, y in [("CHUYẾN TÀU", 370), ("CUỐI MÙA", 445)]:
    box = d.textbbox((0, 0), label, font=bold)
    d.text(((W - box[2]) / 2, y), label, font=bold, fill=(255, 227, 174))
for label, y in [("CINÉ NGHĨA ORIGINAL", 86), ("MỘT HÀNH TRÌNH ĐỂ TRỞ VỀ", 980)]:
    box = d.textbbox((0, 0), label, font=small)
    d.text(((W - box[2]) / 2, y), label, font=small, fill=(226, 197, 148))
im.save(OUT, optimize=True)
print(OUT, OUT.stat().st_size)
