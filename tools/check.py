#!/usr/bin/env python3
"""Check local links, anchors and duplicate HTML IDs without network access."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if 'id' in props:
            self.ids.append(props['id'])
        for key in ('href', 'src'):
            if key in props:
                self.links.append(props[key])


def main():
    problems, checked = [], 0
    pages = {file:Page(file.read_text()) for file in (ROOT / 'docs').glob('*.html')}
    for file, page in pages.items():
        duplicates = [key for key, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            problems.append(f'{file.relative_to(ROOT)}: duplicate IDs {duplicates}')
    for file in list((ROOT / 'book').glob('*.md')) + [ROOT / 'README.md'] + list(pages):
        text = file.read_text()
        links = pages[file].links if file in pages else re.findall(r'\]\(([^)]+)\)', text)
        for target in links:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            resolved = (file.parent / unquote(url.path)).resolve() if url.path else file
            if not resolved.is_relative_to(ROOT):
                problems.append(f'{file.relative_to(ROOT)}: link leaves repository: {target}')
                continue
            if not resolved.exists():
                problems.append(f'{file.relative_to(ROOT)}: missing link {target}')
            elif url.fragment and resolved.suffix == '.html':
                page = pages.get(resolved)
                if page and unquote(url.fragment) not in page.ids:
                    problems.append(f'{file.relative_to(ROOT)}: missing anchor {target}')
            checked += 1
    meta = json.loads((ROOT / 'book.json').read_text())
    for chapter in meta['chapters']:
        assert (ROOT / 'book' / (chapter['slug'] + '.md')).exists(), chapter['slug']
    assert len(list((ROOT / 'stdlib').glob('*.ramos'))) == 12
    if problems:
        raise SystemExit('\n'.join(problems))
    print(f'Checked {checked} local links; {len(pages)} HTML pages have valid anchors and unique IDs.')


if __name__ == '__main__':
    main()
