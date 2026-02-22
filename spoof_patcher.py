import os
import sys
import io

# Sửa lỗi hiển thị tiếng Việt trên Console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC_ROOT = "build/src"

def inject_code(file_path, search_str, inject_str):
    full_path = os.path.join(SRC_ROOT, file_path)
    if not os.path.exists(full_path): 
        print(f"[!] LỖI: Không thấy {file_path}"); sys.exit(1)
        
    with open(full_path, 'r', encoding='utf-8') as f: 
        content = f.read()
    
    # Tìm kiếm linh hoạt (hỗ trợ cả trường hợp thiếu const)
    actual_search = search_str
    if search_str not in content:
        alt_search = search_str.replace(" const {", " {")
        if alt_search in content:
            actual_search = alt_search
        else:
            print(f"[!] LỖI: Không tìm thấy điểm chèn trong {file_path}"); sys.exit(1)
        
    if 'base/command_line.h' not in content:
        content = '#include "base/command_line.h"\n' + content
        
    if inject_str not in content:
        with open(full_path, 'w', encoding='utf-8') as f: 
            f.write(content.replace(actual_search, actual_search + inject_str))
        print(f"[+] Thành công: {file_path}")

# --- Nhóm Hardware (CPU, RAM) ---
inject_code("third_party/blink/renderer/core/frame/navigator_id.cc", "int NavigatorID::hardwareConcurrency() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-hardware-concurrency\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-hardware-concurrency\"));")
inject_code("third_party/blink/renderer/core/frame/navigator_device_memory.cc", "float NavigatorDeviceMemory::deviceMemory() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-device-memory\")) return std::stof(cmd->GetSwitchValueASCII(\"fingerprint-device-memory\"));")

# --- Nhóm Screen (Width, Height, Scale Factor) ---
inject_code("third_party/blink/renderer/core/frame/screen.cc", "int Screen::width() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-screen-width\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-screen-width\"));")
inject_code("third_party/blink/renderer/core/frame/screen.cc", "int Screen::height() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-screen-height\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-screen-height\"));")
inject_code("third_party/blink/renderer/core/frame/screen.cc", "double Screen::devicePixelRatio() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-device-scale-factor\")) return std::stof(cmd->GetSwitchValueASCII(\"fingerprint-device-scale-factor\"));")

# --- Nhóm User-Agent & WebGL ---
inject_code("components/embedder_support/user_agent_utils.cc", "std::string GetUserAgent() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-ua\")) return cmd->GetSwitchValueASCII(\"fingerprint-ua\");")
inject_code("third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc", "String WebGLRenderingContextBase::getParameter(", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (pname == 0x9245 && cmd->HasSwitch(\"fingerprint-webgl-vendor\")) return String::FromUTF8(cmd->GetSwitchValueASCII(\"fingerprint-webgl-vendor\"));\n  if (pname == 0x9246 && cmd->HasSwitch(\"fingerprint-webgl-renderer\")) return String::FromUTF8(cmd->GetSwitchValueASCII(\"fingerprint-webgl-renderer\"));")

# --- Nhóm Touch & Language ---
inject_code("third_party/blink/renderer/core/frame/navigator.cc", "int Navigator::maxTouchPoints() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-max-touch-points\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-max-touch-points\"));")
inject_code("third_party/blink/renderer/core/frame/navigator_language.cc", "String NavigatorLanguage::language() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-lang\")) return String::FromUTF8(cmd->GetSwitchValueASCII(\"fingerprint-lang\"));")
