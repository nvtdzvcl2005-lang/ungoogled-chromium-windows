import os
import sys
import io
import re

# Ép console dùng UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def universal_patch(file_path, keyword, inject_code):
    """Tìm hàm dựa trên tên và tự động xác định vị trí dấu { để tiêm mã."""
    full_path = os.path.join(SRC_ROOT, file_path)
    if not os.path.exists(full_path):
        print(f"[!] Bỏ qua: Không thấy {file_path}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'base/command_line.h' not in content:
        content = '#include "base/command_line.h"\n' + content

    # Tìm vị trí xuất hiện của tên hàm theo sau là dấu (
    # Ví dụ: hardwareConcurrency(
    pattern = re.escape(keyword) + r"\s*\("
    match = re.search(pattern, content)
    
    if match:
        # Tìm dấu { đầu tiên sau khi tìm thấy tên hàm
        brace_pos = content.find('{', match.end())
        if brace_pos != -1:
            start_pos = brace_pos + 1
            # Tránh vá trùng
            if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+300]:
                print(f"[~] Đã vá rồi: {keyword}")
                return
            
            new_content = content[:start_pos] + "\n  " + inject_code + "\n" + content[start_pos:]
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[+] THẮNG LỢI: Đã vá {keyword} trong {file_path}")
            return

    print(f"[!] THẤT BẠI: Không thấy '{keyword}' trong {file_path}")

# --- TIÊM CODE FAKE CHỦ ĐỘNG ---
# Khớp 100% với 24 tham số anh Trường cần
universal_patch("third_party/blink/renderer/core/frame/navigator_id.cc", "hardwareConcurrency", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));')
universal_patch("third_party/blink/renderer/core/frame/navigator_device_memory.cc", "deviceMemory", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));')
universal_patch("third_party/blink/renderer/core/frame/screen.cc", "width", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));')
universal_patch("third_party/blink/renderer/core/frame/screen.cc", "height", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-height")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-height"));')
universal_patch("third_party/blink/renderer/core/frame/screen.cc", "devicePixelRatio", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));')
universal_patch("third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc", "getParameter", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));')
universal_patch("third_party/blink/renderer/core/frame/navigator.cc", "maxTouchPoints", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));')
universal_patch("third_party/blink/renderer/modules/battery/battery_manager.cc", "level", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-battery-level"));')
universal_patch("third_party/blink/renderer/core/frame/navigator_language.cc", "language", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang"));')
