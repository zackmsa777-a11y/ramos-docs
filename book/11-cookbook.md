# Runnable projects

These are complete programs from Ramos 0.19.1, not pseudocode. The repository
includes their exact source under `examples/` and the matching `stdlib/`.
Compile commands below assume you placed the native compiler in this
repository's root. Add `--force` when intentionally rebuilding an output.

## File copy

```sh
./ramos-linux-x86_64 build examples/rcopy.ramos -o rcopy
./rcopy source.bin new-copy.bin
```

```powershell
.\ramos.exe build .\examples\rcopy.ramos -o .\rcopy.exe
.\rcopy.exe .\source.bin .\new-copy.bin
```

[Source: rcopy.ramos](../examples/rcopy.ramos). Uses streamed I/O, processes files
larger than the per-buffer limit and refuses existing destinations. Failed
streaming copies can leave a partial new file; they are not atomic replacement.

## Literal file search

```sh
./ramos-linux-x86_64 build examples/rgrep.ramos -o rgrep
./rgrep needle book/00-welcome.md book/01-getting-started.md
```

[Source: rgrep.ramos](../examples/rgrep.ramos). Matches literal bytes, reports
file and line, and returns 0 for a match, 1 for none and 2 for errors. It does
not traverse directories or interpret regular expressions.

## Full-screen file viewer

```sh
./ramos-linux-x86_64 build examples/rview.ramos -o rview
./rview book/00-welcome.md
```

[Source: rview.ramos](../examples/rview.ramos). Run in an interactive terminal;
use arrows, j/k, Space/n, p and q. The viewer deliberately sanitizes non-ASCII
and control bytes. It is not a complete Unicode text editor.

## Desktop Notes — Windows and Linux

```powershell
.\ramos.exe build .\examples\notes.ramos -o .\notes.exe --gui
.\notes.exe
```

[Source: notes.ramos](../examples/notes.ramos). Unicode editor, Open/Save/Save As/Clear
buttons, status messages and resizing. Save creates a new file and refuses an
existing path. Open chooses and loads a valid UTF-8 file; cancellation or invalid text preserves
the current note. Save As chooses a new path and keeps exclusive creation. Shared
row/padding helpers handle resize. There is no unsaved-change prompt.

## A small GUI event loop

[Source: gui_hello.ramos](../examples/gui_hello.ramos):

```ramos
weave "stdlib/gui.ramos"
weave "stdlib/numbers.ramos"

fn main() {
    gui_check(gui_open(s"Hello, Ramos", 360, 180))
    gui_label(1, 20, 20, 320, 24, s"A real window, written in Ramos")
    gui_button(2, 20, 60, 120, 32, s"Click me")
    var count = 0
    var running = true
    while running {
        let event = gui_event(-1)
        if event.kind == 1 { running = false }
        if event.kind == 2 && event.id == 2 {
            count = count + 1
            gui_set(1, s"Clicks: " + num_text(count))
        }
    }
    gui_check(gui_close())
}

```

The code above is intended as a root-level source file. The checked-in example
is inside `examples/` and therefore uses `../stdlib/`. Build for Windows with
`--gui`; Linux can run the same source with GTK3 installed:

```sh
./ramos-linux-x86_64 run examples/notes.ramos --gui
```

See [desktop GUI setup and limits](09-gui.md).

## More complete sources

- [Interactive number input](../examples/input.ramos)
- [Streaming Unicode line statistics](../examples/line_stats.ramos)
- [Library, list and map demo](../examples/library_demo.ramos)
- [Checked calculator](../examples/calculator.ramos)

The shell and PowerShell versions of a build follow the same structure:
`COMPILER build SOURCE -o OUTPUT`. Windows outputs should use `.exe`.

## Recursive file-name search

```sh
./ramos-linux-x86_64 build examples/rfind.ramos -o rfind
./rfind examples .ramos
```

[Source: rfind.ramos](../examples/rfind.ramos). Iterative traversal uses one
directory handle at a time, skips links/junctions and reports OS failures.
See [limits and traversal policy](18-system.md).

## Direct command execution

```powershell
.\ramos.exe build .\examples\rrun.ramos -o .\rrun.exe
.\rrun.exe .\ramos.exe --version
```

[Source: rrun.ramos](../examples/rrun.ramos). No shell or PATH lookup. Argument
values and inherited standard streams are preserved; OS failures are separate
from child exit codes. Exit codes above 255 map to 1 in this small CLI wrapper.

## Run and format while developing

```sh
./ramos-linux-x86_64 run examples/hello.ramos
./ramos-linux-x86_64 run examples/rgrep.ramos -- needle README.md
./ramos-linux-x86_64 fmt examples/hello.ramos -o hello-formatted.ramos
./ramos-linux-x86_64 fmt hello-formatted.ramos --check
```

The same commands work with `.\ramos.exe` in PowerShell. [Authoring tools](19-devtools.md)
cover preserved comments/newlines, error previews and cleanup.

## Number UTF-8 lines

```sh
./ramos-linux-x86_64 run examples/rnumber.ramos -- input.txt
```

[Source](../examples/rnumber.ramos). Streams input, reuses one text builder and
normalizes LF/CRLF output. [Text builder contracts](20-text-builder.md) cover
size/error behavior and immutable snapshots.

## Render a numerical image

```sh
./ramos-linux-x86_64 run examples/mandelbrot.ramos -- image.pgm 320 240 100
```

```powershell
.\ramos.exe run .\examples\mandelbrot.ramos -- image.pgm 320 240 100
```

[Source](../examples/mandelbrot.ramos). Native float64 computes P5 grayscale
pixels; an image viewer opens the result. Existing output is preserved. Read
[math and renderer contracts](21-math.md) for argument and size limits.

## Summarize decimal numbers

```sh
./ramos-linux-x86_64 run examples/rstats.ramos -- numbers.txt
```

```powershell
.\ramos.exe run .\examples\rstats.ramos -- .\numbers.txt
```

[Source](../examples/rstats.ramos). Read one decimal number per line and report
count/min/max/sum/mean. Omit the argument to read stdin. Input files are preserved.
[Decimal input contracts](22-math-input.md) explain status precedence, strict
syntax, fixed output and checked summation.

## Larger application: scientific calculator

The [calculator repository](https://github.com/zackmsa777-a11y/ramos-calculator)
is a complete application consumer of Ramos 0.19.1: a shared expression engine,
CLI/REPL and resizable native desktop GUI. It demonstrates `weave`, strings,
structs, float64, fallible decimal input, reusable functions and GUI event loops.
The parser handles precedence, parentheses, integer powers and bounded
scientific functions implemented in Ramos. Its README documents numerical
limits and setup; its checks compare independent references and native UI behavior.

Find smaller programs in [ramos-examples](https://github.com/zackmsa777-a11y/ramos-examples).
The existing sources bundled with this book remain pinned and runnable. Browse
all five repositories from the [Ramos hub](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/ecosystem.md).
