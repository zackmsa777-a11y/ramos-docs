# Install, build and run

Use the complete
[0.23.0 canvas bundle](https://github.com/zackmsa777-a11y/ramos/releases/download/v0.23.0/ramos-0.23.0-canvas.zip),
which also includes the CLI/TUI tools, both compilers, examples and all thirteen
libraries. Extract the archive and keep its directory structure. The published
`SHA256SUMS` file lists asset hashes for integrity checking.

## Your first source file

Save `hello.ramos` as UTF-8 in the extracted directory:

```ramos
fn main() {
    print(s"Hello, Ramos!")
}
```

## Windows x64 — PowerShell

```powershell
.\ramos.exe --version
.\ramos.exe run .\hello.ramos
.\ramos.exe build .\hello.ramos -o .\hello.exe
.\hello.exe
```

Expected output: `Hello, Ramos!`. Python, a C compiler and a separate runtime
are not required for Windows/CLI programs with the downloaded compiler.
Linux `--gui` programs additionally require system GTK3 and a desktop display;
see [GUI setup](09-gui.md).

## Linux x64 — shell

```sh
chmod +x ramos-linux-x86_64
./ramos-linux-x86_64 --version
./ramos-linux-x86_64 run hello.ramos
./ramos-linux-x86_64 build hello.ramos -o hello
./hello
```

## Formatting and readable errors

```sh
./ramos-linux-x86_64 fmt hello.ramos --check
./ramos-linux-x86_64 fmt hello.ramos -o formatted-hello.ramos
```

Use `.\ramos.exe` for these commands in PowerShell. Source-line/caret errors
help locate mistakes; [authoring tools](19-devtools.md) describe formatting,
argument forwarding and temporary executable cleanup.

## Rebuilding an existing output

Use `--force` only when you intend to replace an existing executable:

```sh
./ramos-linux-x86_64 build hello.ramos -o hello --force
```

A failed compilation preserves existing output. The compiler refuses source
file aliases as output even with `--force`.

## Libraries and example folders

For a root-level source file, use `weave "stdlib/numbers.ramos"`. Sources inside
`examples/` use `weave "../stdlib/numbers.ramos"`. Paths resolve relative to the
source that contains the directive, not the terminal's working directory.

This documentation repository includes the same example and library sources.
To use them, place the downloaded native compiler at the repository root:

```sh
./ramos-linux-x86_64 build examples/library_demo.ramos -o library-demo
./library-demo
```

```powershell
.\ramos.exe build .\examples\library_demo.ramos -o .\library-demo.exe
.\library-demo.exe
```

## Build from the compiler repository

In a checkout of the main Ramos repository, initial bootstrapping on Linux
requires Make and GNU binutils. Python is used for validation, not as a runtime
for generated programs.

```sh
make
./ramos build examples/hello.ramos -o hello --force
./hello
make install PREFIX="$HOME/.local"
```

Once built, the compiler emits executables without those bootstrap tools.
Add the installation prefix's `bin` directory to `PATH` if needed. See
[self-hosting](12-self-hosting.md) for verification commands.
