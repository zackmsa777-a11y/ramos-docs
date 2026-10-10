# Performance and evidence

Ramos 0.7.1 has a reproducible eight-task comparison with optimized checked C,
Rust and CPython. On the recorded Linux VM, the execution index is **Ramos 40.82,
C 100, Rust 119.77 and Python 2.53** (higher is faster). Ramos is **16.16× faster
than Python** across this suite and takes **2.45× C's time**. These are geometric
means of per-task median ratios, not a general language ranking.

The suite checks outputs against independent references, runs nine randomized
samples per task, and records raw timings, build commands and source hashes.
Startup and build times are reported separately. See the
[full report and methodology](https://github.com/zackmsa777-a11y/ramos/blob/c94ff2d1cd9211e63e2466f053de21d3b7ad3955/benchmarks/report.md), [raw samples](../evidence/results.json)
and [workload sources](https://github.com/zackmsa777-a11y/ramos/blob/c94ff2d1cd9211e63e2466f053de21d3b7ad3955/benchmarks/fixtures). The saved 0.7.0 baseline and
[interleaved old/new comparison](https://github.com/zackmsa777-a11y/ramos/blob/c94ff2d1cd9211e63e2466f053de21d3b7ad3955/benchmarks/optimization.md) show a **2.05× overall
speedup**. Version 0.8 emits [identical benchmark executable bytes](../evidence/codegen-continuity.json)
for both targets. Versions 0.9–0.11 expand the native runtime; the timings above
remain the recorded 0.7.1 measurements, not a current-version performance claim.

```sh
make
python3 benchmarks/run_suite.py                 # measure all eight tasks
python3 benchmarks/run_suite.py --validate-only # output checks without timing
```



The [historical 0.2 comparison](https://github.com/zackmsa777-a11y/ramos/blob/c94ff2d1cd9211e63e2466f053de21d3b7ad3955/benchmarks/report-0.2.md) used another machine
and one unrolled workload; it is not directly comparable. Its legacy script
still requires the 0.2 compiler and writes to `work/results-0.2` by default.

## Read the results correctly

The 0.7.1 index is historical, not a speed measurement of Ramos 0.13. C is
normalized to 100; higher is faster on the recorded workloads. The historical
Ramos score of 40.82 means roughly 2.45 times C's execution time on that suite,
not 2.45 times faster than C. It says nothing about all possible programs.

The development roadmap requires fresh measurements before new release speed
claims. Run benchmark commands from the compiler repository, where the harness
and workload sources live, rather than from this documentation repository.
