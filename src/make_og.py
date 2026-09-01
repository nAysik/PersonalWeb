"""Generate the 1200x630 social cards: dist/og.png (EN) and dist/og-cs.png (CS).

Run from the repo root:   python src/make_og.py
Only needed when the headline copy or brand colours change.
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

BG = (250, 252, 252)
INK = (12, 20, 19)
INK_SOFT = (61, 77, 74)
TEAL = (0, 209, 193)
TEAL_DEEP = (11, 126, 116)
W, H = 1200, 630

BOLD = ['segoeuib.ttf', 'arialbd.ttf']
BLACK = ['seguibl.ttf', 'segoeuib.ttf', 'arialbd.ttf']
SEMI = ['seguisb.ttf', 'segoeui.ttf', 'arial.ttf']

CARDS = {
    'og.png': {
        'line1': 'UA & Ad Monetization',
        'line2': 'for mobile games.',
        'sub': 'Performance user acquisition, mediation & eCPM optimization.',
    },
    'og-cs.png': {
        'line1': 'UA a ad monetizace',
        'line2': 'pro mobilní hry.',
        'sub': 'Výkonnostní user acquisition, mediace a optimalizace eCPM.',
    },
}


def font(names, size):
    for n in names:
        p = os.path.join('C:/Windows/Fonts', n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def build(spec, out):
    img = Image.new('RGB', (W, H), BG)

    glow = Image.new('RGB', (W, H), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse([880, -220, 1420, 320], fill=(214, 246, 242))
    g.ellipse([-180, 420, 260, 860], fill=(228, 248, 245))
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(90)), 1.0)

    d = ImageDraw.Draw(img)

    for y in range(0, H, 30):
        for x in range(0, W, 30):
            if x > 760:
                continue
            a = max(0.0, 1.0 - (x / 900.0))
            c = tuple(int(bg + (ink - bg) * 0.13 * a) for bg, ink in zip(BG, INK))
            d.ellipse([x, y, x + 2, y + 2], fill=c)

    M = 84
    f_k = font(SEMI, 24)
    d.ellipse([M, 150, M + 14, 164], fill=TEAL)
    x = M + 30
    for ch in 'MARTIN HENDRYCH':
        d.text((x, 142), ch, font=f_k, fill=INK_SOFT)
        x += d.textlength(ch, font=f_k) + 3.4

    f_t = font(BLACK, 78)
    d.text((M, 206), spec['line1'], font=f_t, fill=INK)
    d.text((M, 300), spec['line2'], font=f_t, fill=TEAL_DEEP)

    d.rectangle([M, 432, M + 96, 439], fill=TEAL)

    d.text((M, 470), spec['sub'], font=font(SEMI, 27), fill=INK_SOFT)
    d.text((M, H - 84), 'hendrych.me', font=font(BOLD, 25), fill=INK)

    path = os.path.join(DIST, out)
    img.save(path, optimize=True)
    print('  dist/%-12s %6d bytes' % (out, os.path.getsize(path)))


if __name__ == '__main__':
    for name, spec in CARDS.items():
        build(spec, name)
