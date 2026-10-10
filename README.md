# The Ramos Book

A practical book for **Ramos 0.13.0**: Markdown for AI coding agents and a
readable HTML edition for people, generated from the same source.

- **Read online:** [The Ramos Book](https://zackmsa777-a11y.github.io/ramos-docs/)
- **Markdown chapters:** [Start here](book/00-welcome.md)
- **Single Markdown book:** [BOOK.md](book/BOOK.md)
- **AI agents:** [Capability guide](book/16-agent-guide.md)
- **HTML edition:** [docs/index.html](docs/index.html), including an entire-book print view
- **Compiler:** [zackmsa777-a11y/ramos](https://github.com/zackmsa777-a11y/ramos)

The language rules are **simple programming** and **measured native speed**.
This edition describes released features; proposed upgrades are clearly marked.

## Contents

1. Welcome and capability overview
2. Install, build and run on Linux and Windows
3. Syntax, control flow, functions and checked arithmetic
4. Strings, structs, arrays and reclaiming memory
5. Byte buffers and binary data
6. Stdin and number conversion
7. Arguments and file I/O
8. `weave` and the standard library
9. CLI tools and terminal interfaces
10. Native Windows desktop GUI
11. Windows and cross-compilation
12. Runnable projects
13. Compiler self-hosting
14. Limits and standard library signatures
15. Performance evidence
16. Proposed application-language roadmap
17. AI coding agent guide

The `examples/` and `stdlib/` folders contain matching source from the compiler
repository. Download a native compiler from the
[0.13.0 release](https://github.com/zackmsa777-a11y/ramos/releases/tag/v0.13.0)
and place it at this repository's root to compile those examples. See the
[quick start](book/01-getting-started.md). This repository does not include or
implement a second compiler.

## Read offline

Open `docs/index.html` in a browser, or use a local HTTP server for book search:

```sh
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. Reading HTML does not require Python; only this
optional preview command does. Chapter navigation, themes and print view work
without a server. Search uses a static JSON index and requires HTTP hosting.

## Build and check both editions

```sh
python3 -m pip install -r requirements.txt
python3 tools/build.py
python3 tools/build.py --check
python3 tools/check.py
```

Edit `book/*.md`, not generated HTML or `book/BOOK.md`. `book.json` records
chapter order and the upstream source commit. `assets/` contains the small
stylesheet and browser script. The build produces committed HTML in `docs/`
for GitHub Pages; there is no frontend framework or server-side application.

GitHub Pages publishes `main` → `/docs`. CI verifies that generated editions
match the Markdown and checks internal links. To update this book for a future
Ramos release, review changed compiler contracts and examples, update the
version/provenance, then regenerate and check both editions. Do not label planned
syntax as supported before a compiler release actually implements it.

Documentation and source excerpts originate in the Ramos project at the commit
recorded in [book.json](book.json). No additional license grant is introduced.
