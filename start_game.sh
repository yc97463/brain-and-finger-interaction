#!/bin/bash

# 手勢辨識遊戲啟動腳本 - 完整版
# 包含所有必要的確認步驟

set -e  # 遇到錯誤時停止執行

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 函數：打印帶顏色的訊息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎮 $1${NC}"
}

# 函數：檢查命令是否存在
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 函數：檢查Python版本
check_python_version() {
    print_info "檢查Python版本..."
    
    if check_command python3; then
        PYTHON_CMD="python3"
    elif check_command python; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python！請安裝Python 3.6或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -ge 6 ]; then
        print_success "Python版本: $PYTHON_VERSION ✓"
    else
        print_error "Python版本過舊: $PYTHON_VERSION (需要3.6+)"
        exit 1
    fi
}

# 函數：檢查並創建虛擬環境
setup_virtual_environment() {
    print_info "檢查虛擬環境..."
    
    if [ ! -d "menv" ]; then
        print_warning "虛擬環境不存在，正在創建..."
        $PYTHON_CMD -m venv menv
        print_success "虛擬環境創建完成"
    else
        print_success "虛擬環境已存在"
    fi
    
    # 啟動虛擬環境
    print_info "啟動虛擬環境..."
    source menv/bin/activate
    print_success "虛擬環境已啟動"
}

# 函數：檢查並安裝依賴套件
check_and_install_dependencies() {
    print_info "檢查Python套件依賴..."
    
    # 檢查requirements.txt是否存在
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt 文件不存在！"
        exit 1
    fi
    
    # 升級pip
    print_info "升級pip..."
    pip install --upgrade pip >/dev/null 2>&1
    
    # 檢查各個套件
    declare -a packages=("cv2:opencv-python" "mediapipe:mediapipe" "PIL:Pillow" "numpy:numpy")
    
    for package_info in "${packages[@]}"; do
        import_name=$(echo $package_info | cut -d':' -f1)
        package_name=$(echo $package_info | cut -d':' -f2)
        
        if python -c "import $import_name" 2>/dev/null; then
            version=$(python -c "import $import_name; print(getattr($import_name, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
            print_success "$package_name 已安裝 (版本: $version)"
        else
            print_warning "$package_name 未安裝，正在安裝..."
            pip install $package_name
            print_success "$package_name 安裝完成"
        fi
    done
    
    # 確保所有依賴都是最新的
    print_info "確保所有依賴套件都已正確安裝..."
    pip install -r requirements.txt >/dev/null 2>&1
    print_success "所有依賴套件檢查完成"
}

# 函數：檢查攝影機
check_camera() {
    print_info "檢查攝影機可用性..."
    
    # 使用Python檢查攝影機，忽略警告訊息
    camera_check=$(python -c "
import cv2
import sys
import warnings
warnings.filterwarnings('ignore')

try:
    # 重定向stderr以忽略OpenCV警告
    import os
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    os.dup2(devnull, 2)
    
    cap = cv2.VideoCapture(0)
    
    # 恢復stderr
    os.dup2(old_stderr, 2)
    os.close(devnull)
    os.close(old_stderr)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            fps = cap.get(cv2.CAP_PROP_FPS)
            backend = int(cap.get(cv2.CAP_PROP_BACKEND))
            cap.release()
            print(f'SUCCESS:{w}x{h}:{fps}:{backend}')
        else:
            cap.release()
            print('FAIL_READ')
    else:
        print('FAIL_OPEN')
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null)

    case $camera_check in
        SUCCESS:*)
            # 解析攝影機資訊
            IFS=':' read -r status width_height fps backend <<< "$camera_check"
            print_success "攝影機檢查通過"
            print_info "攝影機資訊："
            echo "    📐 解析度: $width_height"
            echo "    🎬 FPS: $fps"
            echo "    🔌 後端ID: $backend"
            ;;
        "FAIL_OPEN")
            print_warning "無法開啟攝影機，但可能仍可使用"
            print_info "常見原因："
            echo "  1. 攝影機正被其他程式使用"
            echo "  2. 攝影機權限未開啟"
            echo "  3. 攝影機硬體問題"
            read -p "是否繼續執行？建議先測試攝影機 (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "您可以執行以下命令診斷攝影機："
                echo "  python camera_diagnostic.py"
                exit 1
            fi
            ;;
        "FAIL_READ")
            print_warning "攝影機可以開啟但無法讀取畫面"
            print_info "這可能是暫時性問題，遊戲仍可能正常運行"
            read -p "是否繼續執行？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
        *)
            print_warning "攝影機檢查遇到問題，但可能仍可使用"
            print_info "詳細診斷請執行: python camera_diagnostic.py"
            read -p "是否繼續執行？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
    esac
}

# 函數：檢查中文字體
check_chinese_fonts() {
    print_info "檢查中文字體支援..."
    
    font_check=$(python -c "
from PIL import ImageFont
import sys

font_paths = [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Helvetica.ttc',
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/simhei.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
]

found_fonts = []
for path in font_paths:
    try:
        font = ImageFont.truetype(path, 30)
        found_fonts.append(path)
    except:
        continue

if found_fonts:
    print(f'SUCCESS:{found_fonts[0]}')
else:
    print('NO_FONTS')
" 2>/dev/null)

    if [[ $font_check == SUCCESS:* ]]; then
        font_path=$(echo $font_check | cut -d':' -f2)
        print_success "找到可用的中文字體: $(basename "$font_path")"
    else
        print_warning "未找到理想的中文字體，將使用預設字體"
        print_info "中文可能無法正確顯示，但程式仍可運行"
    fi
}

# 函數：檢查主程式文件
check_main_file() {
    print_info "檢查主程式文件..."
    
    if [ ! -f "手勢辨識_延長版.py" ]; then
        print_error "主程式文件 '手勢辨識_延長版.py' 不存在！"
        exit 1
    fi
    
    # 檢查文件語法
    if python -m py_compile "手勢辨識_延長版.py" 2>/dev/null; then
        print_success "主程式文件檢查通過"
    else
        print_error "主程式文件有語法錯誤！"
        exit 1
    fi
}

# 函數：顯示系統資訊
show_system_info() {
    print_info "系統資訊："
    echo "  作業系統: $(uname -s)"
    echo "  Python版本: $PYTHON_VERSION"
    echo "  工作目錄: $(pwd)"
    echo "  虛擬環境: $(which python)"
}

# 函數：顯示使用說明
show_usage_instructions() {
    print_info "遊戲操作說明："
    echo "  🎯 目標：根據螢幕顯示的數字，用手勢比出對應的數字"
    echo "  ⌨️  按 'q' 鍵退出遊戲"
    echo "  🔄 按 'r' 鍵重置遊戲"
    echo "  ⏱️  準備時間：10秒"
    echo "  🤏 手勢穩定時間：1.5秒"
    echo "  📊 結果顯示時間：8秒"
    echo "  🔢 支援數字：0-7"
    echo "  🎉 連續答對3題有特別慶祝！"
    echo ""
    print_info "建議使用環境："
    echo "  💡 光線充足的環境"
    echo "  📷 確保攝影機畫面清晰"
    echo "  🖐️  手部在攝影機視野內"
    echo "  🎯 背景盡量簡潔"
}

# 主程式開始
main() {
    clear
    print_header "手勢辨識遊戲 - 發展延遲孩童版"
    echo "========================================"
    echo ""
    
    # 執行所有檢查步驟
    check_python_version
    setup_virtual_environment
    check_and_install_dependencies
    check_main_file
    check_chinese_fonts
    check_camera
    
    echo ""
    show_system_info
    echo ""
    show_usage_instructions
    echo ""
    
    # 最終確認
    print_info "所有檢查完成！準備啟動遊戲..."
    read -p "按 Enter 鍵開始遊戲，或按 Ctrl+C 取消: " -r
    echo ""
    
    # 啟動遊戲
    print_header "🚀 啟動手勢辨識遊戲..."
    echo ""
    
    # 執行主程式
    python "手勢辨識_延長版.py"
    
    # 遊戲結束後的訊息
    echo ""
    print_success "遊戲已結束，感謝使用！"
}

# 錯誤處理
trap 'print_error "腳本執行被中斷"; exit 1' INT TERM

# 執行主程式
main "$@" 