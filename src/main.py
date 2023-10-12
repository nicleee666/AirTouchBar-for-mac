import cv2
import time
import subprocess
import math
from hand_detector import HandDetector

action_start_time = None
current_action = None
action_performed = False

# AppleScript Functions
def set_volume(level):
    #current_level = get_volume()
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])

def get_volume():
    result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
    return int(result.stdout.strip())
def get_music_state():
    player_state = subprocess.run(["osascript", "-e", 'tell application "Music" to get player state as string'], capture_output=True, text=True).stdout.strip()
    return player_state

def play_music():
    subprocess.run(["osascript", "-e", 'tell application "Music" to play'])

def pause_music():
    subprocess.run(["osascript", "-e", 'tell application "Music" to pause'])

def next_track():
    subprocess.run(["osascript", "-e", 'tell application "Music" to next track'])

def previous_track():
    subprocess.run(["osascript", "-e", 'tell application "Music" to previous track'])

def set_brightness(level):
    subprocess.run(["osascript", "-e", f'set brightness of display 1 to {level}'])

last_time = 0  # Initialize last_time to keep track of time between volume changes

def control_volume(landmark_list, current_volume):
    global last_time  # Use the global variable to keep track of time between function calls
    
    thumb_tip = landmark_list[4]
    index_tip = landmark_list[8]
    length = math.sqrt((thumb_tip[1] - index_tip[1]) ** 2 + (thumb_tip[2] - index_tip[2]) ** 2)
    
    current_time = time.time()
    
    if current_time - last_time >= 1:  # One second has passed
        if length < 40:  # Voluming down
            current_volume = max(0, current_volume - 10)  # Decrease by 5 Apple volume bar
        elif length < 110:
            current_volume = max(0, current_volume - 5) 
        elif length < 170:  # Voluming up
            current_volume = min(100, current_volume + 5)  # Increase by one Apple volume bar
        else:
            current_volume = min(100, current_volume + 10) 
        set_volume(int(current_volume))
        last_time = current_time  # Update last_time
    
    return current_volume

def soundtrack_selection(landmark_list):
    thumb_base_x = landmark_list[1][1]
    pinky_base_x = landmark_list[17][1]
        
    # Determine palm direction
    if thumb_base_x > pinky_base_x:
        next_track()
        #time.sleep(1)  # Delay to prevent rapid track changes
        return 'next track'
    else:
        previous_track()
        #time.sleep(1)  # Delay to prevent rapid track changes
        return 'last track'

def is_pinch(landmark_list):
    if len(landmark_list) < 21:  # Mediapipe hand model has 21 landmarks
        return False
    thumb_tip = landmark_list[4]
    index_tip = landmark_list[8]
    middle_tip = landmark_list[12]
    ring_tip = landmark_list[16]
    pinky_tip = landmark_list[20]
    wrist = landmark_list[0]
    
    
    wrist_ring = math.sqrt((wrist[1] - ring_tip[1]) ** 2 + (wrist[2] - ring_tip[2]) ** 2)
    wrist_index =math.sqrt((wrist[1] - index_tip[1]) ** 2 + (wrist[2] - index_tip[2]) ** 2) 

    # Check if thumb is far enough from all other fingertips
    if wrist_ring < 130 and wrist_index >160:
        return True
    
    return False

def is_palm(landmark_list):
    thumb_tip = landmark_list[4]
    index_tip = landmark_list[8]
    middle_tip = landmark_list[12]
    ring_tip = landmark_list[16]
    pinky_tip = landmark_list[20]
    wrist = landmark_list[0]

    wrist_ring = math.sqrt((wrist[1] - ring_tip[1]) ** 2 + (wrist[2] - ring_tip[2]) ** 2) 
    wrist_index =math.sqrt((wrist[1] - index_tip[1]) ** 2 + (wrist[2] - index_tip[2]) ** 2) 
    wrist_middle =math.sqrt((wrist[1] - middle_tip[1]) ** 2 + (wrist[2] - middle_tip[2]) ** 2) 
    wrist_pinky =math.sqrt((wrist[1] - pinky_tip[1]) ** 2 + (wrist[2] - pinky_tip[2]) ** 2) 

    if all(dist > 160 for dist in [wrist_ring, wrist_index, wrist_middle, wrist_pinky]):
        return True
    return False

def is_fist(landmard_list):
    thumb_tip = landmark_list[4]
    index_tip = landmark_list[8]
    middle_tip = landmark_list[12]
    ring_tip = landmark_list[16]
    pinky_tip = landmark_list[20]
    wrist = landmark_list[0]

    wrist_ring = math.sqrt((wrist[1] - ring_tip[1]) ** 2 + (wrist[2] - ring_tip[2]) ** 2) 
    wrist_index =math.sqrt((wrist[1] - index_tip[1]) ** 2 + (wrist[2] - index_tip[2]) ** 2) 
    wrist_middle =math.sqrt((wrist[1] - middle_tip[1]) ** 2 + (wrist[2] - middle_tip[2]) ** 2) 
    wrist_pinky =math.sqrt((wrist[1] - pinky_tip[1]) ** 2 + (wrist[2] - pinky_tip[2]) ** 2) 

    if all(dist < 150 for dist in [wrist_ring, wrist_index, wrist_middle, wrist_pinky]):
        return True
    return False 


detector = HandDetector()

# Capture video stream
cap = cv2.VideoCapture(0)

last_action_time = 0
last_action = ""
last_text_update = 0
display_text = ""

while True:
    success, frame = cap.read()
    frame = detector.find_hands(frame)
    landmark_list = detector.get_hand_location(frame)
    
    current_time = time.time()

    if current_time - last_action_time >= 2:  # 2 seconds threshold for a new action
        if landmark_list:
            if is_pinch(landmark_list):
                current_volume = get_volume()
                volume = control_volume(landmark_list, current_volume)
                display_text = f'Volume: {volume}%'
                last_text_update = current_time
                last_action = "volume"
                
            elif is_palm(landmark_list):
                soundtrack = soundtrack_selection(landmark_list)
                display_text = f'{soundtrack}'
                last_text_update = current_time
                last_action = "track"

            elif is_fist(landmark_list):
                player_state = get_music_state()
                if player_state == "playing":
                    pause_music()
                    display_text = "Music Paused"
                else:
                    play_music()
                    display_text = "Music Playing"
                last_text_update = current_time
                last_action = "play_pause"

            last_action_time = current_time  # Update last_action_time

    if current_time - last_text_update < 3:  # 3 seconds
        cv2.putText(frame, display_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Visual", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
