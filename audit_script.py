import os, re, time

SRC  = "build/src/third_party/blink/renderer"
OUT  = "audit_result.txt"
MAX_SECONDS = 10800  # 3 tieng
start = time.time()

# (ten, pattern, mo_ta, uu_tien)
# uu_tien 1=cao nhat, 3=thap nhat
TARGETS = [
    # ── CANVAS ──────────────────────────────────────────────
    ("toDataURL",               r"HTMLCanvasElement::toDataURL\b",              "Canvas hash - toDataURL",              1),
    ("toBlob",                  r"HTMLCanvasElement::toBlob\b",                 "Canvas hash - toBlob",                 1),
    ("getImageDataInternal",    r"getImageDataInternal\s*\(",                   "Canvas hash - getImageData internal",  1),
    ("SnapshotInternal",        r"SnapshotInternal\s*\(",                       "Canvas snapshot internal",             1),
    ("ToDataURLInternal",       r"ToDataURLInternal\s*\(",                      "Canvas ToDataURLInternal",             1),

    # ── AUDIO ────────────────────────────────────────────────
    ("GetFloatFrequencyData",   r"GetFloatFrequencyData\s*\(",                  "Audio - analyser handler",             1),
    ("GetByteFrequencyData",    r"GetByteFrequencyData\s*\(",                   "Audio - analyser handler",             1),
    ("GetFloatTimeDomainData",  r"GetFloatTimeDomainData\s*\(",                 "Audio - analyser handler",             1),

    # ── SCREEN ───────────────────────────────────────────────
    ("Screen_width",            r"Screen::width\(\)",                           "screen.width",                         1),
    ("Screen_height",           r"Screen::height\(\)",                          "screen.height",                        1),
    ("Screen_availWidth",       r"Screen::availWidth\(\)",                      "screen.availWidth",                    1),
    ("Screen_availHeight",      r"Screen::availHeight\(\)",                     "screen.availHeight",                   1),
    ("Screen_colorDepth",       r"Screen::colorDepth\(\)",                      "screen.colorDepth",                    1),

    # ── PLATFORM / UA ────────────────────────────────────────
    ("NavigatorID_platform",    r"NavigatorID::platform\(\)\s*const\s*\{",      "navigator.platform impl",              1),
    ("NavigatorID_vendor",      r"NavigatorID::vendor\(\)",                     "navigator.vendor",                     1),
    ("NavigatorID_userAgent",   r"NavigatorID::userAgent\(\)",                  "navigator.userAgent",                  1),
    ("appVersion",              r"NavigatorID::appVersion\(\)",                 "navigator.appVersion",                 2),

    # ── FONTS ────────────────────────────────────────────────
    ("EnumerateFonts",          r"EnumerateFonts\s*\(",                         "Font enumeration",                     1),
    ("queryLocalFonts",         r"queryLocalFonts\s*\(",                        "queryLocalFonts API",                  1),
    ("getFontFaceSet",          r"getFontFaceSet\s*\(",                         "FontFaceSet",                          2),

    # ── WEBRTC ───────────────────────────────────────────────
    ("RTCPeerConnection_ctor",  r"RTCPeerConnection::RTCPeerConnection\b",      "WebRTC constructor - IP leak point",   1),
    ("AddIceCandidate",         r"RTCPeerConnection::addIceCandidate\b",        "WebRTC ICE candidate",                 1),
    ("OnIceCandidate",          r"OnIceCandidate\s*\(",                         "WebRTC ICE callback",                  1),

    # ── CLIENT RECTS ─────────────────────────────────────────
    ("getBoundingClientRect",   r"getBoundingClientRect\s*\(",                  "ClientRects fingerprint",              2),
    ("getClientRects",          r"Element::getClientRects\b",                   "ClientRects list",                     2),

    # ── SPEECH ───────────────────────────────────────────────
    ("getVoices",               r"SpeechSynthesis::getVoices\b",                "Speech voices list",                   2),
    ("SpeechSynthesisVoice",    r"SpeechSynthesisVoice::name\b",                "Speech voice name",                    2),

    # ── PLUGINS / MIMETYPES ──────────────────────────────────
    ("PluginArray_item",        r"PluginArray::item\b",                         "navigator.plugins",                    2),
    ("MimeTypeArray_item",      r"MimeTypeArray::item\b",                       "navigator.mimeTypes",                  2),
    ("PluginArray_length",      r"PluginArray::length\b",                       "navigator.plugins.length",             2),

    # ── TIMEZONE ─────────────────────────────────────────────
    ("getTimezoneOffset",       r"getTimezoneOffset\s*\(",                      "Date.getTimezoneOffset",               1),
    ("DateTimeFormat_timezone", r"resolvedOptions\s*\(",                        "Intl timezone",                        1),
    ("V8LocalTime",             r"LocalTimeOffset\s*\(",                        "V8 local time offset",                 1),

    # ── NETWORK ──────────────────────────────────────────────
    ("effectiveType",           r"NetworkInformation::effectiveType\(\)",       "connection.effectiveType",             2),
    ("downlink",                r"NetworkInformation::downlink\(\)",            "connection.downlink",                  2),
    ("rtt",                     r"NetworkInformation::rtt\(\)",                 "connection.rtt",                       2),

    # ── MISC NAVIGATOR ───────────────────────────────────────
    ("cookieEnabled",           r"NavigatorBase::cookieEnabled\b",              "navigator.cookieEnabled",              3),
    ("doNotTrack",              r"Navigator::doNotTrack\b",                     "navigator.doNotTrack",                 3),
    ("pdfViewerEnabled",        r"Navigator::pdfViewerEnabled\b",               "navigator.pdfViewerEnabled",           3),
    ("webdriver",               r"Navigator::webdriver\b",                      "navigator.webdriver - QUAN TRONG",     1),
    ("permissions_state",       r"PermissionStatus::state\(\)",                 "permissions.query state",              2),

    # ── CSS MEDIA ────────────────────────────────────────────
    ("matchMedia",              r"LocalDOMWindow::matchMedia\b",                "window.matchMedia",                    2),
    ("prefers_color_scheme",    r"prefers.color.scheme",                        "prefers-color-scheme media query",     2),

    # ── PERFORMANCE ──────────────────────────────────────────
    ("performance_now",         r"Performance::now\b",                          "performance.now timing",               2),
    ("timeOrigin",              r"Performance::timeOrigin\b",                   "performance.timeOrigin",               3),
]

results = []
results.append("AUDIT FINGERPRINT DAY DU - CHROMIUM 145")
results.append(f"Tong so target: {len(TARGETS)}")
results.append("="*60)
results.append("")

total_found = 0
skipped = 0

for (name, pattern, desc, priority) in TARGETS:
    elapsed = time.time() - start
    if elapsed > MAX_SECONDS:
        results.append(f"HET GIO 3 TIENG! Da quet {name} -> dung lai")
        skipped += 1
        continue

    results.append(f"{'='*60}")
    results.append(f"[P{priority}] {name}  ({desc})")
    results.append(f"{'='*60}")

    found_here = 0

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
                if line.strip().startswith("//"):
                    continue
                if re.search(pattern, line):
                    start_l = max(0, i - 2)
                    end_l   = min(len(lines), i + 45)
                    snippet = "".join(lines[start_l:end_l])
                    rel     = os.path.relpath(fpath, "build/src")

                    results.append(f"--- {fname} | dong {i+1} ---")
                    results.append(f"PATH: {rel}")
                    results.append(snippet)
                    results.append("")
                    found_here += 1
                    total_found += 1

    if found_here == 0:
        results.append("KHONG TIM THAY")
        results.append("")

    elapsed = time.time() - start
    print(f"[{int(elapsed)}s] {name}: {found_here} ket qua")

results.append("="*60)
results.append(f"TONG KET: {total_found} ket qua, {skipped} target bi bo qua do het gio")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"\nXONG! {total_found} ket qua. File: {os.path.abspath(OUT)}")
