import os, re

SRC   = "build/src/third_party/blink/renderer"
OUT   = "audit_result.txt"

KEYWORDS = {
    "maxTouchPoints": r"maxTouchPoints\s*\(",
}

results = []
results.append("QUET TOAN BO BLINK TIM maxTouchPoints")
results.append("="*60)
results.append("")

found_count = 0

for root, dirs, files in os.walk(SRC):
    # Bo qua thu muc test de giam nhieu
    dirs[:] = [d for d in dirs if d not in ("tests", "testing", "test")]

    for fname in files:
        if not fname.endswith(".cc"):
            continue

        fpath = os.path.join(root, fname)
        try:
            lines = open(fpath, encoding="utf-8", errors="replace").readlines()
        except:
            continue

        for keyword, pattern in KEYWORDS.items():
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Bo qua comment
                if stripped.startswith("//"):
                    continue
                if re.search(pattern, line):
                    start   = max(0, i - 2)
                    end     = min(len(lines), i + 35)
                    snippet = "".join(lines[start:end])
                    rel     = os.path.relpath(fpath, "build/src")

                    results.append(f"=== {fname} | {keyword} | dong {i+1} ===")
                    results.append(f"PATH: {rel}")
                    results.append(snippet)
                    results.append("--- HET DOAN ---")
                    results.append("")
                    found_count += 1

results.append("="*60)
results.append(f"TONG KET: Tim thay {found_count} cho co maxTouchPoints")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"XONG! Tim thay {found_count} cho. Luu vao {os.path.abspath(OUT)}")
