# Welcome to the Ramos Book

Ramos is a small, self-hosted language that compiles directly to native
Linux x64 and Windows x64 executables. Its two guiding rules are **simple
programming** and **measured speed**.

This book describes **Ramos 0.25.0 preview**. Markdown chapters are the canonical edition
for AI agents, review and offline reading. The HTML edition is generated from
those same chapters for comfortable human reading. Historical version labels
identify when a feature arrived; they do not change this book's baseline.

## Choose your path

- New to Ramos? Start with [install, build and run](01-getting-started.md), then
  [the language](02-language.md) and [values](03-values.md).
- Building a tool? Read [files](06-files.md), [libraries](07-libraries.md) and
  [OS libraries](18-system.md) and [CLI/TUI](08-cli-tui.md), then try the [projects](11-cookbook.md).
- Building a desktop window? Read [desktop GUI](09-gui.md) and [native drawing](27-canvas.md) and [logical scaling](29-gui-scaling.md). Windows uses native
  system controls; Linux GUI requires GTK3 and a display.
- Writing Ramos with an AI agent? Start with the [agent guide](16-agent-guide.md)
  and [API reference](13-reference.md).
- Working on the compiler? Read [self-hosting](12-self-hosting.md).

## What you can use today

Checked int64 and finite float64 arithmetic, booleans, functions, comments, while/range loops, else-if chains, compound assignment, immutable
UTF-8 strings, mutable bytes, structs, typed arrays, reclaiming managed memory,
compile-time `weave`, stdin, streamed files, terminal interfaces and Windows/Linux
native GUI controls, directory iteration/creation, lexical path helpers,
environment lookup, direct child execution and reusable UTF-8 text builders.
[Text builders](20-text-builder.md) provide immutable snapshots and capacity
reuse/release for streamed tools.

[Native math](21-math.md) adds explicit conversions, square root and fixed
decimal formatting. [Decimal input](22-math-input.md) adds fallible parsing
for numerical CLI apps such as streamed statistics. There are no namespaces, networking APIs or package registry
in 0.25.0. Read
[the OS libraries](18-system.md) for directory and child-process contracts. See [the new syntax](17-easier-syntax.md) for ranges,
else-if chains and compound assignment. See the
[limits](13-reference.md) and [proposed roadmap](15-roadmap.md). Planned syntax
must not be used in programs targeting this version.

Use `ramos run app.ramos` to compile and execute a source file directly, or
`build` to save an executable. `ramos fmt` formats a copy or checks formatting.
For desktop apps, use `ramos run app.ramos --gui`; Linux CLI/compiler output
remains static. [Authoring tools](19-devtools.md) explain arguments, errors and cleanup.

[Monotonic timing](23-timing.md) supports elapsed-time animation and native frame
deadlines. The [rmatrix project](https://github.com/zackmsa777-a11y/ramos-examples/tree/main/projects/rmatrix)
shows changed-cell terminal rendering.

[Collection controls](24-collections.md) add explicit reserve/release, full-capacity
status handling and signed integer sorting. `rsort` sorts stdin or a streamed file.

## Project links

- [Compiler and source](https://github.com/zackmsa777-a11y/ramos)
- [Ramos 0.25.0 release](https://github.com/zackmsa777-a11y/ramos/releases/tag/v0.25.0)
- [Documentation source](https://github.com/zackmsa777-a11y/ramos-docs)
- [Small runnable examples](https://github.com/zackmsa777-a11y/ramos-examples)
- [Scientific calculator: CLI, REPL and GUI](https://github.com/zackmsa777-a11y/ramos-calculator)
- [Benchmarks and raw historical evidence](https://github.com/zackmsa777-a11y/ramos-benchmarks)
- [Five-repository project hub](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/ecosystem.md)
- [Shared Ramos topic](https://github.com/topics/ramos)

The application repositories pin their compiler and standard-library snapshot.
The calculator's scientific functions are application library code in Ramos;
they do not add new compiler intrinsics to this book's released baseline.
Existing compiler test/release examples and the book's bundled examples remain
available while new standalone example development takes place in `ramos-examples`.

The limits and negative results matter as much as working features. Native
output is not proof of speed, and compiling for an OS is not proof that its
interactive applications have been tested there.

[Checked recursion](25-stack.md) supports 1,024 active calls within a separate
4 MiB stack budget. The scientific calculator uses it for 64 expression levels.
Read [compatibility and installation](26-compatibility.md) before updating a project.

[Canvas drawing](27-canvas.md) supplies bounded reusable commands for native lines,
shapes and pixels. Repaint snapshots survive buffer reuse and garbage collection.
The interactive plot runs on both desktops; per-monitor DPI policy remains future work.

[Exact numerical output](28-math-output.md) provides scientific and compact
strings. Seventeen significant digits preserve finite binary64 values, including
signed zero; the calculator uses it for readable tiny and large results.

The 0.25 preview verifies initial native Windows DPI behavior and bounded
resource churn, plus genuine GTK scale changes. Actual Windows display changes
remain pending an adjustable-display report; see the [test commands](29-gui-scaling.md).
The practical 1.0 goal remains unfinished.
