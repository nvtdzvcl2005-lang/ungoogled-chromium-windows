import os, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC_ROOT = "build/src"

def audit_and_patch(keyword, inject_code, potential_files):
    found = False
    print(f"\n>>> ĐANG KIỂM TRA THAM SỐ: {keyword}")
    
    for rel_path in potential_files:
        full_path = os.path.join(SRC_ROOT, rel_path)
        if not os.path.exists(full_path): continue
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tìm hàm: keyword( hoặc keyword  (
        match = re.search(re.escape(keyword) + r"\s*\(", content)
        if match:
            # Tìm dấu { đầu tiên sau tên hàm
            brace_match = re.search(r"\{", content[match.end():])
            if brace_match:
                start_pos = match.end() + brace_match.start() + 1
                
                # Né vá trùng
                if "CommandLine::ForCurrentProcess" in content[start_pos:start_pos+500]:
                    print(f"  [~] Đã vá từ trước tại: {rel_path}")
                    found = True
                    continue
                
                # --- PHẦN IN RA ĐỂ ANH TRƯỜNG KIỂM TRA ---
                original_snippet = content[start_pos:start_pos + 150].strip().replace('\n', ' ')
                print(f"  [!] TÌM THẤY TẠI: {rel_path}")
                print(f"  [?] NỘI DUNG GỐC: {original_snippet}...")
                # ------------------------------------------

                # Tiến hành vá
                header = '#include "base/command_line.h"\n'
                if header not in content:
                    content = header + content
                    start_pos += len(header)
                
                new_content = content[:start_pos] + "\n  " + inject_code + "\n" + content[start_pos:]
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [+] VÁ THÀNH CÔNG!")
                found = True
                
    if not found:
        print(f"  [X] KHÔNG TÌM THẤY {keyword} trong bất kỳ file nào!")

# --- DANH SÁCH VÁ TỔNG LỰC ---

# 1. CPU Cores (Sửa lỗi xịt ở bản cũ)
omega_cpu = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));'
audit_and_patch("hardwareConcurrency", omega_cpu, [
    "third_party/blink/renderer/core/frame/navigator_concurrent_hardware.cc",
    "third_party/blink/renderer/core/execution_context/navigator_base.cc"
])

# 2. Touch Points (Càn quét điểm chạm - Quan trọng cho Mobile)
omega_touch = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));'
audit_and_patch("maxTouchPoints", omega_touch, [
    "third_party/blink/renderer/core/execution_context/navigator_base.cc",
    "third_party/blink/renderer/core/frame/navigator.cc",
    "third_party/blink/renderer/core/frame/navigator_id.cc"
])

# 3. RAM (Device Memory)
omega_ram = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));'
audit_and_patch("deviceMemory", omega_ram, [
    "third_party/blink/renderer/core/frame/navigator_device_memory.cc",
    "third_party/blink/renderer/core/execution_context/navigator_base.cc"
])

# 4. Screen & Ratio
omega_pixel = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));'
audit_and_patch("devicePixelRatio", omega_pixel, ["third_party/blink/renderer/core/frame/screen.cc", "third_party/blink/renderer/core/frame/local_dom_window.cc"])

omega_width = 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));'
audit_and_patch("width", omega_width, ["third_party/blink/renderer/core/frame/screen.cc"])
audit_and_patch("availWidth", omega_width, ["third_party/blink/renderer/core/frame/screen.cc"])

# 5. WebGL, UA, Lang
audit_and_patch("getParameter", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));', ["third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc"])
audit_and_patch("GetUserAgent", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-ua")) return cmd->GetSwitchValueASCII("fingerprint-ua");', ["components/embedder_support/user_agent_utils.cc"])
audit_and_patch("language", 'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang"));', ["third_party/blink/renderer/core/frame/navigator_language.cc", "third_party/blink/renderer/core/execution_context/navigator_base.cc"])
