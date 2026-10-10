#!/usr/bin/env python3
"""Render the versioned Markdown book into a deterministic static HTML site."""
from pathlib import Path
import argparse
import html
import json
import re
import shutil
import tempfile
from urllib.parse import urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / 'book.json').read_text())
CHAPTERS = META['chapters']


def page_url(slug):
    return 'index.html' if slug == CHAPTERS[0]['slug'] else slug + '.html'


def rewrite_links(body):
    def link(match):
        prefix, target = match.groups()
        if urlsplit(target).scheme or target.startswith('#'):
            return match.group(0)
        path, marker, anchor = target.partition('#')
        if path.endswith('.md') and not path.startswith('../'):
            slug = Path(path).stem
            if slug in {c['slug'] for c in CHAPTERS}:
                target = page_url(slug) + (marker + anchor if marker else '')
        elif path.startswith('../'):
            target = target[3:]
        return prefix + target + ')'
    return re.sub(r'(\]\()([^)]+)\)', link, body)


def render(body):
    return markdown.markdown(rewrite_links(body), extensions=['fenced_code', 'tables', 'toc'],
                             extension_configs={'toc': {'permalink': False}})


def document(title, body, active='', previous='', following='', contents=''):
    esc = html.escape
    nav = ''.join(f'<a href="{page_url(c["slug"])}"'
                  f'{" aria-current=\"page\"" if c["slug"] == active else ""}>'
                  f'<span>{i:02}</span>{esc(c["title"])}</a>'
                  for i, c in enumerate(CHAPTERS))
    pager = f'<nav class="pager" aria-label="Chapter navigation">{previous}{following}</nav>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="The Ramos Book: a practical reference for Ramos {esc(META['version'])}, with Markdown for agents and HTML for people.">
<title>{esc(title)} · The Ramos Book</title>
<link rel="stylesheet" href="assets/book.css"><script src="assets/book.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="index.html"><b>R</b> The Ramos Book <small>{esc(META['version'])}</small></a>
<div class="actions"><a href="book/BOOK.md">Markdown</a><a href="all.html">Print book</a><button id="theme" aria-label="Switch color theme">Theme</button><button id="menu" aria-expanded="false" aria-controls="sidebar">Chapters</button></div></header>
<aside id="sidebar"><label for="search">Search the book</label><input id="search" type="search" placeholder="Strings, files, GUI…" autocomplete="off"><div id="results" aria-live="polite" hidden></div><nav aria-label="Book chapters">{nav}</nav><a class="source" href="https://github.com/zackmsa777-a11y/ramos-docs">Documentation on GitHub ↗</a></aside>
<main id="main"><div class="edition">A practical native language · Simple syntax · Measured speed</div>{contents}<article>{body}</article>{pager}<footer>Ramos {esc(META['version'])} · <a href="book/{active + '.md' if active else 'BOOK.md'}">Read this in Markdown</a> · <a href="https://github.com/zackmsa777-a11y/ramos-docs/issues">Report a documentation issue</a><br>Future features are marked as plans. Examples and limits describe this edition.</footer></main>
</body></html>
'''


def write(output):
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'assets', output / 'assets')
    for folder in ('examples', 'stdlib', 'evidence'):
        shutil.copytree(ROOT / folder, output / folder)
    (output / 'book').mkdir()
    texts = []
    search = []
    for i, chapter in enumerate(CHAPTERS):
        slug, title = chapter['slug'], chapter['title']
        text = (ROOT / 'book' / (slug + '.md')).read_text()
        (output / 'book' / (slug + '.md')).write_text(text)
        body = render(text)
        previous = (f'<a href="{page_url(CHAPTERS[i-1]["slug"])}">← {html.escape(CHAPTERS[i-1]["title"])}</a>' if i else '<span></span>')
        following = (f'<a href="{page_url(CHAPTERS[i+1]["slug"])}">{html.escape(CHAPTERS[i+1]["title"])} →</a>' if i+1 < len(CHAPTERS) else '')
        (output / page_url(slug)).write_text(document(title, body, slug, previous, following))
        texts.append(text)
        search.append({'title':title,'url':page_url(slug),'text':re.sub('<[^>]+>', ' ', body)})
    combined = '# The Ramos Book — ' + META['version'] + '\n\n' + '\n\n---\n\n'.join(texts)
    (output / 'book' / 'BOOK.md').write_text(combined)
    # Identical source text is also available at the repository's root book folder.
    (ROOT / 'book' / 'BOOK.md').write_text(combined)
    contents = '<nav class="contents" aria-label="Full book contents"><h1>The Ramos Book</h1>' + ''.join(f'<a href="#{c["slug"]}">{html.escape(c["title"])}</a>' for c in CHAPTERS) + '</nav>'
    all_body = ''.join(f'<section id="{c["slug"]}">{render(text)}</section>' for c, text in zip(CHAPTERS, texts))
    # Prefix repeated Markdown-generated heading IDs in the full book.
    def prefix_ids(match):
        slug, body = match.groups()
        ids = set(re.findall(r'\bid="([^"]+)"', body))
        body = re.sub(r'\bid="([^"]+)"', lambda m:f'id="{slug}--{m[1]}"', body)
        body = re.sub(r'href="#([^"]+)"', lambda m:f'href="#{slug}--{m[1]}"' if m[1] in ids else m[0], body)
        return f'<section id="{slug}">{body}</section>'
    all_body = re.sub(r'<section id="([^"]+)">(.*?)</section>', prefix_ids, all_body, flags=re.S)
    (output / 'all.html').write_text(document('Complete book', all_body, contents=contents))
    (output / 'assets' / 'search.json').write_text(json.dumps(search, ensure_ascii=False, separators=(',', ':')) + '\n')
    (output / '.nojekyll').write_text('')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='fail if committed HTML or combined Markdown is stale')
    args = parser.parse_args()
    before = (ROOT / 'book' / 'BOOK.md').read_bytes() if (ROOT / 'book' / 'BOOK.md').exists() else None
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / 'docs'
        write(output)
        generated = {str(p.relative_to(output)):p.read_bytes() for p in output.rglob('*') if p.is_file()}
        if args.check:
            actual = {str(p.relative_to(ROOT / 'docs')):p.read_bytes() for p in (ROOT / 'docs').rglob('*') if p.is_file()}
            combined_changed = before != (ROOT / 'book' / 'BOOK.md').read_bytes()
            if before is not None:
                (ROOT / 'book' / 'BOOK.md').write_bytes(before)
            elif combined_changed:
                (ROOT / 'book' / 'BOOK.md').unlink()
            if actual != generated or combined_changed:
                raise SystemExit('Generated edition is stale. Run python3 tools/build.py and commit both editions.')
            print('Both editions match their Markdown sources.')
        else:
            shutil.rmtree(ROOT / 'docs', ignore_errors=True)
            shutil.copytree(output, ROOT / 'docs')
            print(f'Built {len(CHAPTERS)} chapters, complete HTML and Markdown editions.')


if __name__ == '__main__':
    main()
