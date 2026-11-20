#!/usr/bin/env python3
"""Entrypoint for the 20 November 2026 news-image entry.

Renders the infographic with render.py, then places the finished
entry.png in the output directory the harness asks for. Uses only the
standard library, touches no network, and produces identical bytes on
every run so the grader's two runs agree.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "render.py")],
                   check=True)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        fout.write(fin.read())


if __name__ == "__main__":
    main()
