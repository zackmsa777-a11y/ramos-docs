# Working on the Ramos Book

This repository documents Ramos; it is not the compiler repository.

- Target the released version recorded in `book.json` (currently 0.23.0).
- Edit canonical chapters in `book/`; never directly edit generated `docs/` or
  `book/BOOK.md`. Change design assets in `assets/`.
- Treat proposed roadmap features as unavailable until verified in a release.
- Preserve bytes/string distinctions, checked arithmetic, source-relative
  `weave`, fallible I/O status and platform limits.
- Keep examples native Ramos. Verify changed complete programs with the matching
  compiler; do not introduce a hidden Python/C implementation.
- The compiler and bundled libraries are upstream sources. Review updates before
  copying them; record the upstream commit in `book.json`.
- Run `python3 tools/build.py`, `python3 tools/build.py --check` and
  `python3 tools/check.py` before publishing documentation changes.
- Do not invent performance measurements, API functions or license terms.

For agents writing Ramos applications, read `book/16-agent-guide.md` and the
relevant chapters. Repository instructions here apply to documentation edits.
