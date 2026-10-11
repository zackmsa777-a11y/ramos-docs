# Limits and standard library reference

The self-hosted compiler accepts up to 64 regular source files totaling 1 MiB
(with boundary separators), at most 50,000
tokens including EOF, 4,096 total declarations including parameters and ended
blocks and hidden range-bound slots, 256 functions and 16 parameters per function. Structs are limited to 64
types with 16 fields each; array type nesting to 16. Expression and block
depth remain bounded at 128; generated programs allow 64 active calls.
Its output and decoded string-data arenas are each 1 MiB; labels and fixups each
have a 40,000-entry bound. These are checked limits. The retained bootstrap has
the older 4 MiB output and IR limits. See [compiler representation limits](https://github.com/zackmsa777-a11y/ramos/blob/1561b5a8d12080e16fb5e43b5aaae15b4f6d0c1a/compiler/README.md).

The compiler is self-hosted; namespaces, more library types, wrapping arithmetic,
broader optimization and additional targets remain future work. Performance claims need
new repeatable measurements. The runtime provides checked arithmetic and bounded
buffers, but generated programs execute with the caller's operating-system
permissions. General canvas graphics, games, a Linux GUI backend and browser support need further platform work.

## Compiler commands

`build SOURCE -o PROGRAM [--force] [--target linux|windows] [--gui]` writes an
executable. `run SOURCE [-- ARG...]` compiles and runs for the native OS.
`fmt SOURCE [--check | -o FILE [--force]]` formats one file. See
[complete authoring contracts](19-devtools.md).

## Float limits

[Float64 contracts](21-math.md) specify 768 mantissa digits and written decimal
exponents -400..400, finite values, explicit conversions and fixed formatting
precision 0..18. These extend numeric types without raising collection, memory
or active-call limits.

## Standard library signatures

These are the complete function signatures defined in the thirteen bundled
libraries. Follow chapter APIs for supported application-facing helpers; some
prefixed functions are implementation helpers. Read source for structs and
exact status/lifetime contracts. [Math](21-math.md), [decimal input](22-math-input.md),
[text builders](20-text-builder.md) and [OS APIs](18-system.md) document application contracts.

### bytes.ramos

[Read the source](../stdlib/bytes.ramos).

```ramos
fn bytes_copy(source: bytes) -> bytes
fn bytes_equal(a: bytes, b: bytes) -> bool
fn bytes_slice(source: bytes, start: int64, end: int64) -> bytes
fn bytes_put(out: bytes, start: int64, source: bytes)
fn bytes_find(haystack: bytes, needle: bytes) -> int64
```

### cli.ramos

[Read the source](../stdlib/cli.ramos).

```ramos
fn cli_arg(index: int64) -> string
fn cli_has(name: string) -> bool
fn cli_value(name: string, fallback: string) -> string
fn cli_fail(message: string)
```

### gui.ramos

[Read the source](../stdlib/gui.ramos).

```ramos
fn gui_word(out: bytes, at: int64, value: int64)
fn gui_number(raw: bytes, at: int64) -> int64
fn gui_check(status: int64)
fn gui_open(title: string, width: int64, height: int64) -> int64
fn gui_close() -> int64
fn gui_rgb(red: int64, green: int64, blue: int64) -> int64
fn gui_properties(kind: int64, id: int64, x: int64, y: int64, width: int64, height: int64, color: int64) -> bytes
fn gui_label(id: int64, x: int64, y: int64, width: int64, height: int64, text: string)
fn gui_button(id: int64, x: int64, y: int64, width: int64, height: int64, text: string)
fn gui_input(id: int64, x: int64, y: int64, width: int64, height: int64, text: string)
fn gui_editor(id: int64, x: int64, y: int64, width: int64, height: int64, text: string)
fn gui_panel(id: int64, x: int64, y: int64, width: int64, height: int64, color: int64)
fn gui_set(id: int64, text: string)
fn gui_move(id: int64, x: int64, y: int64, width: int64, height: int64)
fn gui_text(id: int64) -> string
fn gui_event(timeout_ms: int64) -> GuiEvent
```

### io.ramos

[Read the source](../stdlib/io.ramos).

```ramos
fn io_reader(path: bytes) -> FileReader
fn io_close(reader: FileReader) -> int64
fn io_byte(reader: FileReader) -> int64
fn io_append(builder: ByteBuilder, value: int64)
fn io_line(reader: FileReader) -> bytes
fn io_copy(source: bytes, destination: bytes) -> int64
fn io_seek(reader: FileReader, offset: int64) -> int64
```

### lists.ramos

[Read the source](../stdlib/lists.ramos).

```ramos
fn list_new() -> IntList
fn list_len(list: IntList) -> int64
fn list_push(list: IntList, value: int64)
fn list_get(list: IntList, index: int64) -> int64
fn list_set(list: IntList, index: int64, value: int64)
fn list_pop(list: IntList) -> int64
fn list_clear(list: IntList)
```

### maps.ramos

[Read the source](../stdlib/maps.ramos).

```ramos
fn map_new() -> StringMap
fn map_len(map: StringMap) -> int64
fn map_index(map: StringMap, key: string) -> int64
fn map_has(map: StringMap, key: string) -> bool
fn map_get(map: StringMap, key: string, fallback: string) -> string
fn map_set(map: StringMap, key: string, value: string)
fn map_remove(map: StringMap, key: string) -> bool
```

### math.ramos

[Read the source](../stdlib/math.ramos).

```ramos
fn math_abs(value: float64) -> float64
fn math_min(a: float64, b: float64) -> float64
fn math_max(a: float64, b: float64) -> float64
fn math_clamp(value: float64, low: float64, high: float64) -> float64
fn math_sqrt(value: float64) -> float64
fn math_text(value: float64, places: int64) -> string
fn math_decimal_new(value: int64) -> MathMagnitude
fn math_decimal_copy(value: MathMagnitude) -> MathMagnitude
fn math_decimal_trim(value: MathMagnitude)
fn math_decimal_mul(value: MathMagnitude, factor: int64, add: int64)
fn math_decimal_shift(value: MathMagnitude, count: int64)
fn math_decimal_half(value: MathMagnitude)
fn math_decimal_compare(a: MathMagnitude, b: MathMagnitude) -> int64
fn math_decimal_sub(a: MathMagnitude, b: MathMagnitude)
fn math_decimal_bits(value: MathMagnitude) -> int64
fn math_decimal_digit(value: int64) -> bool
fn math_decimal_scale(value: int64, exponent: int64) -> float64
fn math_parse_bytes(text: bytes) -> FloatResult
fn math_parse(text: string) -> FloatResult
```

### numbers.ramos

[Read the source](../stdlib/numbers.ramos).

```ramos
fn num_min(a: int64, b: int64) -> int64
fn num_max(a: int64, b: int64) -> int64
fn num_abs(n: int64) -> int64
fn num_clamp(n: int64, low: int64, high: int64) -> int64
fn num_text(n: int64) -> string
fn num_parse(text: string) -> int64
```

### path.ramos

[Read the source](../stdlib/path.ramos).

```ramos
fn path_separator(value: int64) -> bool
fn path_absolute_bytes(path: bytes) -> bool
fn path_join_bytes(parent: bytes, child: bytes) -> bytes
fn path_name_bytes(path: bytes) -> bytes
fn path_join(parent: string, child: string) -> string
fn path_name(path: string) -> string
fn path_absolute(path: string) -> bool
```

### process.ramos

[Read the source](../stdlib/process.ramos).

```ramos
fn process_put(packet: ProcessPacket, value: int64)
fn process_raw(packet: ProcessPacket, text: bytes)
fn process_quote(packet: ProcessPacket, text: bytes)
fn process_run(executable: string, arguments: [string]) -> ProcessResult
```

### system.ramos

[Read the source](../stdlib/system.ramos).

```ramos
fn system_cwd() -> SystemValue
fn system_env(name: string) -> SystemValue
fn directory_open(path: bytes) -> Directory
fn directory_next(directory: Directory) -> DirectoryEntry
fn directory_close(directory: Directory) -> int64
fn directory_create(path: bytes) -> int64
```

### text.ramos

[Read the source](../stdlib/text.ramos).

```ramos
fn text_starts(text: string, prefix: string) -> bool
fn text_ends(text: string, suffix: string) -> bool
fn text_find(text: string, needle: string) -> int64
fn text_contains(text: string, needle: string) -> bool
fn text_join(parts: [string], separator: string) -> string
fn text_repeat(text: string, count: int64) -> string
fn text_builder() -> TextBuilder
fn text_builder_valid(builder: TextBuilder)
fn text_builder_bytes(builder: TextBuilder) -> int64
fn text_builder_append(builder: TextBuilder, text: string) -> int64
fn text_builder_finish(builder: TextBuilder) -> string
fn text_builder_clear(builder: TextBuilder)
fn text_builder_release(builder: TextBuilder)
```

### tui.ramos

[Read the source](../stdlib/tui.ramos).

```ramos
fn tui_escape() -> string
fn tui_write(value: string)
fn tui_control(value: string)
fn tui_begin() -> int64
fn tui_end() -> int64
fn tui_clear()
fn tui_move(row: int64, column: int64)
fn tui_color(foreground: int64, background: int64)
fn tui_reset()
fn tui_at(row: int64, column: int64, value: string)
fn tui_box(row: int64, column: int64, width: int64, height: int64)
fn tui_safe(value: bytes, width: int64) -> string
fn tui_key(timeout_ms: int64) -> int64
```
