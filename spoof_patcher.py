import os, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def omega_patch(keyword, inject_code, potential_files):
    """Vá trên mọi mặt trận, tìm thấy là tiêm mã fake ngay lập tức."""
    found = False
    for rel_path in potential_files:
        full_path = os.path.join(SRC_ROOT, rel_path)
        if not os.path.exists(full_path): continue
        with open(full_path, 'r', encoding='utf-8') as f: content = f.read()
        
        match = re.search(re.escape(keyword) + r"\s*\(", content)
        if match:
            brace_match = re.search(r"\{", content[match.end():])
            if brace_match:
                start_pos = match.end() + brace_match.start() + 1
                if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+500]:
                    print(f"[~] Đã vá rồi: {keyword} tại {rel_path}"); found = True; continue
                
                header = '#include "base/command_line.h"\n'
                if header not in content:
                    content = header + content
                    start_pos += len(header)
                
                new_content = content[:start_pos] + "\n  " + inject_code + "\n" + content[start_pos:]
                with open(full_path, 'w', encoding='utf-8') as f: f.write(new_content)
                print(f"[+] THÀNH CÔNG: {keyword} -> {rel_path}"); found = True
    if not found: print(f"[!] KHÔNG TÌM THẤY: {keyword}")

# --- VÁ TỔNG LỰC ---
# 1. CPU Cores (Bản 145 nằm ở navigator_concurrent_hardware.cc)
omega_patch("hardwareConcurrency", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));', 
    ["third_party/blink/renderer/core/frame/navigator_concurrent_hardware.cc", "third_party/blink/renderer/core/execution_context/navigator_base.cc"])

# 2. Touch Points
omega_patch("maxTouchPoints", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));', 
    ["third_party/blink/renderer/core/frame/navigator.cc", "third_party/blink/renderer/core/frame/navigator_id.cc"])

# 3. RAM & Màn hình
omega_patch("deviceMemory", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));', ["third_party/blink/renderer/core/frame/navigator_device_memory.cc"])
omega_patch("devicePixelRatio", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));', ["third_party/blink/renderer/core/frame/screen.cc", "third_party/blink/renderer/core/frame/local_dom_window.cc"])
omega_patch("width", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));', ["third_party/blink/renderer/core/frame/screen.cc"])
omega_patch("availWidth", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));', ["third_party/blink/renderer/core/frame/screen.cc"])

# 4. WebGL & Lang & Battery
omega_patch("getParameter", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));', ["third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc"])
omega_patch("GetUserAgent", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-ua")) return cmd->GetSwitchValueASCII("fingerprint-ua");', ["components/embedder_support/user_agent_utils.cc"])
omega_patch("language", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang"));', ["third_party/blink/renderer/core/frame/navigator_language.cc"])
omega_patch("level", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-battery-level"));', ["third_party/blink/renderer/modules/battery/battery_manager.cc"])
