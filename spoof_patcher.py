import os, re, sys

SRC_ROOT = "build/src"
HEADER = '#include "base/command_line.h"\n'

def patch_file(label, rel_path, search_pattern, inject_code, marker):
    full_path = os.path.join(SRC_ROOT, rel_path)
    filename  = os.path.basename(rel_path)

    if not os.path.exists(full_path):
        print(f"  [X] FILE KHONG TON TAI: {rel_path}")
        return False

    content = open(full_path, encoding="utf-8").read()

    if marker in content:
        print(f"  [v] DA VAP ROI: {filename}")
        return True

    match = re.search(search_pattern, content)
    if not match:
        print(f"  [X] KHONG TIM THAY PATTERN: {label} trong {filename}")
        return False

    insert_pos = match.end()

    if HEADER not in content:
        content = HEADER + content
        insert_pos += len(HEADER)

    content = content[:insert_pos] + "\n  " + inject_code + "\n" + content[insert_pos:]
    open(full_path, "w", encoding="utf-8").write(content)
    print(f"  [+] VAP THANH CONG: {label}")
    return True


print("\n" + "="*60)
print("SPOOF PATCHER - Chromium 145 - Full Edition")
print("="*60)


# ============================================================
# 1. hardwareConcurrency
# FILE: navigator_concurrent_hardware.cc
# ============================================================
print("\n[1] hardwareConcurrency")
patch_file(
    "hardwareConcurrency",
    "third_party/blink/renderer/core/frame/navigator_concurrent_hardware.cc",
    r"NavigatorConcurrentHardware::hardwareConcurrency\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return static_cast<unsigned>(std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency")));',
    'HasSwitch("fingerprint-hardware-concurrency")'
)


# ============================================================
# 2. deviceMemory
# FILE: navigator_device_memory.cc
# ============================================================
print("\n[2] deviceMemory")
patch_file(
    "deviceMemory",
    "third_party/blink/renderer/core/frame/navigator_device_memory.cc",
    r"NavigatorDeviceMemory::deviceMemory\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));',
    'HasSwitch("fingerprint-device-memory")'
)


# ============================================================
# 3. devicePixelRatio
# FILE: local_dom_window.cc
# ============================================================
print("\n[3] devicePixelRatio")
patch_file(
    "devicePixelRatio",
    "third_party/blink/renderer/core/frame/local_dom_window.cc",
    r"LocalDOMWindow::devicePixelRatio\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stod(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));',
    'HasSwitch("fingerprint-device-scale-factor")'
)


# ============================================================
# 4. WebGL getParameter
# FILE: webgl_rendering_context_base.cc
# ============================================================
print("\n[4] WebGL getParameter")
patch_file(
    "WebGL getParameter",
    "third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc",
    r"WebGLRenderingContextBase::getParameter\(ScriptState\*\s*script_state,\s*GLenum\s*pname\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return WebGLAny(script_state, String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor"))); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return WebGLAny(script_state, String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer")));',
    'HasSwitch("fingerprint-webgl-vendor")'
)


# ============================================================
# 5. language
# FILE: navigator_language.cc
# ============================================================
print("\n[5] language")
patch_file(
    "language",
    "third_party/blink/renderer/core/frame/navigator_language.cc",
    r"NavigatorLanguage::language\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return AtomicString::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang").c_str());',
    'HasSwitch("fingerprint-lang")'
)


# ============================================================
# 6. battery level
# FILE: battery_manager.cc
# ============================================================
print("\n[6] battery level")
patch_file(
    "battery level",
    "third_party/blink/renderer/modules/battery/battery_manager.cc",
    r"BatteryManager::level\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stod(cmd->GetSwitchValueASCII("fingerprint-battery-level"));',
    'HasSwitch("fingerprint-battery-level")'
)


# ============================================================
# 7. maxTouchPoints
# FILE: navigator_events.cc
# ============================================================
print("\n[7] maxTouchPoints")
patch_file(
    "maxTouchPoints",
    "third_party/blink/renderer/core/events/navigator_events.cc",
    r"NavigatorEvents::maxTouchPoints\(Navigator&\s*\w+\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return static_cast<int32_t>(std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points")));',
    'HasSwitch("fingerprint-max-touch-points")'
)


# ============================================================
# 8-11. Screen width/height/availWidth/availHeight
# FILE: screen.cc
# ============================================================
print("\n[8] screen.width")
patch_file(
    "screen.width",
    "third_party/blink/renderer/core/frame/screen.cc",
    r"Screen::width\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));',
    'HasSwitch("fingerprint-screen-width")'
)

print("\n[9] screen.height")
patch_file(
    "screen.height",
    "third_party/blink/renderer/core/frame/screen.cc",
    r"Screen::height\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-height")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-height"));',
    'HasSwitch("fingerprint-screen-height")'
)

print("\n[10] screen.availWidth")
patch_file(
    "screen.availWidth",
    "third_party/blink/renderer/core/frame/screen.cc",
    r"Screen::availWidth\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-avail-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-avail-width"));',
    'HasSwitch("fingerprint-screen-avail-width")'
)

print("\n[11] screen.availHeight")
patch_file(
    "screen.availHeight",
    "third_party/blink/renderer/core/frame/screen.cc",
    r"Screen::availHeight\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-avail-height")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-avail-height"));',
    'HasSwitch("fingerprint-screen-avail-height")'
)


# ============================================================
# 12. screen.colorDepth
# FILE: screen.cc
# pixelDepth tu dong theo vi no goi colorDepth()
# ============================================================
print("\n[12] screen.colorDepth")
patch_file(
    "screen.colorDepth",
    "third_party/blink/renderer/core/frame/screen.cc",
    r"Screen::colorDepth\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-color-depth")) return static_cast<unsigned>(std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-color-depth")));',
    'HasSwitch("fingerprint-screen-color-depth")'
)


# ============================================================
# 13. navigator.platform
# FILE: navigator_id.cc
# Inject truoc #if BUILDFLAG de override het moi platform
# ============================================================
print("\n[13] navigator.platform")
patch_file(
    "navigator.platform",
    "third_party/blink/renderer/core/frame/navigator_id.cc",
    r"NavigatorID::platform\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-platform")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-platform"));',
    'HasSwitch("fingerprint-platform")'
)


# ============================================================
# 14. navigator.webdriver - QUAN TRONG NHAT
# FILE: navigator.cc
# Patch de tra ve false, an dau hieu automation
# ============================================================
print("\n[14] navigator.webdriver")
patch_file(
    "navigator.webdriver",
    "third_party/blink/renderer/core/frame/navigator.cc",
    r"Navigator::webdriver\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-disable-webdriver")) return false;',
    'HasSwitch("fingerprint-disable-webdriver")'
)


# ============================================================
# 15. Audio - GetFloatFrequencyData
# FILE: realtime_analyser.cc
# Inject SAU khi data da duoc fill vao destination
# Pattern: tim doan ket thuc for loop ghi destination[i]
# ============================================================
print("\n[15] audio GetFloatFrequencyData")
patch_file(
    "audio GetFloatFrequencyData",
    "third_party/blink/renderer/modules/webaudio/realtime_analyser.cc",
    r"RealtimeAnalyser::GetFloatFrequencyData\(DOMFloat32Array\*\s*destination_array,\s*double\s*current_time\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-audio-noise")) { float noise = std::stof(cmd->GetSwitchValueASCII("fingerprint-audio-noise")); if (destination_array && destination_array->length() > 0) { destination_array->Data()[0] += noise; } }',
    'HasSwitch("fingerprint-audio-noise")'
)


# ============================================================
# 16. Audio - GetByteFrequencyData
# FILE: realtime_analyser.cc
# ============================================================
print("\n[16] audio GetByteFrequencyData")
patch_file(
    "audio GetByteFrequencyData",
    "third_party/blink/renderer/modules/webaudio/realtime_analyser.cc",
    r"RealtimeAnalyser::GetByteFrequencyData\(DOMUint8Array\*\s*destination_array,\s*double\s*current_time\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-audio-noise")) { int noise = static_cast<int>(std::stof(cmd->GetSwitchValueASCII("fingerprint-audio-noise")) * 1000) & 1; if (destination_array && destination_array->length() > 0) { destination_array->Data()[0] = static_cast<uint8_t>(std::clamp((int)destination_array->Data()[0] + noise, 0, 255)); } }',
    'HasSwitch("fingerprint-audio-noise-byte")'
)


# ============================================================
# 17. Canvas - ToDataURLInternal
# FILE: html_canvas_element.cc
# Day la ham thuc su tao ra chuoi base64
# Lay snapshot -> sua 1 pixel -> encode lai
# ============================================================
print("\n[17] canvas ToDataURLInternal")
patch_file(
    "canvas ToDataURLInternal",
    "third_party/blink/renderer/core/html/canvas/html_canvas_element.cc",
    r"HTMLCanvasElement::ToDataURLInternal\(\s*const String&\s*\w+,\s*const double&\s*\w+,\s*SourceDrawingBuffer\s*\w+\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-canvas-seed")) { const_cast<HTMLCanvasElement*>(this)->SetExternallyAllocatedMemory(std::stoi(cmd->GetSwitchValueASCII("fingerprint-canvas-seed"))); }',
    'HasSwitch("fingerprint-canvas-seed")'
)


# ============================================================
# 18. network effectiveType
# FILE: network_information.cc
# ============================================================
print("\n[18] network effectiveType")
patch_file(
    "network effectiveType",
    "third_party/blink/renderer/modules/netinfo/network_information.cc",
    r"NetworkInformation::effectiveType\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-effective-type")) { std::string val = cmd->GetSwitchValueASCII("fingerprint-effective-type"); if (val == "4g") return V8EffectiveConnectionType(V8EffectiveConnectionType::Enum::k4g); if (val == "3g") return V8EffectiveConnectionType(V8EffectiveConnectionType::Enum::k3g); if (val == "2g") return V8EffectiveConnectionType(V8EffectiveConnectionType::Enum::k2g); if (val == "slow-2g") return V8EffectiveConnectionType(V8EffectiveConnectionType::Enum::kSlow2g); }',
    'HasSwitch("fingerprint-effective-type")'
)


# ============================================================
# 19. network downlink
# FILE: network_information.cc
# ============================================================
print("\n[19] network downlink")
patch_file(
    "network downlink",
    "third_party/blink/renderer/modules/netinfo/network_information.cc",
    r"NetworkInformation::downlink\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-downlink")) return std::stod(cmd->GetSwitchValueASCII("fingerprint-downlink"));',
    'HasSwitch("fingerprint-downlink")'
)


# ============================================================
# 20. network rtt
# FILE: network_information.cc
# ============================================================
print("\n[20] network rtt")
patch_file(
    "network rtt",
    "third_party/blink/renderer/modules/netinfo/network_information.cc",
    r"NetworkInformation::rtt\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-rtt")) return static_cast<uint32_t>(std::stoi(cmd->GetSwitchValueASCII("fingerprint-rtt")));',
    'HasSwitch("fingerprint-rtt")'
)


# ============================================================
# 21. performance.now - them nhieu nho de chong timing attack
# FILE: performance.cc
# ============================================================
print("\n[21] performance.now")
patch_file(
    "performance.now",
    "third_party/blink/renderer/core/timing/performance.cc",
    r"Performance::now\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-timing-noise")) { static thread_local int counter = 0; if ((++counter & 0xF) == 0) { volatile double sink = 0; for (int i = 0; i < std::stoi(cmd->GetSwitchValueASCII("fingerprint-timing-noise")); ++i) sink += i; } }',
    'HasSwitch("fingerprint-timing-noise")'
)


print("\n" + "="*60)
print("XONG! Tong cong 21 patches.")
print("="*60)
print()
print("CACH DUNG:")
print('  chrome.exe \\')
print('    --fingerprint-hardware-concurrency=8 \\')
print('    --fingerprint-device-memory=8 \\')
print('    --fingerprint-device-scale-factor=1.0 \\')
print('    --fingerprint-webgl-vendor="Intel Inc." \\')
print('    --fingerprint-webgl-renderer="Intel Iris OpenGL Engine" \\')
print('    --fingerprint-lang=en-US \\')
print('    --fingerprint-battery-level=0.85 \\')
print('    --fingerprint-max-touch-points=0 \\')
print('    --fingerprint-screen-width=1920 \\')
print('    --fingerprint-screen-height=1080 \\')
print('    --fingerprint-screen-avail-width=1920 \\')
print('    --fingerprint-screen-avail-height=1040 \\')
print('    --fingerprint-screen-color-depth=24 \\')
print('    --fingerprint-platform=Win32 \\')
print('    --fingerprint-disable-webdriver \\')
print('    --fingerprint-audio-noise=0.0001 \\')
print('    --fingerprint-effective-type=4g \\')
print('    --fingerprint-downlink=10.0 \\')
print('    --fingerprint-rtt=50 \\')
print('    --fingerprint-timing-noise=100')
