# Guide for AI coding agents

This chapter is a compact capability contract for agents generating Ramos
programs. Target **0.21.0** unless the task explicitly provides a newer compiler
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
- `int64`, `float64`, `bool`, `bytes`, `string`, named structs and `[T]` arrays.
- `"bytes"` and `s"UTF-8 string"` have different types. Conversions copy.
- `weave "relative/path.ramos"` is top-level and resolves relative to its file.
- Use `+=` for matching int64/float64/string values and `-=` for int64/float64. These are
  statements, with destinations evaluated once before the RHS. Local bindings
  must be `var`; a for counter cannot be reassigned.

## Do not invent these features

No `import`, `++`, `*=`, `/=`, bitwise/shift operators,
exceptions, nullable pointers, generics, methods, closures, namespaces, package
manager, asynchronous child spawning, environment mutation or recursive backup. Both `else if` chains and nested `if` blocks are supported. Planned features in the roadmap are not current
capabilities. Do not substitute Python or C as a hidden backend for Ramos code.

## Error and lifetime contracts

Integer overflow, divide-by-zero, invalid bounds and malformed string UTF-8
trap with a diagnostic and exit 1. Expected file failures are fallible instead.
Check `io_error()` immediately after operations that use it; another operation
can change it. Check `parse_error()` after `text_to_int` or `num_parse`; zero
as a return value alone does not distinguish a successful parse from failure.

`arg_count()` includes the executable name. Use `arg()` for bytes, `cli_arg()`
for validated strings. Process the final nonempty stdin line even if EOF is set.
Close file streams and directory iterators explicitly; GC reclaims memory, not OS handles. Do not mix
buffered stdin reading with raw terminal input.

For directories/processes, read [OS contracts](18-system.md). Use directory
entry kinds, skip links/junctions during traversal, and close after early exit.
`process_run(executable: string, arguments: [string])` has explicit status/code;
there is no shell or PATH lookup. Supply an executable path; at most 256 argument
values and 32767 packed UTF-8 bytes. Child input/output is inherited, not captured.
`system_env` returns bytes and distinguishes missing (-2) from empty success.

For GUI, use `run app.ramos --gui` or `build app.ramos -o PROGRAM --gui`.
Windows uses system controls; Linux requires GTK3 and a display. A static Linux
build returns -38 from GUI startup, a missing display returns -19, and missing
shared libraries prevent loader startup. X11 is verified; Wayland is unverified.
GTK memory is outside the Ramos managed heap. Pump events regularly, use blocking
waits when idle and close the window. Use checked `gui_rect`/`gui_inset`/`gui_row`/`gui_column` geometry and
`gui_open_file`/`gui_save_file` path pickers. Picker status 0 selects, 1 cancels,
and negatives fail. Selection does not read/create/overwrite a file. Use
`gui_set_bytes` to reject invalid file text before changing an editor. Notes
keeps exclusive creation and preserves editor/path when Open fails. Do not invent
automatic layout/DPI handling, multiple windows or general canvas APIs. For TUI, require an interactive terminal and restore it before exit.

For incremental text, use the [text builder](20-text-builder.md). Check append
status (0 or -27); byte count differs from Unicode scalar count. Snapshot
strings are independent; clear reuses capacity and release drops storage for
normal collection. Do not access backing fields to bypass UTF-8 checks.

For numerical code, read [float64 and math](21-math.md). Use explicit
`float64(int64)` and `float_to_int(float64)`; mixed numeric operations fail.
Float overflow/non-finite results, division by zero, invalid conversion and
negative nonzero square root trap; gradual underflow is allowed. Printing uses
six fractional digits; `float_to_text`/`math_text` allow 0..18 fixed digits,
not lossless round trips. Do not invent NaN/infinity. For numeric input use
`math_parse(string)` or `math_parse_bytes(bytes)` from the [math-input library](22-math-input.md).
Check the returned FloatResult.status (0, -22, -27 or -34) before using value.
It does not change integer parse_error or io_error. Do not invent a native
text_to_float intrinsic or silently trim input; parsing consumes the whole buffer.

## Build and verify

Use `ramos run app.ramos -- ARG...` for local native execution; stdin, stdout
and stderr are inherited and child exit codes are forwarded. Use `build` for
saved or cross-target executables. `run` also accepts `--gui` before `--`. `ramos fmt app.ramos --check`
checks formatting; `fmt app.ramos -o copy.ramos` writes an atomic copy and
protects source aliases. It validates lexical syntax only, not full types.
Errors show an escaped source line and caret with byte-column locations. Read
[authoring contracts](19-devtools.md) before relying on temp-file lifetime.


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

For frame timing, `monotonic_ms()` returns nonnegative milliseconds or -1;
check `io_error()` immediately. It needs no terminal/GUI setup. Read
[timing contracts](23-timing.md), use differences and deadlines, and avoid
repeated rendering while paused. Do not interpret it as a Unix timestamp.

For bounded integer collections, use `list_try_push` for expected full-capacity
input, `list_reserve` when size is known and `list_sort` for ascending signed
order. Map lookup stays linear. Clear retains arrays; release detaches owned
storage while preserving external aliases. Read [collection contracts](24-collections.md).
