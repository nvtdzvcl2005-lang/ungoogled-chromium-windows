import os
import sys
import io
import re

# Ép console dùng UTF-8 để không lỗi Unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC_ROOT = "build/src"

def patch_cpp_function(file_path, function_pattern, inject_code):
    """Sử dụng Regex để tìm hàm và chèn code vào ngay đầu thân hàm."""
    full_path = os.path.join(SRC_ROOT, file_path)
    if not os.path.exists(full_path):
        print(f"[!] Bỏ qua: Không thấy {file_path}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Thêm header cần thiết
    if 'base/command_line.h' not in content:
        content = '#include "base/command_line.h"\n' + content

    # Regex tìm điểm bắt đầu của thân hàm {
    # Mẫu: kiểu_trả_về TênLớp::TênHàm(đối_số) const {
    match = re.search(function_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        start_pos = match.end()
        # Tránh chèn trùng lặp
        if inject_code.strip() in content:
            print(f"[~] Đã có mã trong {file_path}")
            return
            
        new_content = content[:start_pos] + "\n  " + inject_code + content[start_pos:]
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[+] Đã vá thành công: {file_path}")
    else:
        print(f"[!] LỖI: Không tìm thấy hàm trong {file_path} với pattern: {function_pattern}")
        # sys.exit(1) # Bật dòng này nếu muốn ngắt build ngay khi lỗi

# --- 1. NHÓM HARDWARE (CPU, RAM) ---
patch_cpp_function(
    "third_party/blink/renderer/core/frame/navigator_id.cc",
    r"int\s+NavigatorID::hardwareConcurrency\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-hardware-concurrency")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-hardware-concurrency"));'
)
patch_cpp_function(
    "third_party/blink/renderer/core/frame/navigator_device_memory.cc",
    r"float\s+NavigatorDeviceMemory::deviceMemory\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-memory")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-memory"));'
)

# --- 2. NHÓM SCREEN (3 tham số chính + các tham số phụ) ---
screen_patch = """
  auto* cmd = base::CommandLine::ForCurrentProcess();
  if (cmd->HasSwitch("fingerprint-screen-width")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-width"));
"""
patch_cpp_function("third_party/blink/renderer/core/frame/screen.cc", r"int\s+Screen::width\(\)\s*const\s*\{", screen_patch)
patch_cpp_function("third_party/blink/renderer/core/frame/screen.cc", r"int\s+Screen::availWidth\(\)\s*const\s*\{", screen_patch)

screen_h_patch = """
  auto* cmd = base::CommandLine::ForCurrentProcess();
  if (cmd->HasSwitch("fingerprint-screen-height")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-screen-height"));
"""
patch_cpp_function("third_party/blink/renderer/core/frame/screen.cc", r"int\s+Screen::height\(\)\s*const\s*\{", screen_h_patch)
patch_cpp_function("third_party/blink/renderer/core/frame/screen.cc", r"int\s+Screen::availHeight\(\)\s*const\s*\{", screen_h_patch)

patch_cpp_function(
    "third_party/blink/renderer/core/frame/screen.cc",
    r"double\s+Screen::devicePixelRatio\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-device-scale-factor")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-device-scale-factor"));'
)

# --- 3. NHÓM USER-AGENT & CLIENT HINTS ---
patch_cpp_function(
    "components/embedder_support/user_agent_utils.cc",
    r"std::string\s+GetUserAgent\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-ua")) return cmd->GetSwitchValueASCII("fingerprint-ua");'
)

# --- 4. NHÓM WEBGL (GPU VENDOR & RENDERER) ---
patch_cpp_function(
    "third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc",
    r"String\s+WebGLRenderingContextBase::getParameter\s*\([^)]*\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor")); if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));'
)

# --- 5. NHÓM BATTERY & TOUCH & LANG ---
patch_cpp_function(
    "third_party/blink/renderer/core/frame/navigator.cc",
    r"int\s+Navigator::maxTouchPoints\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-max-touch-points")) return std::stoi(cmd->GetSwitchValueASCII("fingerprint-max-touch-points"));'
)
patch_cpp_function(
    "third_party/blink/renderer/core/frame/navigator_language.cc",
    r"String\s+NavigatorLanguage::language\(\)\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-lang")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-lang"));'
)
patch_cpp_function(
    "third_party/blink/renderer/modules/battery/battery_manager.cc",
    r"double\s+BatteryManager::level\(\)\s*const\s*\{",
    'auto* cmd = base::CommandLine::ForCurrentProcess(); if (cmd->HasSwitch("fingerprint-battery-level")) return std::stof(cmd->GetSwitchValueASCII("fingerprint-battery-level"));'
)
