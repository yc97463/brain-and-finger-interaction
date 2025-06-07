#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# 全域字體快取
_font_cache = {}

# 中文字體顯示函數
def put_chinese_text(img, text, position, font_size=30, color=(255, 255, 255), font_path=None):
    """
    在OpenCV圖像上顯示中文文字
    """
    global _font_cache
    
    # 將OpenCV圖像轉換為PIL圖像
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # 創建字體快取鍵
    cache_key = f"{font_path or 'default'}_{font_size}"
    
    # 檢查快取中是否已有字體
    if cache_key in _font_cache:
        font = _font_cache[cache_key]
    else:
        # 嘗試載入中文字體
        font = None
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                # 嘗試系統預設中文字體
                font_paths = [
                    # macOS 系統字體
                    "/System/Library/Fonts/STHeiti Medium.ttc",
                    "/System/Library/Fonts/STHeiti Light.ttc",
                    "/System/Library/Fonts/Helvetica.ttc",
                    # Windows 系統字體
                    "C:/Windows/Fonts/msyh.ttc",
                    "C:/Windows/Fonts/simhei.ttf",
                    # Linux 系統字體
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
                ]
                
                for path in font_paths:
                    try:
                        font = ImageFont.truetype(path, font_size)
                        print(f"✅ 載入字體: {path}")
                        break
                    except:
                        continue
                        
                # 如果所有字體都載入失敗，使用預設字體
                if font is None:
                    font = ImageFont.load_default()
                    print("⚠️  使用預設字體")
                    
        except Exception as e:
            print(f"字體載入錯誤: {e}")
            font = ImageFont.load_default()
        
        # 將字體存入快取
        _font_cache[cache_key] = font
    
    # 繪製文字
    draw.text(position, text, font=font, fill=color)
    
    # 轉換回OpenCV格式
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv

def main():
    print("🎮 測試遊戲界面中文顯示")
    print("按 ESC 鍵退出")
    
    w, h = 640, 480
    target_number = 2
    correct_count = 1
    
    # 模擬不同的遊戲狀態
    states = [
        {
            "name": "準備階段",
            "texts": [
                ("準備好了嗎？請比出這個數字：", (30, 30), 25, (255, 255, 255)),
                ("倒數計時: 5 秒", (30, 400), 35, (0, 165, 255)),
                (f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255))
            ]
        },
        {
            "name": "辨識階段", 
            "texts": [
                ("請比出數字:", (30, 55), 35, (255, 255, 255)),
                (f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255)),
                ("保持手勢", (400, 70), 20, (255, 255, 255)),
                ("偵測到: 2", (30, 180), 40, (221, 255, 97)),
                ("請將手放在鏡頭前", (30, 230), 35, (255, 255, 0))
            ]
        },
        {
            "name": "結果階段 - 正確",
            "texts": [
                ("下一題倒數: 3 秒", (w-250, 30), 30, (255, 255, 255)),
                (f"目標數字: {target_number}", (30, 30), 35, (255, 255, 255)),
                (f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255)),
                ("答對了！", (w//2-80, h//2-30), 80, (0, 255, 0)),
                ("做得很好！", (w//2-90, h//2+40), 45, (0, 255, 0))
            ]
        },
        {
            "name": "結果階段 - 錯誤",
            "texts": [
                ("下一題倒數: 3 秒", (w-250, 30), 30, (255, 255, 255)),
                (f"目標數字: {target_number}", (30, 30), 35, (255, 255, 255)),
                (f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255)),
                ("再試一次！", (w//2-90, h//2-30), 70, (0, 100, 255)),
                ("沒關係，繼續加油！", (w//2-140, h//2+40), 35, (0, 100, 255))
            ]
        },
        {
            "name": "慶祝階段",
            "texts": [
                (f"目標數字: {target_number}", (30, 30), 35, (255, 255, 255)),
                ("連續答對: 3/3", (30, 450), 30, (255, 255, 255)),
                ("太棒了！", (w//2-80, h//2-70), 80, (255, 255, 255)),
                ("連續答對3題！", (w//2-120, h//2), 45, (255, 255, 255))
            ]
        }
    ]
    
    current_state = 0
    
    while True:
        # 創建黑色背景
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        # 顯示當前狀態的文字
        state = states[current_state]
        print(f"\n📺 顯示狀態: {state['name']}")
        
        for text, pos, size, color in state['texts']:
            img = put_chinese_text(img, text, pos, size, color)
        
        # 在中央顯示大數字
        if current_state in [0, 1, 2, 3]:  # 不是慶祝階段
            cv2.putText(img, f"{target_number}", (w//2-40, h//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 8, cv2.LINE_AA)
        
        # 顯示進度條（辨識階段）
        if current_state == 1:
            progress = 0.7  # 模擬70%進度
            bar_width = 200
            bar_height = 20
            bar_x = w - bar_width - 30
            bar_y = 100
            
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
        
        cv2.imshow('Hand Gesture Game - 中文顯示測試', img)
        
        # 等待按鍵
        key = cv2.waitKey(2000)  # 2秒後自動切換
        if key == 27:  # ESC鍵
            break
        elif key == ord(' '):  # 空白鍵手動切換
            current_state = (current_state + 1) % len(states)
        else:
            # 自動切換到下一個狀態
            current_state = (current_state + 1) % len(states)
    
    cv2.destroyAllWindows()
    print("✅ 測試完成")

if __name__ == '__main__':
    main() 