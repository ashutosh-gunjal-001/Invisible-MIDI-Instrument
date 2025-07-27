import cv2
import mediapipe as mp
import time

try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import math
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    volume_range = volume.GetVolumeRange()
    min_volume = volume_range[0]
    max_volume = volume_range[1]
    
    print("Audio control initialized")
    os_control = "windows"
except:
    try:
        import osascript
        
        def set_volume_macos(volume_percent):
            vol = int(volume_percent * 7 / 100) 
            osascript.osascript(f"set volume {vol}")
            
        print("Audio control initialized for macOS")
        os_control = "macos"
    except:
        try:
            import alsaaudio
            
            mixer = alsaaudio.Mixer()
            print("Audio control initialized for Linux")
            os_control = "linux"
        except:
            print("Could not initialize volume control for your OS")
            os_control = "none"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cooldown = 0    
prev_finger_count = 0  
current_volume = 50 

def set_system_volume(volume_percent):
    volume_percent = max(0, min(100, volume_percent))
    
    if os_control == "windows":
        volume_value = min_volume + (max_volume - min_volume) * (volume_percent / 100)
        volume.SetMasterVolumeLevelScalar(volume_percent / 100, None)
    elif os_control == "macos":
        set_volume_macos(volume_percent)
    elif os_control == "linux":
        mixer.setvolume(int(volume_percent))
    
    return volume_percent

current_volume = set_system_volume(current_volume)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
        
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    results = hands.process(image_rgb)
        
    finger_count = 0
        
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
            fingertips = [8, 12, 16, 20]  
            thumb_tip = 4
            thumb_ip = 3  
            
            if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_ip].x:
                finger_count += 1
                
            for tip in fingertips:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    finger_count += 1
                    
            cv2.putText(image, f"Fingers: {finger_count}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
            if cooldown <= 0:
                if finger_count == 1 and prev_finger_count != 1:
                 
                    current_volume = set_system_volume(current_volume + 5)
                    print(f"Volume Up: {current_volume}%")
                    cooldown = 15
                elif finger_count == 2 and prev_finger_count != 2:

                    current_volume = set_system_volume(current_volume - 5)
                    print(f"Volume Down: {current_volume}%")
                    cooldown = 15
                    
            prev_finger_count = finger_count
    else:
        prev_finger_count = 0
        cv2.putText(image, "No hand detected", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    if cooldown > 0:
        cooldown -= 1
        
    cv2.putText(image, "1 finger: Volume Up, 2 fingers: Volume Down", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, f"Current Volume: {current_volume}%", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
    cv2.imshow('Hand Gesture Volume Control', image)
        
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
