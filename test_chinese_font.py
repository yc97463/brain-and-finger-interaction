#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def put_chinese_text(img, text, position, font_size=30, color=(255, 255, 255), font_path=None):
    """
    在OpenCV圖像上顯示中文文字
    """
    # 將OpenCV圖像轉換為PIL圖像
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
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
                    print(f"✅ 成功載入字體: {path}")
                    break
                except Exception as e:
                    print(f"❌ 字體載入失敗: {path} - {e}")
                    continue
                    
            # 如果所有字體都載入失敗，使用預設字體
            if font is None:
                font = ImageFont.load_default()
                print("⚠️  使用預設字體")
                
    except Exception as e:
        print(f"字體載入錯誤: {e}")
        font = ImageFont.load_default()
    
    # 繪製文字
    draw.text(position, text, font=font, fill=color)
    
    # 轉換回OpenCV格式
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv

def main():
    # 創建一個黑色背景圖像
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 測試中文文字顯示
    test_texts = [
        ("準備好了嗎？請比出這個數字：", (50, 50), 30, (255, 255, 255)),
        ("請比出數字:", (50, 100), 35, (0, 255, 0)),
        ("偵測到: 2", (50, 150), 40, (221, 255, 97)),
        ("答對了！", (50, 200), 50, (0, 255, 0)),
        ("做得很好！", (50, 260), 35, (0, 255, 0)),
        ("太棒了！", (50, 310), 60, (255, 255, 255)),
        ("連續答對3題！", (50, 380), 40, (255, 255, 255)),
        ("再試一次！", (50, 430), 45, (0, 100, 255))
    ]
    
    print("🧪 測試中文字體顯示...")
    
    for text, pos, size, color in test_texts:
        img = put_chinese_text(img, text, pos, size, color)
        print(f"✅ 顯示文字: {text}")
    
    # 顯示結果
    cv2.imshow('中文字體測試', img)
    print("\n📺 顯示測試視窗...")
    print("按任意鍵關閉視窗")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("✅ 測試完成")

if __name__ == '__main__':
    main() 