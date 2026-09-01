"""Render dist/index.html (English) and dist/cs/index.html (Czech) from
src/template.html + src/strings.json, and regenerate dist/sitemap.xml.

Run from the repo root:   python src/build.py

The files in dist/ are GENERATED. Edit copy in src/strings.json and layout
in src/template.html, never dist/*.html directly -- a rebuild overwrites them.
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://hendrych.me'

# lang code -> (output path relative to dist/, page URL, og locale, switcher label)
LANGS = {
    'en': {'out': 'index.html',    'url': SITE + '/',    'locale': 'en_US', 'label': 'EN', 'og': '/og.png'},
    'cs': {'out': 'cs/index.html', 'url': SITE + '/cs/', 'locale': 'cs_CZ', 'label': 'CS', 'og': '/og-cs.png'},
}
ORDER = ['en', 'cs']


def switcher(active, strings, indent, extra_class=''):
    """Both languages shown, the active one marked. Links are root-absolute so
    they work identically from / and /cs/."""
    links = []
    for i, code in enumerate(ORDER):
        cfg = LANGS[code]
        href = '/' if code == 'en' else '/%s/' % code
        if code == active:
            links.append('<a href="%s" hreflang="%s" lang="%s" class="on" aria-current="true">%s</a>'
                         % (href, code, code, cfg['label']))
        else:
            links.append('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (href, code, code, cfg['label']))
        if i == 0:
            links.append('<span class="sep" aria-hidden="true">/</span>')
    pad = ' ' * indent
    cls = ('lang ' + extra_class).strip()
    return ('%s<div class="%s" role="group" aria-label="%s">\n%s  %s\n%s</div>'
            % (pad, cls, strings['a11y_lang'], pad, ''.join(links), pad))


def main():
    template = io.open(os.path.join(SRC, 'template.html'), encoding='utf-8').read()
    data = json.load(io.open(os.path.join(SRC, 'strings.json'), encoding='utf-8'))

    # Both languages must define the same keys, or one page silently keeps English.
    keys = {c: set(k for k in data[c] if not k.startswith('_')) for c in ORDER}
    if keys['en'] != keys['cs']:
        missing_cs = sorted(keys['en'] - keys['cs'])
        missing_en = sorted(keys['cs'] - keys['en'])
        sys.exit('strings.json key mismatch\n  missing in cs: %s\n  missing in en: %s'
                 % (missing_cs or 'none', missing_en or 'none'))

    written = []
    for code in ORDER:
        cfg = LANGS[code]
        s = dict(data[code])
        other = [c for c in ORDER if c != code][0]
        s.update({
            'html_lang': code,
            'canonical': cfg['url'],
            'og_locale': cfg['locale'],
            'og_locale_alt': LANGS[other]['locale'],
            'og_image': SITE + cfg['og'],
            'lang_switch_nav': switcher(code, data[code], 6),
            'lang_switch_mobile': switcher(code, data[code], 4),
        })

        out = template
        for key, value in s.items():
            out = out.replace('{{%s}}' % key, value)

        leftover = sorted(set(re.findall(r'\{\{(\w+)\}\}', out)))
        if leftover:
            sys.exit('[%s] unresolved placeholders: %s' % (code, ', '.join(leftover)))

        path = os.path.join(DIST, cfg['out'])
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
        written.append((cfg['out'], len(out)))

    # sitemap: each page lists itself plus every alternate, as Google expects
    rows = []
    for code in ORDER:
        alts = '\n'.join(
            '    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (c, LANGS[c]['url'])
            for c in ORDER)
        rows.append(
            '  <url>\n    <loc>%s</loc>\n%s\n'
            '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n'
            '    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>'
            % (LANGS[code]['url'], alts, LANGS['en']['url']))
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
               '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
               + '\n'.join(rows) + '\n</urlset>\n')
    io.open(os.path.join(DIST, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sitemap)

    for name, size in written:
        print('  dist/%-16s %6d bytes' % (name, size))
    print('  dist/sitemap.xml   %6d bytes' % len(sitemap))


if __name__ == '__main__':
    main()
