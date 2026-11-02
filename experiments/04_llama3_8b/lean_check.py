"""Compile-check Lean 4 statements against a Mathlib project, many candidates per file.

Each candidate is wrapped in its own `namespace` so theorem names never clash; an error is charged
to the candidate whose line range holds it. A candidate passes when Lean reports no
`error` inside its range (the `sorry` warning is fine) and its sentinel `#print` still ran. Same criterion as ZIP-FIT's
get_list_lean4_syntax_errors(...) == [].
"""
import os, re, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor

ERR = re.compile(r"^[^:\n]+:(\d+):\d+: error", re.M)


def lean_env(mathlib_dir: str) -> dict:
    lp = [f"{mathlib_dir}/.lake/build/lib"]
    pk = f"{mathlib_dir}/.lake/packages"
    lp += [f"{pk}/{p}/.lake/build/lib" for p in sorted(os.listdir(pk))]
    return dict(os.environ, LEAN_PATH=":".join(lp))


HEADER_FALLBACKS = []  # (header, n_cands, first 400 chars of Lean output) for every task that needed the one-candidate-per-file fallback


def check_task(header_no_import: str, cands: list[str], lean_bin: str, mathlib_dir: str,
               timeout: int = 900) -> list[bool]:
    """Return one bool per candidate: True if it compiles with no error.

    Normally all candidates of a task share one Lean file. When Lean reports an error before the first candidate
    (a sample disturbed the shared header region), the task is rechecked one candidate per file, so one sample can
    never decide another's result; a candidate that still errors before its own start is counted as failing."""
    try:
        return _check_shared(header_no_import, cands, lean_bin, mathlib_dir, timeout)
    except RuntimeError as e:
        HEADER_FALLBACKS.append((header_no_import[:200], len(cands), str(e)[:400]))
        out = []
        for c in cands:
            try:
                out.append(_check_shared(header_no_import, [c], lean_bin, mathlib_dir, timeout)[0])
            except RuntimeError:
                out.append(False)
        return out


def _check_shared(header_no_import: str, cands: list[str], lean_bin: str, mathlib_dir: str,
                  timeout: int = 900) -> list[bool]:
    lines = ["import Mathlib", ""] + header_no_import.strip().split("\n") + [""]
    spans = []
    for i, c in enumerate(cands):
        lines.append(f"namespace cand_{i}")
        start = len(lines) + 1
        lines.extend(c.split("\n"))
        spans.append((start, len(lines)))
        lines.append(f"end cand_{i}")
        spans[-1] = (start, len(lines))  # the `end` line counts: an unfinished candidate errors there
        lines.append(f'#print "SENTINEL_{i}_OK"')  # missing in the output => candidate swallowed the rest (e.g. open comment)
        lines.append("")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, dir=os.environ.get("TMPDIR")) as f:
        f.write("\n".join(lines))
        path = f.name
    try:
        r = subprocess.run([lean_bin, path], capture_output=True, text=True, timeout=timeout,
                           env=lean_env(mathlib_dir))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return [False] * len(cands)
    finally:
        os.unlink(path)
    bad_lines = {int(m) for m in ERR.findall(out)}
    if any(ln < spans[0][0] - 1 for ln in bad_lines):
        raise RuntimeError(f"error in import/header, not in a candidate:\n{out[:800]}")
    return [(f"SENTINEL_{i}_OK" in out) and not any(s <= ln <= e for ln in bad_lines)
            for i, (s, e) in enumerate(spans)]


def check_all(items: list[tuple[str, list[str]]], lean_bin: str, mathlib_dir: str, workers: int = 16):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda it: check_task(it[0], it[1], lean_bin, mathlib_dir), items))
