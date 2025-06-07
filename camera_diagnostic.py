#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import sys
import platform

def check_camera_permissions():
    """檢查攝影機權限（macOS特定）"""
    if platform.system() == "Darwin":  # macOS
        print("💡 macOS攝影機權限檢查：")
        print("   請確認已在 系統偏好設定 > 安全性與隱私 > 攝影機 中")
        print("   允許終端機或Python存取攝影機")
        print()

def test_camera_indices():
    """測試不同的攝影機索引"""
    print("🔍 攝影機索引測試...")
    print("=" * 50)
    
    working_cameras = []
    
    for i in range(10):  # 測試索引 0-9
        print(f"📷 測試攝影機索引 {i}: ", end="")
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # 嘗試讀取一幀
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    print(f"✅ 成功 - 解析度: {w}x{h}")
                    working_cameras.append(i)
                else:
                    print("❌ 可開啟但無法讀取畫面")
                cap.release()
            else:
                print("❌ 無法開啟")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
    
    print("=" * 50)
    return working_cameras

def test_camera_backends():
    """測試不同的攝影機後端"""
    print("🔧 攝影機後端測試...")
    print("=" * 50)
    
    backends = [
        (cv2.CAP_ANY, "CAP_ANY (自動)"),
        (cv2.CAP_AVFOUNDATION, "CAP_AVFOUNDATION (macOS)"),
        (cv2.CAP_V4L2, "CAP_V4L2 (Linux)"),
        (cv2.CAP_DSHOW, "CAP_DSHOW (Windows)"),
    ]
    
    working_backends = []
    
    for backend_id, backend_name in backends:
        print(f"🔌 測試後端 {backend_name}: ", end="")
        try:
            cap = cv2.VideoCapture(0, backend_id)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print("✅ 成功")
                    working_backends.append((backend_id, backend_name))
                else:
                    print("❌ 可開啟但無法讀取")
                cap.release()
            else:
                print("❌ 無法開啟")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
    
    print("=" * 50)
    return working_backends

def detailed_camera_info():
    """獲取詳細的攝影機資訊"""
    print("📊 攝影機詳細資訊...")
    print("=" * 50)
    
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            # 獲取攝影機屬性
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            backend = cap.get(cv2.CAP_PROP_BACKEND)
            
            print(f"📐 預設解析度: {int(width)}x{int(height)}")
            print(f"🎬 預設FPS: {fps}")
            print(f"🔌 後端ID: {int(backend)}")
            
            # 嘗試設定不同解析度
            test_resolutions = [(640, 480), (320, 240), (1280, 720)]
            print("\n📏 解析度測試:")
            for w, h in test_resolutions:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
                actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(f"   設定 {w}x{h} → 實際 {actual_w}x{actual_h}")
            
            cap.release()
        else:
            print("❌ 無法開啟攝影機進行詳細檢查")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    print("=" * 50)

def check_system_info():
    """檢查系統資訊"""
    print("💻 系統資訊...")
    print("=" * 50)
    print(f"作業系統: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print(f"OpenCV版本: {cv2.__version__}")
    print("=" * 50)

def main():
    print("🎥 攝影機診斷工具")
    print("=" * 50)
    print()
    
    # 系統資訊
    check_system_info()
    print()
    
    # 權限檢查
    check_camera_permissions()
    
    # 測試攝影機索引
    working_cameras = test_camera_indices()
    print()
    
    # 測試後端
    working_backends = test_camera_backends()
    print()
    
    # 詳細資訊
    if working_cameras:
        detailed_camera_info()
        print()
    
    # 總結報告
    print("📋 診斷總結")
    print("=" * 50)
    
    if working_cameras:
        print(f"✅ 找到 {len(working_cameras)} 個可用攝影機:")
        for cam_id in working_cameras:
            print(f"   - 攝影機索引 {cam_id}")
    else:
        print("❌ 未找到可用的攝影機")
        print("\n🔧 建議解決方案:")
        print("1. 檢查攝影機是否被其他程式使用")
        print("2. 檢查攝影機權限設定")
        print("3. 重新連接攝影機")
        print("4. 重啟電腦")
    
    if working_backends:
        print(f"\n✅ 找到 {len(working_backends)} 個可用後端:")
        for backend_id, backend_name in working_backends:
            print(f"   - {backend_name}")
    else:
        print("\n❌ 未找到可用的攝影機後端")
    
    print("=" * 50)
    
    # 提供修正建議
    if not working_cameras:
        print("\n🛠️  修正建議:")
        print("1. 確認攝影機硬體正常")
        print("2. 檢查系統權限設定")
        print("3. 嘗試重新安裝OpenCV: pip install --upgrade opencv-python")
        print("4. 檢查是否有其他程式正在使用攝影機")

if __name__ == "__main__":
    main() 