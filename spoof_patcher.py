import os, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def smart_patch(keyword, inject_code, primary_file, backup_files=[]):
    target_files = [primary_file] + backup_files
    for rel_path in target_files:
        full_path = os.path.join(SRC_ROOT, rel_path)
        if not os.path.exists(full_path): continue
        with open(full_path, 'r', encoding='utf-8') as f: content = f.read()
        match = re.search(re.escape(keyword) + r"\s*\(", content)
        if match:
            brace_pos = content.find('{', match.end())
            if brace_pos != -1:
                start_pos = brace_pos + 1
                if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+400]:
                    print(f"[~] Đã vá rồi: {keyword}")
                    return
                if 'base/command_line.h' not in content:
                    content = '#include "base/command_line.h"\n' + content
                    start_pos += len('#include "base/command_line.h"\n')
                new_content = content[:start_pos] + "\n  " + inject_code + "\n" + content[start_pos:]
                with open(full_path, 'w', encoding='utf-8') as f: f.write(new_content)
                print(f"[+] THÀNH CÔNG: Đã vá {keyword} tại {rel_path}")
                return
    print(f"[!] THẤT BẠI: Méo tìm được {keyword}!")

# --- VÁ THAM SỐ CHỦ ĐỘNG ---
smart_patch("hardwareConcurrency", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));', "third_party/blink/renderer/core/frame/navigator_id.cc", ["third_party/blink/renderer/core/frame/navigator.cc"])
smart_patch("deviceMemory", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));', "third_party/blink/renderer/core/frame/navigator_device_memory.cc")
smart_patch("width", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));', "third_party/blink/renderer/core/frame/screen.cc")
smart_patch("devicePixelRatio", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));', "third_party/blink/renderer/core/frame/screen.cc", ["third_party/blink/renderer/core/frame/local_dom_window.cc"])
smart_patch("getParameter", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));', "third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc")
