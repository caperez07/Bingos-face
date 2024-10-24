import paho.mqtt.client as mqtt
import threading
import tkinter as tk
from PIL import Image, ImageTk
import imageio
import random
import time

# MQTT settings
HOST = "192.168.137.6"
TOPIC = "bingo-rosto"

# Define the on_connect callback function for MQTT
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

# Define the on_message callback function for MQTT
def on_message(mqttc, obj, msg):
    byte_string = msg.payload
    decoded_string = byte_string.decode('utf-8')
    clean_string = decoded_string.strip('"')
    print("MENSAGEM: " + str(clean_string))

    if(str(clean_string) == 'ouvindo'):
        listen_face()
    elif(str(clean_string) == 'falando'):
        speech_face()

# Define the MQTT thread that runs the loop
def mqtt_thread():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(HOST)
    mqttc.subscribe(TOPIC)
    mqttc.loop_forever()

# Function to start MQTT in a separate thread
def start_mqtt():
    mqtt_thread_instance = threading.Thread(target=mqtt_thread)
    mqtt_thread_instance.daemon = True  # Daemon allows the program to close properly
    mqtt_thread_instance.start()

# Function to preload video frames
def preload_frames(video_path, screen_width, screen_height):
    reader = imageio.get_reader(video_path)
    frames = []
    for frame in reader:
        img = Image.fromarray(frame)
        img = img.resize((screen_width, screen_height))  # Resize to fit the screen
        img_tk = ImageTk.PhotoImage(img)
        frames.append(img_tk)
    reader.close()
    return frames

# Function to play video in the label
def play_video():
    global frame_index, video_playing, current_frames
    if video_playing:
        try:
            frame = current_frames[frame_index]
            label.config(image=frame)
            label.image = frame
            frame_index += 1
            if frame_index >= len(current_frames):
                if current_frames != normal_frames:
                    current_frames = normal_frames
                    frame_index = 0
                    enable_clicks()
                else:
                    frame_index = 0
        except IndexError:
            frame_index = 0

    root.after(20, play_video)

# Function to disable mouse clicks
def disable_clicks():
    label.unbind("<ButtonPress-1>")
    label.unbind("<ButtonRelease-1>")

# Function to enable mouse clicks
def enable_clicks():
    label.bind("<ButtonPress-1>", on_mouse_down)
    label.bind("<ButtonRelease-1>", on_mouse_up)

# Mouse event functions
def on_mouse_down(event):
    global mouse_down_time
    mouse_down_time = time.time()

def on_mouse_up(event):
    global mouse_down_time, video_playing, current_frames, frame_index
    if mouse_down_time is not None:
        click_duration = time.time() - mouse_down_time
        mouse_down_time = None
        if click_duration >= long_click_duration:
            current_frames = happy_frames  # Long click
            print("Long click detected")
        else:
            current_frames = random.choice([sad_frames, angry_frames])  # Short click
            print("Short click detected")

        disable_clicks()
        frame_index = 0
        video_playing = True

# Function called when MQTT message arrives (simulate facial recognition)
def listen_face():
    print("Listening for face...")
    global current_frames, frame_index, video_playing
    current_frames = listen_frames
    frame_index = 0
    video_playing = True

def speech_face():
    print("Listening for face...")
    global current_frames, frame_index, video_playing
    current_frames = speech_frames
    frame_index = 0
    video_playing = True

# Video paths
normalBingo = 'videos/Normal_Bingo.gif'
angryBingo = 'videos/Angry_Bingo.gif'
sadBingo = 'videos/Sad_Bingo.gif'
happyBingo = 'videos/Happy_Bingo.gif'
listenBingo = 'videos/Hear_Bingo.gif'
speechBingo = 'videos/Talk_Bingo.gif'

fastClick = [sadBingo, angryBingo]

# Initialize the Tkinter root window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(cursor="none")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Initialize the Tkinter label to display the video
label = tk.Label(root)
label.pack()

# Preload the frames for each video
normal_frames = preload_frames(normalBingo, screen_width, screen_height)
angry_frames = preload_frames(angryBingo, screen_width, screen_height)
sad_frames = preload_frames(sadBingo, screen_width, screen_height)
happy_frames = preload_frames(happyBingo, screen_width, screen_height)
listen_frames = preload_frames(listenBingo, screen_width, screen_height)
speech_frames = preload_frames(speechBingo, screen_width, screen_height)

# Initialize the variables for video playback
current_frames = normal_frames
frame_index = 0
mouse_down_time = None
long_click_duration = 0.5  # Seconds to define a long click
video_playing = True

# Bind mouse events for interaction
label.bind("<ButtonPress-1>", on_mouse_down)
label.bind("<ButtonRelease-1>", on_mouse_up)

# Start video playback in the Tkinter GUI
root.after(20, play_video)

# Start the MQTT client in a separate thread
start_mqtt()

# Start the Tkinter main loop
root.mainloop()
