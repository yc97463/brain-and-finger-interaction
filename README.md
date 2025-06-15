# Brain and Finger Interaction Game

一個專為發展延遲孩童設計的手勢辨識教育遊戲，透過互動式的手勢訓練，幫助孩童提升手部協調能力和數字認知。

## 🌟 特點

- 🤖 使用 MediaPipe 進行即時手勢辨識
- 🎯 支援單手和雙手數字手勢（0-9）
- ⏱️ 特別設計的延長時間版本：
  - 準備時間：10秒
  - 手勢穩定時間：1.5秒
  - 結果顯示時間：8秒
- 📊 完整的遊戲記錄系統
- 🎮 友善的使用者介面
- 🎉 連續答對獎勵機制
- 📝 中文字體支援

## 🚀 快速開始

### 系統需求

- Python 3.6 或更高版本
- 攝影機
- 作業系統：Windows/macOS/Linux

### 安裝步驟

1. 複製專案：
```bash
git clone https://github.com/yc97463/brain-and-finger-interaction.git
cd brain-and-finger-interaction
```

2. 執行啟動腳本：
```bash
chmod +x start_game.sh
./start_game.sh
```

啟動腳本會自動：
- 檢查 Python 環境
- 設置虛擬環境
- 安裝必要套件
- 檢查攝影機和中文字體
- 啟動遊戲

如果你只想要執行遊戲，可以執行 `手勢辨識_延長版.py` 檔案。
```bash
python 手勢辨識_延長版.py
# python 是 python3 的別名，你需要確定裝置上安裝的 python 版本。
```

## 🎮 遊戲操作

- 🎯 目標：根據螢幕顯示的數字，用手勢比出對應的數字
- ⌨️ 按 'q' 鍵退出遊戲
- 🔄 按 'r' 鍵重置遊戲
- 🤏 支援單手或雙手相加
- 🎉 連續答對3題有特別慶祝！

## 📝 遊戲記錄

遊戲記錄會自動儲存在 `game_logs` 目錄裡，包含：
- 答題時間
- 正確率
- 使用的手勢方式（單手/雙手）
- 反應時間

## 🛠️ 開發工具

- `手勢辨識_延長版.py`：主程式
- `start_game.sh`：啟動腳本
- `camera_diagnostic.py`：攝影機診斷工具
- `test_chinese_font.py`：中文字體測試工具

## 📚 相關文件

- [快速開始指南](QUICK_START.md)
- [中文字體顯示說明](README_中文顯示修正.md)
- [延長版功能說明](README_延長版.md)

## 🤝 貢獻

歡迎提交 Pull Request 或開 Issue 來改進這個專案！

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件