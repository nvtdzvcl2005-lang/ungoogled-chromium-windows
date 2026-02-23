import os
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def super_patch(file_path, keyword, inject_code):
    full_path = os.path.join(SRC_ROOT, file_path)
    if not os.path.exists(full_path):
        print(f"[!] Bỏ qua: Không thấy {file_path}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'base/command_line.h' not in content:
        content = '#include "base/command_line.h"\n' + content

    # Regex tìm hàm linh hoạt: [Kiểu trả về] [TênLớp::]keyword([đối số]) [const] {
    pattern = r"[\w:<>]+\s+[\w:]*" + re.escape(keyword) + r"\s*\([^)]*\)\s*(?:const\s*)?\{"
    
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        start_pos = match.end()
        if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+300]:
            print(f"[~] Đã vá rồi: {keyword}")
            return
            
        new_content = content[:start_pos] + "\n  " + inject_code + content[start_pos:]
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[+] THẮNG LỢI: Đã vá {keyword} trong {file_path}")
    else:
        print(f"[!] THẤT BẠI: Không thấy '{keyword}' trong {file_path}")

# --- TIÊM CODE FAKE CHỦ ĐỘNG ---
# Khớp 100% với tham số của anh Trường trong profile_manager.py
super_patch("third_party/blink/renderer/core/frame/navigator_id.cc", "hardwareConcurrency", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));')
super_patch("third_party/blink/renderer/core/frame/navigator_device_memory.cc", "deviceMemory", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));')
super_patch("third_party/blink/renderer/core/frame/screen.cc", "width", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));')
super_patch("third_party/blink/renderer/core/frame/screen.cc", "devicePixelRatio", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));')
super_patch("third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc", "getParameter", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));')
super_patch("third_party/blink/renderer/core/frame/navigator.cc", "maxTouchPoints", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));')
super_patch("third_party/blink/renderer/modules/battery/battery_manager.cc", "level", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-battery-level"));')
