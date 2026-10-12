# Working with bytes

```text
fn main() {
    let source = "let answer = 42"
    print(buffer_len(source))
    print(buffer_get(source, 0))
    buffer_set(source, 0, 76)
    print(source)
}
```

`buffer(length)` allocates zero-filled bytes. `buffer_len`, `buffer_get`, and
`buffer_set` provide length, checked reads, and checked writes. Indices count
bytes; reads return 0..255 and writes accept only that range. String literals
in expressions allocate fresh buffers. Bindings and function values alias their
buffer; `let` protects the binding while allowing content changes.

Buffers share the reclaiming heap with strings, structs and arrays: 16 MiB of
allocated blocks plus an 8 MiB ownership map, and at most 1 MiB per payload.
Metadata and alignment count toward the heap limit. Invalid sizes, indices,
byte values or allocation failures report a runtime error and exit 1.
Unreachable allocations can be collected automatically or with `collect()`.
See [buffer semantics](https://github.com/zackmsa777-a11y/ramos/blob/d496ba4eb84d11152100d258df0464bea4a405bf/docs/buffers.md).

## Bytes versus strings

`"abc"` is mutable bytes. `s"abc"` is an immutable UTF-8 string. A byte index
is not a Unicode scalar index. Use `string(bytes)` to validate and copy into a
string, and `to_bytes(string)` to produce an independent mutable copy.

For binary or arbitrary Linux file data, keep bytes. Converting malformed UTF-8
to a string traps. `print(bytes)` adds LF; `stdout(bytes)` writes exactly the
bytes and returns a fallible status. Check the result before continuing.

```ramos
fn main() {
    let raw = "cat"
    buffer_set(raw, 0, 98)
    print(raw)
    let immutable = string(raw)
    buffer_set(raw, 0, 114)
    print(immutable)
}
```

Output is `bat`, then `bat`: conversion copied the data before the second edit.
Use [the bytes library](07-libraries.md) for slicing and copying helpers.
