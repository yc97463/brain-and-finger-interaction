#!/bin/bash

# 測試啟動腳本 - 只執行檢查步驟
source start_game.sh

# 重新定義main函數，只執行檢查
test_main() {
    clear
    print_header "手勢辨識遊戲 - 系統檢查測試"
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
    
    print_success "所有檢查完成！系統準備就緒。"
    print_info "如要啟動遊戲，請執行: ./start_game.sh"
}

# 執行測試
test_main "$@" 