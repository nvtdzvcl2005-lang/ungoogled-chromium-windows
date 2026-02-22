import os
import sys

SRC_ROOT = "build/src"

def inject_code(file_path, search_str, inject_str):
    full_path = os.path.join(SRC_ROOT, file_path)
    if not os.path.exists(full_path): 
        print(f"[!] LỖI: Không thấy file {file_path}")
        sys.exit(1)
    with open(full_path, 'r', encoding='utf-8') as f: content = f.read()
    if search_str not in content:
        print(f"[!] LỖI: Không tìm thấy điểm chèn trong {file_path}")
        sys.exit(1)
    if 'base/command_line.h' not in content:
        content = '#include "base/command_line.h"\n' + content
    if inject_str not in content:
        new_content = content.replace(search_str, search_str + inject_str)
        with open(full_path, 'w', encoding='utf-8') as f: f.write(new_content)
        print(f"[+] Đã tiêm code vào {file_path}")

# --- NHÓM 1: HARDWARE (CPU & RAM) ---
inject_code("third_party/blink/renderer/core/frame/navigator_id.cc", "int NavigatorID::hardwareConcurrency() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-hardware-concurrency\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-hardware-concurrency\"));")
inject_code("third_party/blink/renderer/core/frame/navigator_device_memory.cc", "float NavigatorDeviceMemory::deviceMemory() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-device-memory\")) return std::stof(cmd->GetSwitchValueASCII(\"fingerprint-device-memory\"));")

# --- NHÓM 2: SCREEN (WIDTH, HEIGHT, SCALE) ---
inject_code("third_party/blink/renderer/core/frame/screen.cc", "int Screen::width() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-screen-width\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-screen-width\"));")
inject_code("third_party/blink/renderer/core/frame/screen.cc", "int Screen::height() const {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-screen-height\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-screen-height\"));")

# --- NHÓM 3: USER-AGENT & CLIENT HINTS ---
inject_code("components/embedder_support/user_agent_utils.cc", "std::string GetUserAgent() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-ua\")) return cmd->GetSwitchValueASCII(\"fingerprint-ua\");")

# --- NHÓM 4: WEBGL (GPU VENDOR & RENDERER) ---
inject_code("third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc", "String WebGLRenderingContextBase::getParameter(", 
            """
  auto* cmd = base::CommandLine::ForCurrentProcess();
  if (pname == 0x9245 && cmd->HasSwitch("fingerprint-webgl-vendor")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-vendor"));
  if (pname == 0x9246 && cmd->HasSwitch("fingerprint-webgl-renderer")) return String::FromUTF8(cmd->GetSwitchValueASCII("fingerprint-webgl-renderer"));
""")

# --- NHÓM 5: NOISE (CANVAS, AUDIO, RECTS) ---
# Tận dụng tham số của anh để tạo seed nhiễu chủ động
inject_code("third_party/blink/renderer/core/html/canvas/canvas_rendering_context.cc", "void CanvasRenderingContext::DidDraw(", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-canvas-noise\")) { /* Thêm logic nhiễu dựa trên seed */ }")

# --- NHÓM 6: THIẾT BỊ (TOUCH, LANG, BATTERY) ---
inject_code("third_party/blink/renderer/core/frame/navigator.cc", "int Navigator::maxTouchPoints() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-max-touch-points\")) return std::stoi(cmd->GetSwitchValueASCII(\"fingerprint-max-touch-points\"));")
inject_code("third_party/blink/renderer/core/frame/navigator_language.cc", "String NavigatorLanguage::language() {", 
            "\n  auto* cmd = base::CommandLine::ForCurrentProcess();\n  if (cmd->HasSwitch(\"fingerprint-lang\")) return String::FromUTF8(cmd->GetSwitchValueASCII(\"fingerprint-lang\"));")
