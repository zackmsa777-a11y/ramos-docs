# Runnable projects

These are complete programs from Ramos 0.14, not pseudocode. The repository
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

## Desktop Notes — Windows

```powershell
.\ramos.exe build .\examples\notes.ramos -o .\notes.exe --gui
.\notes.exe
```

[Source: notes.ramos](../examples/notes.ramos). Unicode editor, Save/Clear
buttons, status messages and resizing. Save creates a new file and refuses an
existing path. This version has no open dialog or unsaved-change prompt.

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
`--gui`; Linux can cross-compile this source but cannot run its GUI backend.

## More complete sources

- [Interactive number input](../examples/input.ramos)
- [Streaming Unicode line statistics](../examples/line_stats.ramos)
- [Library, list and map demo](../examples/library_demo.ramos)
- [Checked calculator](../examples/calculator.ramos)

The shell and PowerShell versions of a build follow the same structure:
`COMPILER build SOURCE -o OUTPUT`. Windows outputs should use `.exe`.
