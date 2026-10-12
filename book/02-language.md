# The language

## Syntax

```text
fn main() {
    let price = 20
    var count = 3
    print(price * count)

    count = count + 2
    print("Updated total:")
    print(price * count)
}
```

- Exactly one parameterless `main` returning void is required. Other top-level
  functions and structs may appear before or after it. `weave` adds library
  definitions at top level.
- `print` accepts a string literal, buffer, integer, float64 or boolean expression
  and adds a newline. Booleans print as `true` or `false`; floats use six fractional digits.
- Integer expressions support `+`, `-`, `*`, `/`, `%`, unary `+`/`-`, and
  parentheses. Multiplication, division, and remainder bind more tightly than
  addition and subtraction. Binary operators at the same precedence associate
  left to right.
- Integers range from `-9223372036854775808` to `9223372036854775807`.
  `-9223372036854775808` is accepted as a directly negated literal; its positive
  magnitude cannot be used as an ordinary positive literal.
- `let` declares an immutable binding; `var` declares a mutable
  binding. Every binding must have an initializer. `int64`, `float64`, `bool`, `bytes`, `string`, struct and array types
  are inferred and fixed for the lifetime of the binding.
- Binding reassignment is supported only for `var`; fields and array elements can be mutated through `let`. Names must be declared before use;
  duplicate declarations in the same block are errors. Inner blocks may
  shadow outer names, and their bindings are invisible after the block ends.
  Identifiers use ASCII letters,
  underscores, and digits, with a letter or underscore first. Keywords are
  reserved. `"..."` produces bytes; `s"..."` produces immutable UTF-8 strings.
- Separate statements with newlines; the final statement may directly precede
  `}`. Newlines after operators and opening parentheses are allowed. Semicolons
  are not implemented. Comments use `//` or non-nesting `/* ... */`; newlines
  in block comments retain their statement-separator meaning.
- Input is UTF-8. String escapes are `\n`, `\t`, `\r`, `\"`, `\\`, and `\0`.
- Empty bodies, empty strings, LF, and CRLF are supported.
- Raw NUL source bytes, malformed UTF-8, unsupported escapes, and raw newlines inside
  strings are rejected. Diagnostics contain filename, line, and byte column.

## Booleans and control flow

```text
fn main() {
    var running = true
    var count = 0
    while running {
        count = count + 1
        if count == 5 {
            running = false
        } else {
            print(count)
        }
    }
    print(!running)
}
```

- `true` and `false` are distinct boolean literals; `!` negates a boolean.
- `<`, `<=`, `>`, and `>=` compare two signed integers or two floats. `==` and `!=` compare
  two integers, two floats, two booleans or two strings. Mixing types is a compile-time error.
- `&&` and `||` require booleans and short-circuit left to right; skipped operands
  still undergo type checking.
- From lowest to highest precedence: `||`, `&&`, equality, ordering, addition/subtraction,
  multiplication/division/remainder, unary signs/`!`, and primary expressions.
  Operators at one level associate left to right. `1 < 2 < 3` is rejected;
  combine pairwise comparisons with `&&`. Arithmetic requires matching numeric types; `+` also concatenates strings.
- `if condition { ... } else { ... }` and `while condition { ... }` require
  a boolean condition. `else` is optional and may follow on a new line.
  Branches use braces; `else if` chains test later conditions only when prior arms fail.
- `while` reevaluates its condition before every iteration. `break` exits the
  innermost loop; `continue` reevaluates its condition. Both require a loop.
  `while true` runs until a `break` or a runtime failure; there is no implicit
  iteration limit. Code in skipped branches is type-checked but not executed.
- Bindings initialize whenever execution reaches their declaration. A shadowing
  initializer can refer to the outer binding. Blocks do not expose their locals.
- `for name in start..end { ... }` evaluates int64 bounds once, then counts
  upward with an excluded end. The counter is immutable and local to the body;
  empty/reversed ranges do not run. `break`/`continue` target the innermost loop.
- `+=` accepts int64/float64/string, `-=` accepts int64/float64, and both are statements with
  matching operand types. Destinations and indices evaluate once, before the RHS.
  Bindings require `var`; fields/elements retain mutation through `let`.
  Separate statements with newlines, including after a compound statement.

Run `make control-flow` for a native Fibonacci/loop example.

## Functions

```text
fn factorial(n: int64) -> int64 {
    if n == 0 {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}

fn main() {
    print(factorial(10))
    announce()
}

fn announce() {
    print("Functions work!")
}
```

Parameters require non-void type annotations and their bindings are immutable.
Results can declare any value type or `void`; omitting the result means void.
Calls evaluate arguments left to right and require exactly matching types and
argument counts. Functions may call later definitions, themselves or each other.
A lexical binding can shadow a function name; that name then cannot be called.
`main` is the process entry and cannot be called by user code.

`return expression` must match the declared value type; bare `return` is for void
functions, including `main`. A value function must return on every statically
checked path. Both arms of an `if`/`else` may establish that guarantee. Loops are
checked conservatively, so even a `while true` needs a return after it for a
value function. Unreachable statements are still type-checked. Void calls may
be statements; value calls used as statements discard their result.

Every call has its own local frame. At most 1,024 Ramos calls may be active,
including `main`; attempting the next call reports a runtime error and exits 1.
Normal returns release the frame and restore the active-call counter.
A separate 4 MiB [stack budget](25-stack.md) is checked before each frame;
use an OS stack of at least 8 MiB. This
check assumes an ordinary Linux process stack; it cannot compensate for an
unusually small stack limit selected by the caller.

Run `make functions` for factorial, a digit classifier and a void helper.
See [the native calling convention](https://github.com/zackmsa777-a11y/ramos/blob/d496ba4eb84d11152100d258df0464bea4a405bf/docs/functions.md) for compiler details.

## Arithmetic behavior

The overflow rules below apply to int64. [Float64](21-math.md) uses a finite-value
policy, explicit conversions and gradual underflow.

Generated native instructions check signed overflow for addition, subtraction,
multiplication, and negation. Division truncates toward zero; a remainder has the
dividend's sign. Division or remainder by zero, and either operation on
`INT64_MIN` with divisor `-1`, fail explicitly.

A failed arithmetic operation writes a runtime diagnostic to stderr and exits
with status 1. It never silently wraps or depends on an unhandled CPU divide
fault. Successfully completed programs exit with status 0. Earlier output is
retained if a later operation fails.
