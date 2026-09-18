#!/usr/bin/env python3
"""LintCat helper: generate CrashReport annotation sources.

Mimics the build system's ``pre-export`` GeneratedFile step defined in
``mobile/android/moz.build`` (script: toolkit/crashreporter/annotations/generate.py).

This produces the sources that Gradle expects under objdir, e.g.:
  objdir/mobile/android/android-components/components/lib/crash/src/main/java/
      mozilla/components/lib/crash/service/CrashReport.kt
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ = os.environ.get("OBJ", os.path.join(ROOT, "obj-aarch64-unknown-linux-android"))
VALIDATED = os.path.join(
    OBJ, "toolkit", "crashreporter", "annotations", "validated.yaml"
)
OUTPUTS = [
    "mobile/android/android-components/components/lib/crash/src/main/java/mozilla/components/lib/crash/service/CrashReport.kt",
    "mobile/android/geckoview/src/main/java/org/mozilla/geckoview/CrashReport.java",
]

sys.path.insert(0, os.path.join(ROOT, "toolkit", "crashreporter", "annotations"))
import load as crash_load  # noqa: E402
import generate  # noqa: E402


def main():
    # Step 1: produce validated.yaml (same as GeneratedFile("validated.yaml", script="load.py"))
    os.makedirs(os.path.dirname(VALIDATED), exist_ok=True)
    with open(VALIDATED, "w", encoding="utf-8") as f:
        crash_load.main(f)
    print("generated:", VALIDATED)

    # Step 2: produce CrashReport sources using validated.yaml
    for rel in OUTPUTS:
        out_path = os.path.join(OBJ, rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            generate.main(f, VALIDATED)
        print("generated:", out_path)
    print("DONE")


if __name__ == "__main__":
    main()