# Guide for AI coding agents

This chapter is a compact capability contract for agents generating Ramos
programs. Target **0.14.0** unless the task explicitly provides a newer compiler
and verified documentation. Read the relevant chapter rather than guessing
from Python, C or Rust syntax.

## Read in this order

1. [Language](02-language.md): statements, types, operators and functions.
2. [Values](03-values.md): immutable strings, aliases, arrays and heap behavior.
3. [Libraries](07-libraries.md) and [signatures](13-reference.md).
4. [Files](06-files.md), [CLI/TUI](08-cli-tui.md) or [GUI](09-gui.md) for the task.

`BOOK.md` is a generated single-file edition if loading the whole reference is
useful. Individual chapters are smaller and have stable relative links.

## Supported source patterns

- One parameterless `fn main()` returning void per executable; none in libraries.
- Newline-separated statements and braces; no semicolons.
- `let` for an immutable binding, `var` for a reassignable binding. Inferred local
  types cannot change. Mutating a field/array/byte value through `let` is allowed.
- Function parameters use explicit types; omitted return type is void.
- `if`/`else if`/`else`, `while`, `for`, `break`, `continue`, `&&`, `||`, `!`;
  boolean conditions. Range bounds are int64, evaluated once and end-exclusive;
  loop counters are immutable and local to the body.
- `int64`, `bool`, `bytes`, `string`, named structs and `[T]` arrays.
- `"bytes"` and `s"UTF-8 string"` have different types. Conversions copy.
- `weave "relative/path.ramos"` is top-level and resolves relative to its file.
- Use `+=` for matching int64/string values and `-=` for int64. These are
  statements, with destinations evaluated once before the RHS. Local bindings
  must be `var`; a for counter cannot be reassigned.

## Do not invent these features

No `import`, `++`, `*=`, `/=`, floats, bitwise/shift operators,
exceptions, nullable pointers, generics, methods, closures, namespaces, package
manager, direct child-process API or directory iteration. Both `else if` chains and nested `if` blocks are supported. Planned features in the roadmap are not current
capabilities. Do not substitute Python or C as a hidden backend for Ramos code.

## Error and lifetime contracts

Integer overflow, divide-by-zero, invalid bounds and malformed string UTF-8
trap with a diagnostic and exit 1. Expected file failures are fallible instead.
Check `io_error()` immediately after operations that use it; another operation
can change it. Check `parse_error()` after `text_to_int` or `num_parse`; zero
as a return value alone does not distinguish a successful parse from failure.

`arg_count()` includes the executable name. Use `arg()` for bytes, `cli_arg()`
for validated strings. Process the final nonempty stdin line even if EOF is set.
Close file streams explicitly; GC reclaims memory, not OS handles. Do not mix
buffered stdin reading with raw terminal input.

For GUI, support is Windows-only. Pump events regularly, use blocking waits
when idle and close the window. Do not promise dialogs, canvas APIs or a Linux
backend. For TUI, require an interactive terminal and restore it before exit.

## Build and verify

For a native downloaded compiler on Linux:

```sh
./ramos-linux-x86_64 build app.ramos -o app
./app
```

For Windows:

```powershell
.\ramos.exe build .\app.ramos -o .\app.exe
.\app.exe
```

Preserve existing user files; `--force` intentionally replaces outputs. Compile
before reporting working syntax. Check expected output, exit status and failure
paths relevant to the app. Cross-compiling proves emission, not native GUI/TUI
interaction. Do not claim a speedup without equivalent workloads and timings.

When changing compiler internals, use the main repository's native suites and
Linux/Windows fixed-point proofs. This book repository only builds and checks
documentation. Its build dependency is not a Ramos runtime dependency.
