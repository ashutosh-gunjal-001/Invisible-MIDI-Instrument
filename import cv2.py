import cv2
import mediapipe as mp
import time

# For controlling laptop volume
try:
    # For Windows
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import math
    
    # Get default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Get volume range
    volume_range = volume.GetVolumeRange()
    min_volume = volume_range[0]
    max_volume = volume_range[1]
    
    print("Audio control initialized")
    os_control = "windows"
except:
    try:
        # For macOS
        import osascript
        
        def set_volume_macos(volume_percent):
            vol = int(volume_percent * 7 / 100)  # macOS volume goes from 0-7
            osascript.osascript(f"set volume {vol}")
            
        print("Audio control initialized for macOS")
        os_control = "macos"
    except:
        try:
            # For Linux
            import alsaaudio
            
            mixer = alsaaudio.Mixer()
            print("Audio control initialized for Linux")
            os_control = "linux"
        except:
            print("Could not initialize volume control for your OS")
            os_control = "none"

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# For gesture detection
cooldown = 0    # Prevent rapid changes
prev_finger_count = 0  # Track previous finger count
current_volume = 50  # Start at 50% volume

# Function to set system volume
def set_system_volume(volume_percent):
    # Ensure volume is within 0-100 range
    volume_percent = max(0, min(100, volume_percent))
    
    if os_control == "windows":
        # Convert to Windows volume range (logarithmic)
        volume_value = min_volume + (max_volume - min_volume) * (volume_percent / 100)
        volume.SetMasterVolumeLevelScalar(volume_percent / 100, None)
    elif os_control == "macos":
        set_volume_macos(volume_percent)
    elif os_control == "linux":
        mixer.setvolume(int(volume_percent))
    
    return volume_percent

# Initialize volume
current_volume = set_system_volume(current_volume)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
        
    # Flip the image horizontally and convert BGR to RGB
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    # Process the image and detect hands
    results = hands.process(image_rgb)
        
    # Initialize finger count for this frame
    finger_count = 0
        
    # Draw hand landmarks and count fingers
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
            # Get landmarks for fingertips and finger bases
            fingertips = [8, 12, 16, 20]  # Index, middle, ring, pinky
            thumb_tip = 4
            thumb_ip = 3  # Interphalangeal joint of thumb
            
            # Count extended fingers (simplified approach)
            # Check if thumb is extended (comparing x-coordinates for thumb)
            if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_ip].x:
                finger_count += 1
                
            # Check if fingers are extended (comparing y-coordinates)
            for tip in fingertips:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    finger_count += 1
                    
            # Display finger count on screen
            cv2.putText(image, f"Fingers: {finger_count}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
            # Check cooldown before changing volume
            if cooldown <= 0:
                # Check for specific finger counts
                if finger_count == 1 and prev_finger_count != 1:
                    # Increase volume by 5%
                    current_volume = set_system_volume(current_volume + 5)
                    print(f"Volume Up: {current_volume}%")
                    cooldown = 15
                elif finger_count == 2 and prev_finger_count != 2:
                    # Decrease volume by 5%
                    current_volume = set_system_volume(current_volume - 5)
                    print(f"Volume Down: {current_volume}%")
                    cooldown = 15
                    
            # Update previous finger count
            prev_finger_count = finger_count
    else:
        # Reset previous finger count if no hand detected
        prev_finger_count = 0
        cv2.putText(image, "No hand detected", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    # Decrement cooldown counter
    if cooldown > 0:
        cooldown -= 1
        
    # Display instructions and current volume
    cv2.putText(image, "1 finger: Volume Up, 2 fingers: Volume Down", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, f"Current Volume: {current_volume}%", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
    cv2.imshow('Hand Gesture Volume Control', image)
        
    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
hands.close()