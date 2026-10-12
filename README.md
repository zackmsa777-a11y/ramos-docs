# The Ramos Book

A practical book for **Ramos 0.23.0**: Markdown for AI coding agents and a
readable HTML edition for people, generated from the same source.

- **Read online:** [The Ramos Book](https://zackmsa777-a11y.github.io/ramos-docs/)
- **Markdown chapters:** [Start here](book/00-welcome.md)
- **Single Markdown book:** [BOOK.md](book/BOOK.md)
- **AI agents:** [Capability guide](book/16-agent-guide.md)
- **HTML edition:** [docs/index.html](docs/index.html), including an entire-book print view
- **Compiler:** [zackmsa777-a11y/ramos](https://github.com/zackmsa777-a11y/ramos)

The language rules are **simple programming** and **measured native speed**.
This edition describes released features; proposed upgrades are clearly marked.

## Ramos project family

This book is the documentation repository in the
[five-repository Ramos hub](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/ecosystem.md).
Find [small examples](https://github.com/zackmsa777-a11y/ramos-examples), the
[native scientific calculator](https://github.com/zackmsa777-a11y/ramos-calculator)
and [benchmarks](https://github.com/zackmsa777-a11y/ramos-benchmarks) there.
All five use the shared [`ramos` topic](https://github.com/topics/ramos).
The existing compiler release and book URLs remain stable.

## Contents

1. Welcome to the Ramos Book
2. Install, build and run
3. Diagnostics, formatting and running source files
4. The language
5. Easier syntax: branches, ranges and assignment
6. Native float64 and essential math
7. Decimal input and streamed numerical tools
8. Strings, structs, arrays and memory
9. Reusable text builders and streamed text tools
10. Collection capacity, release and integer sorting
11. Checked recursion and native stack budgets
12. Working with bytes
13. Stdin and number conversion
14. Arguments and file I/O
15. Libraries with weave
16. Paths, directories, environment and child processes
17. CLI tools and terminal interfaces
18. Monotonic timing and terminal animation
19. Desktop GUI on Windows and Linux
20. Native drawing and retained canvas frames
21. Windows and cross-compilation
22. Runnable projects
23. How the compiler builds itself
24. Limits and standard library reference
25. Performance and evidence
26. Versions, installation and compatibility
27. What comes next
28. Guide for AI coding agents

The `examples/` and `stdlib/` folders contain matching source from the compiler
repository. Download a native compiler from the
[0.23.0 release](https://github.com/zackmsa777-a11y/ramos/releases/tag/v0.23.0)
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
