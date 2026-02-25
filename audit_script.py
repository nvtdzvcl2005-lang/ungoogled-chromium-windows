import os, re

SRC = "build/src/third_party/blink/renderer"
OUT = "audit_result.txt"

# Danh sach can tim: (ten_hien_thi, pattern_regex, mo_ta)
TARGETS = [
    # Canvas 2D
    ("canvas_toDataURL",    r"toDataURL\s*\(",           "Canvas fingerprint - toDataURL"),
    ("canvas_toBlob",       r"toBlob\s*\(",              "Canvas fingerprint - toBlob"),
    ("getImageData",        r"getImageData\s*\(",        "Canvas fingerprint - getImageData"),

    # Audio
    ("getFloatFrequencyData",  r"getFloatFrequencyData\s*\(",   "AudioContext fingerprint"),
    ("getByteFrequencyData",   r"getByteFrequencyData\s*\(",    "AudioContext fingerprint"),
    ("getFloatTimeDomainData", r"getFloatTimeDomainData\s*\(",  "AudioContext fingerprint"),

    # Screen
    ("screen_width",        r"Screen::width\b",          "Screen width"),
    ("screen_height",       r"Screen::height\b",         "Screen height"),
    ("screen_availWidth",   r"availWidth\s*\(",           "Screen availWidth"),
    ("screen_availHeight",  r"availHeight\s*\(",          "Screen availHeight"),
    ("screen_colorDepth",   r"colorDepth\s*\(",           "Screen colorDepth"),

    # Platform / UA
    ("platform",            r"NavigatorID::platform\s*\(",     "navigator.platform"),
    ("vendor",              r"NavigatorID::vendor\s*\(",       "navigator.vendor"),
    ("userAgent",           r"NavigatorID::userAgent\s*\(",    "navigator.userAgent"),

    # Timezone
    ("timezone_offset",     r"getTimezoneOffset\s*\(",         "Date.getTimezoneOffset"),

    # Connection
    ("effectiveType",       r"effectiveType\s*\(",             "navigator.connection.effectiveType"),
    ("connection_type",     r"NetworkInformation::type\s*\(",  "navigator.connection.type"),

    # WebRTC
    ("createOffer",         r"RTCPeerConnection::createOffer\s*\(",  "WebRTC - co the leak IP"),

    # Permissions
    ("permissions_query",   r"PermissionStatus::state\s*\(",   "navigator.permissions"),
]

results = []
results.append("QUET TOAN BO BLINK - AUDIT FINGERPRINT")
results.append("="*60)
results.append("")

total = 0

for (name, pattern, desc) in TARGETS:
    results.append(f"{'='*60}")
    results.append(f"TIM: {name}  ({desc})")
    results.append(f"{'='*60}")

    found_in_target = 0

    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d not in ("tests", "testing", "test")]

        for fname in files:
            if not fname.endswith(".cc"):
                continue

            fpath = os.path.join(root, fname)
            try:
                lines = open(fpath, encoding="utf-8", errors="replace").readlines()
            except:
                continue

            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith("//"):
                    continue
                if re.search(pattern, line):
                    start   = max(0, i - 2)
                    end     = min(len(lines), i + 35)
                    snippet = "".join(lines[start:end])
                    rel     = os.path.relpath(fpath, "build/src")

                    results.append(f"--- {fname} | dong {i+1} ---")
                    results.append(f"PATH: {rel}")
                    results.append(snippet)
                    results.append("")
                    found_in_target += 1
                    total += 1

    if found_in_target == 0:
        results.append("KHONG TIM THAY")
        results.append("")

results.append("="*60)
results.append(f"TONG KET: {total} ket qua")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"XONG! {total} ket qua. Luu vao {os.path.abspath(OUT)}")
