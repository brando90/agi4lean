"""Compile-check Lean 4 statements against a Mathlib project, many candidates per file.

Each candidate is wrapped in its own namespace so names never clash (see check_task).
"""
import os, re, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor

ERR = re.compile(r"^[^:\n]+:(\d+):\d+: error", re.M)


def lean_env(mathlib_dir: str) -> dict:
    lp = [f"{mathlib_dir}/.lake/build/lib"]
    pk = f"{mathlib_dir}/.lake/packages"
    lp += [f"{pk}/{p}/.lake/build/lib" for p in sorted(os.listdir(pk))]
    return dict(os.environ, LEAN_PATH=":".join(lp))


def check_task(header_no_import: str, cands: list[str], lean_bin: str, mathlib_dir: str,
               timeout: int = 900):
    """Return one bool per candidate (True: compiles with no error), or None if Lean timed out.

    Each candidate sits in its own `namespace cand_i ... end cand_i` followed by `#print "SENTINEL_i_OK"`.
    It passes when no error line falls on its lines (the `end` line included, where an unfinished candidate
    errors) and its sentinel was printed (a missing sentinel means the candidate swallowed the rest, e.g. an
    open comment). Namespace + `end` line + sentinel follow the fix found in the Qwen3 reproduction.
    """
    lines = ["import Mathlib", ""] + header_no_import.strip().split("\n") + [""]
    spans = []
    for i, c in enumerate(cands):
        lines.append(f"namespace cand_{i}")
        start = len(lines) + 1
        lines.extend(c.split("\n"))
        lines.append(f"end cand_{i}")
        spans.append((start, len(lines)))
        lines.append(f'#print "SENTINEL_{i}_OK"')
        lines.append("")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, dir=os.environ.get("TMPDIR")) as f:
        f.write("\n".join(lines))
        path = f.name
    try:
        r = subprocess.run([lean_bin, path], capture_output=True, text=True, timeout=timeout,
                           env=lean_env(mathlib_dir))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return None  # caller splits the chunk
    finally:
        os.unlink(path)
    bad_lines = {int(m) for m in ERR.findall(out)}
    if any(ln < spans[0][0] - 1 for ln in bad_lines):
        return None  # an error before the first candidate: some candidate upsets the file; the caller bisects
    return [(f"SENTINEL_{i}_OK" in out) and not any(s <= ln <= e for ln in bad_lines)
            for i, (s, e) in enumerate(spans)]


def check_chunked(header, cands, lean_bin, mathlib_dir, chunk=20, timeout=90):
    """check_task in chunks; a chunk that times out (or upsets the header lines) is split in halves, a single such candidate fails."""
    out = []
    for i in range(0, len(cands), chunk):
        part = cands[i:i + chunk]
        r = check_task(header, part, lean_bin, mathlib_dir, timeout)
        if r is None:
            if len(part) == 1:
                r = [False]
            else:
                h = len(part) // 2
                r = check_chunked(header, part[:h], lean_bin, mathlib_dir, max(h, 1), max(30, timeout // 2)) + \
                    check_chunked(header, part[h:], lean_bin, mathlib_dir, max(len(part) - h, 1), max(30, timeout // 2))
        out += r
    return out


def check_all(items: list[tuple[str, list[str]]], lean_bin: str, mathlib_dir: str, workers: int = 16):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda it: check_task(it[0], it[1], lean_bin, mathlib_dir), items))
