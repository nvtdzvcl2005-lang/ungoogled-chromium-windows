import os, re

SRC = "build/src"
OUT = "audit_result.txt"

targets = [
    ("third_party/blink/renderer/core/frame/navigator_concurrent_hardware.cc",     "hardwareConcurrency"),
    ("third_party/blink/renderer/core/execution_context/navigator_base.cc",         "hardwareConcurrency"),
    ("third_party/blink/renderer/modules/touch_events/navigator_touch_points.cc",   "maxTouchPoints"),
    ("third_party/blink/renderer/core/frame/navigator.cc",                          "maxTouchPoints"),
    ("third_party/blink/renderer/core/frame/navigator_device_memory.cc",            "deviceMemory"),
    ("third_party/blink/renderer/core/frame/local_dom_window.cc",                   "devicePixelRatio"),
    ("third_party/blink/renderer/core/frame/screen.cc",                             "devicePixelRatio"),
    ("third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc",    "getParameter"),
    ("third_party/blink/renderer/core/frame/navigator_language.cc",                 "language"),
    ("third_party/blink/renderer/modules/battery/battery_manager.cc",               "level"),
]

results = []

for rel_path, keyword in targets:
    full_path = os.path.join(SRC, rel_path)
    filename  = os.path.basename(rel_path)

    if not os.path.exists(full_path):
        results.append("=== " + filename + " | " + keyword + " ===")
        results.append("FILE KHONG TON TAI")
        results.append("")
        continue

    lines = open(full_path, encoding="utf-8", errors="replace").readlines()
    found = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.search(re.escape(keyword) + r"\s*\(", line) and not stripped.startswith("//"):
            start   = max(0, i - 3)
            end     = min(len(lines), i + 40)
            snippet = "".join(lines[start:end])
            results.append("=== " + filename + " | " + keyword + " | dong " + str(i+1) + " ===")
            results.append(snippet)
            results.append("--- HET DOAN ---")
            results.append("")
            found = True

    if not found:
        results.append("=== " + filename + " | " + keyword + " ===")
        results.append("KHONG TIM THAY KEYWORD")
        results.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("DA GHI:", os.path.abspath(OUT))
