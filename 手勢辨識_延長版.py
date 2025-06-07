import cv2
import mediapipe as mp
import math
import random
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 全域設定變數
MIN_NUMBER = 0  # 測驗數字最小值
MAX_NUMBER = 7  # 測驗數字最大值

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
                    # "/System/Library/Fonts/STHeiti Medium.ttc",
                    # "/System/Library/Fonts/STHeiti Light.ttc",
                    "/Users/yc97463/Library/Fonts/jf-jinxuan-3.1-bold.otf",
                    "/Users/yc97463/Library/Fonts/jf-jinxuan-3.1-medium.otf",
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
                        break
                    except:
                        continue
                        
                # 如果所有字體都載入失敗，使用預設字體
                if font is None:
                    font = ImageFont.load_default()
                    
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

# 原有的角度計算函數
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 原有的手指角度計算函數
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 原有的手勢判斷函數，但只保留數字判斷
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 只判斷數字手勢
    if f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '2'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        return '9'
    else:
        return ''

def main():
    # 首先嘗試列出可用的攝影機
    print("🔍 正在檢測可用的攝影機...")
    
    # 嘗試不同的攝影機索引
    camera_indices = [0, 1, 2, -1]  # -1 通常代表預設攝影機
    cap = None
    working_index = None
    
    for index in camera_indices:
        print(f"嘗試攝影機索引 {index}...")
        test_cap = cv2.VideoCapture(index)
        
        # 在 macOS 上，有時需要設定後端
        if test_cap.isOpened():
            # 嘗試讀取一幀來確認攝影機真的可用
            ret, frame = test_cap.read()
            if ret and frame is not None:
                print(f"✅ 攝影機索引 {index} 可用")
                cap = test_cap
                working_index = index
                break
            else:
                print(f"❌ 攝影機索引 {index} 無法讀取畫面")
                test_cap.release()
        else:
            print(f"❌ 攝影機索引 {index} 無法開啟")
            test_cap.release()
    
    # 如果所有索引都失敗，嘗試使用不同的後端
    if cap is None:
        print("🔄 嘗試使用不同的攝影機後端...")
        backends = [cv2.CAP_AVFOUNDATION, cv2.CAP_V4L2, cv2.CAP_DSHOW]
        backend_names = ["AVFoundation (macOS)", "V4L2 (Linux)", "DirectShow (Windows)"]
        
        for i, backend in enumerate(backends):
            try:
                print(f"嘗試 {backend_names[i]} 後端...")
                test_cap = cv2.VideoCapture(0, backend)
                if test_cap.isOpened():
                    ret, frame = test_cap.read()
                    if ret and frame is not None:
                        print(f"✅ {backend_names[i]} 後端可用")
                        cap = test_cap
                        working_index = 0
                        break
                    else:
                        test_cap.release()
                else:
                    test_cap.release()
            except Exception as e:
                print(f"❌ {backend_names[i]} 後端失敗: {e}")
    
    # 檢查攝影機是否成功開啟
    if cap is None or not cap.isOpened():
        print("❌ 無法開啟任何攝影機，請檢查：")
        print("1. 攝影機是否被其他程式使用（如 Zoom、Teams、FaceTime 等）")
        print("2. 攝影機權限是否已開啟")
        print("   - macOS: 系統偏好設定 > 安全性與隱私 > 隱私權 > 攝影機")
        print("   - Windows: 設定 > 隱私權 > 攝影機")
        print("3. 攝影機是否正常連接")
        print("4. 嘗試重新啟動應用程式")
        if cap:
            cap.release()
        return
    
    print(f"✅ 成功開啟攝影機 (索引: {working_index})")
    
    # 設定攝影機參數
    print("⚙️ 設定攝影機參數...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # 驗證設定是否成功
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"📹 攝影機設定: {int(actual_width)}x{int(actual_height)} @ {actual_fps:.1f}fps")
    
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    lineType = cv2.LINE_AA

    # Game variables
    correct_count = 0
    target_number = None
    show_gift = False
    answer_confirmed = False
    answer_display_time = 0
    wrong_answer_confirmed = False  # New: track if wrong answer was confirmed
    stable_frames = 0  # New: count how many frames the same number appears
    last_detected_number = None  # New: keep track of the last detected number
    REQUIRED_STABLE_FRAMES = 45  # 延長至45幀 (約1.5秒) 讓孩童有更多時間穩定手勢
    
    # 延長時間設定，適合發展延遲的孩童
    PREPARATION_DELAY = 10  # 延長至10秒讓孩童有充足時間準備
    RESULT_DISPLAY_DELAY = 8  # 延長至8秒讓孩童有足夠時間理解結果
    
    # New: Game state variables
    game_state = "WAITING"  # States: WAITING, RECOGNIZING, SHOWING_RESULT
    state_start_time = time.time()
    countdown_value = PREPARATION_DELAY

    print("🤖 初始化 MediaPipe...")
    try:
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.4,  # 降低檢測門檻，讓手勢更容易被辨識
            min_tracking_confidence=0.4) as hands:  # 降低追蹤門檻，提高穩定性

            print("🎮 遊戲開始！按 'q' 退出，按 'r' 重新開始")
            w, h = 640, 480

            while True:
                ret, img = cap.read()
                if not ret:
                    print("❌ 無法讀取攝影機畫面")
                    break
                
                img = cv2.resize(img, (w,h))
                img = cv2.flip(img, 1)
                
                if target_number is None:
                    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                    game_state = "WAITING"
                    state_start_time = time.time()
                    countdown_value = PREPARATION_DELAY
                
                # Process the current game state
                current_time = time.time()
                elapsed_time = current_time - state_start_time
                
                # State: WAITING (preparation phase)
                if game_state == "WAITING":
                    # Update countdown timer
                    countdown_value = max(0, PREPARATION_DELAY - int(elapsed_time))
                    
                    # Display target number and countdown with larger, more visible text
                    img = put_chinese_text(img, f"準備好了嗎？請比出這個數字：", (30, 30), 25, (255, 255, 255))
                    cv2.putText(img, f"{target_number}", (w//2-40, h//2), 
                                fontFace, 6, (0, 255, 0), 8, lineType)  # 更大更粗的數字
                    img = put_chinese_text(img, f"倒數計時: {countdown_value} 秒", (30, 400), 35, (0, 165, 255))
                    img = put_chinese_text(img, f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255))
                    
                    # Move to recognition state after delay
                    if elapsed_time >= PREPARATION_DELAY:
                        game_state = "RECOGNIZING"
                        state_start_time = current_time
                        stable_frames = 0
                        last_detected_number = None
                
                # State: RECOGNIZING
                elif game_state == "RECOGNIZING":
                    # Display target number with encouraging message
                    img = put_chinese_text(img, f"請比出數字:", (30, 55), 35, (255, 255, 255))
                    cv2.putText(img, f"{target_number}", (100, 120),
                                fontFace, 4, (0, 255, 0), 6, lineType)  # 更大的目標數字
                    img = put_chinese_text(img, f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255))
                    
                    # 顯示穩定度進度條，讓孩童知道需要保持手勢
                    progress = min(stable_frames / REQUIRED_STABLE_FRAMES, 1.0)
                    bar_width = 200
                    bar_height = 20
                    bar_x = w - bar_width - 30
                    bar_y = 100
                    
                    # 繪製進度條背景
                    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
                    # 繪製進度條前景
                    cv2.rectangle(img, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
                    img = put_chinese_text(img, "保持手勢", (bar_x, bar_y - 30), 20, (255, 255, 255))
                    
                    # Hand gesture recognition
                    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = hands.process(img2)
                    
                    if results.multi_hand_landmarks:
                        hand_numbers = []
                        
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                img,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style())

                            finger_points = []
                            for i in hand_landmarks.landmark:
                                x = i.x*w
                                y = i.y*h
                                finger_points.append((x,y))
                            
                            if finger_points:
                                finger_angle = hand_angle(finger_points)
                                hand_number = hand_pos(finger_angle)
                                if hand_number:
                                    hand_numbers.append(hand_number)
                        
                        # Process detected hand gestures
                        if hand_numbers:
                            detected_numbers = sorted([int(num) for num in hand_numbers if num.isdigit()])
                            
                            # Show detected numbers with larger font
                            for i, num in enumerate(detected_numbers):
                                img = put_chinese_text(img, f"偵測到: {str(num)}", (30 + i*150, 180), 40, (221, 255, 97))
                            
                            # Get the first detected number (if any)
                            current_number = detected_numbers[0] if detected_numbers else None
                            
                            # Check if the number is stable
                            if current_number == last_detected_number:
                                stable_frames += 1
                            else:
                                stable_frames = 0
                                
                            last_detected_number = current_number
                            
                            # Only confirm answer after stable frames threshold
                            if stable_frames >= REQUIRED_STABLE_FRAMES:
                                game_state = "SHOWING_RESULT"
                                state_start_time = current_time
                                
                                if target_number in detected_numbers:
                                    answer_confirmed = True
                                    wrong_answer_confirmed = False
                                    correct_count += 1
                                    if correct_count >= 3:
                                        show_gift = True
                                else:
                                    answer_confirmed = False
                                    wrong_answer_confirmed = True
                    else:
                        # 沒有偵測到手勢時重置穩定幀數
                        stable_frames = 0
                        last_detected_number = None
                        img = put_chinese_text(img, "請將手放在鏡頭前", (30, 230), 35, (255, 255, 0))
                
                # State: SHOWING_RESULT
                elif game_state == "SHOWING_RESULT":
                    # Display remaining display time
                    remaining_time = max(0, RESULT_DISPLAY_DELAY - int(elapsed_time))
                    img = put_chinese_text(img, f"下一題倒數: {remaining_time} 秒", (w-250, 30), 30, (255, 255, 255))
                    
                    # Display target number
                    img = put_chinese_text(img, f"目標數字: {target_number}", (30, 30), 35, (255, 255, 255))
                    img = put_chinese_text(img, f"連續答對: {correct_count}/3", (30, 450), 30, (255, 255, 255))
                    
                    # Display 'Wonderful!' for completing 3 in a row
                    if show_gift:
                        img = put_chinese_text(img, "太棒了！", (w//2-80, h//2-70), 80, (255, 255, 255))
                        img = put_chinese_text(img, "連續答對3題！", (w//2-120, h//2), 45, (255, 255, 255))
                    # Display feedback based on answer
                    elif answer_confirmed:
                        img = put_chinese_text(img, "答對了！", (w//2-80, h//2-30), 80, (0, 255, 0))
                        img = put_chinese_text(img, "做得很好！", (w//2-90, h//2+40), 45, (0, 255, 0))
                    elif wrong_answer_confirmed:
                        img = put_chinese_text(img, "再試一次！", (w//2-90, h//2-30), 70, (0, 100, 255))
                        img = put_chinese_text(img, "沒關係，繼續加油！", (w//2-140, h//2+40), 35, (0, 100, 255))
                    
                    # Move to next number after delay
                    if elapsed_time >= RESULT_DISPLAY_DELAY:
                        if show_gift:
                            correct_count = 0
                            show_gift = False
                        target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                        game_state = "WAITING"
                        state_start_time = current_time
                        stable_frames = 0
                        last_detected_number = None
                        answer_confirmed = False
                        wrong_answer_confirmed = False

                cv2.imshow('Hand Gesture Game - 發展延遲孩童版', img)
                key = cv2.waitKey(5)
                if key == ord('q'):
                    break
                # Reset game if 'r' is pressed
                elif key == ord('r'):
                    correct_count = 0
                    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                    show_gift = False
                    answer_confirmed = False
                    wrong_answer_confirmed = False
                    stable_frames = 0
                    last_detected_number = None
                    game_state = "WAITING"
                    state_start_time = time.time()

    except Exception as e:
        print(f"❌ MediaPipe 初始化失敗: {e}")
    finally:
        print("🔄 清理資源...")
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        print("✅ 程式結束")

if __name__ == '__main__':
    main() 