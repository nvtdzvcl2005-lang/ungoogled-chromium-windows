import os, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def omega_patch(keyword, inject_code, potential_files):
    """Quét tất cả các file có khả năng chứa hàm để đảm bảo không bỏ sót."""
    found_at_least_one = False
    for rel_path in potential_files:
        full_path = os.path.join(SRC_ROOT, rel_path)
        if not os.path.exists(full_path): continue
        
        with open(full_path, 'r', encoding='utf-8') as f: content = f.read()
        
        # Tìm keyword dạng: keyword( hoặc keyword  (
        match = re.search(re.escape(keyword) + r"\s*\(", content)
        if match:
            # Tìm dấu { đầu tiên sau tên hàm
            brace_match = re.search(r"\{", content[match.end():])
            if brace_match:
                start_pos = match.end() + brace_match.start() + 1
                
                # Né vá trùng
                if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+500]:
                    print(f"[~] Đã vá rồi: {keyword} tại {rel_path}")
                    found_at_least_one = True
                    continue
                
                # Chèn header và code fake
                header = '#include "base/command_line.h"\n'
                if header not in content:
                    content = header + content
                    start_pos += len(header)
                
                new_content = content[:start_pos] + "\n  " + inject_code + "\n" + content[start_pos:]
                with open(full_path, 'w', encoding='utf-8') as f: f.write(new_content)
                print(f"[+] THÀNH CÔNG: Đã vá {keyword} tại {rel_path}")
                found_at_least_one = True

    if not found_at_least_one:
        print(f"[!] CẢNH BÁO: Không tìm thấy {keyword} trong danh sách file cung cấp!")

# --- DANH SÁCH VÁ TOÀN DIỆN (COVER 100% CÁC TRƯỜNG HỢP) ---

# 1. Hardware (CPU/RAM) - Thử cả 3 file Google hay dùng
omega_patch("hardwareConcurrency", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));',
    ["third_party/blink/renderer/core/frame/navigator_id.cc", "third_party/blink/renderer/core/frame/navigator.cc", "third_party/blink/renderer/core/frame/local_dom_window.cc"])

omega_patch("deviceMemory", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));',
    ["third_party/blink/renderer/core/frame/navigator_device_memory.cc", "third_party/blink/renderer/core/frame/navigator.cc"])

# 2. Screen & Scaling (Width/Height/Ratio)
omega_patch("devicePixelRatio", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));',
    ["third_party/blink/renderer/core/frame/screen.cc", "third_party/blink/renderer/core/frame/local_dom_window.cc", "third_party/blink/renderer/core/frame/window_screen.cc"])

screen_patch = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));'
omega_patch("width", screen_patch, ["third_party/blink/renderer/core/frame/screen.cc"])
omega_patch("availWidth", screen_patch, ["third_party/blink/renderer/core/frame/screen.cc"])

# 3. WebGL & User-Agent
omega_patch("getParameter", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));',
    ["third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc"])

omega_patch("GetUserAgent", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-ua")) return cmd->GetSwitchValueASCII("fingerprint-ua");',
    ["components/embedder_support/user_agent_utils.cc"])

# 4. Pin & Ngôn ngữ & Touch
omega_patch("level", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-battery-level"));',
    ["third_party/blink/renderer/modules/battery/battery_manager.cc"])

omega_patch("language", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang"));',
    ["third_party/blink/renderer/core/frame/navigator_language.cc", "third_party/blink/renderer/core/frame/navigator.cc"])

omega_patch("maxTouchPoints", 
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));',
    ["third_party/blink/renderer/core/frame/navigator.cc"])
