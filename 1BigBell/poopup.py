import tkinter as tk #GUI program w/ mouse & keyboard
from collections import deque #built-in list thing
from pynput import keyboard #self-explanatory 
from PIL import Image, ImageSequence, ImageTk
import pygame #graphics, sounds, etc
import os

# Changeables ------------------------------
# FILES
BASE = os.path.dirname(os.path.abspath(__file__))
SOUND = os.path.join(BASE, "assets", "sound.mp3")
GIF = os.path.join(BASE, "assets", "GIF.gif")
IMAGE = os.path.join(BASE, "assets", "image.jpg")
#

#SIZE
IMAGE_SIZE = None
GIF_SIZE = None

MODE = "image" #fading "image" or "GIF"
#

TRIGGER = "help"
EXIT_PHRASE = "exit poopup"

# -------------------------------------------
buffer = deque(maxlen=max(len(TRIGGER), len(EXIT_PHRASE)))     #holds 9 chars

KEY = "#FF00FE"   #colors of this pixel become transparent, like a greenscreen (?)
FADE_STEP = 0.05    #opacity change per tick
FADE_INTERVAL = 15  #ms between fade ticks (timer)
HOLD_MS =  1200     #time image stays full opacity

pygame.mixer.init()

def play_sound():
    try:
        pygame.mixer.music.load(SOUND)      #get sound
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()           #plays loaded sound
    except Exception as e:
        print("Sound error:", e)            #error message

def load_image(path, size):
    img = Image.open(path).convert("RGBA")      #puts into RGB format
    if size:
        img = img.resize(size, Image.LANCZOS)   #fancy ahh algorithm
    keyed = Image.new("RGB", img.size, KEY)
    keyed.paste(img, mask = img.split()[3])
    return ImageTk.PhotoImage(keyed) 

def load_gif_frames(path, size):
    img = Image.open(path)                                  #opens gif path
    frames, durations = [], []
    for frame in ImageSequence.Iterator(img):
        rgba = frame.convert("RGBA")
        if size:
            rgba = rgba.resize(size, Image.LANCZOS)
        keyed = Image.new("RGB", rgba.size, KEY)            #makes transparent = key color
        keyed.paste(rgba, mask=rgba.split()[3])             #makes GIF have mask
        frames.append(ImageTk.PhotoImage(keyed))
        durations.append(frame.info.get("duration", 80))    #per-frame delay in ms
    return frames, durations

def play_popup(w, h, start_alpha):                                
    win = tk.Toplevel(root)
    win.overrideredirect(True)                    #kills title bar
    win.attributes("-topmost", True)            #puts GUI on very top, fish will be seen.
    win.attributes("-transparentcolor", KEY)    #KEY-colored pixel = transparent
    win.attributes("-alpha", start_alpha)
    win.config(bg=KEY)
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")            #center on screen math bullshit
    return win

def image_fade():
    play_sound()        #what do you think buddy
    win = play_popup(image_frame.width(), image_frame.height(), 0.0)
    label = tk.Label(win, image=image_frame, bg=KEY, bd=0)
    label.image = image_frame #reference so not garbage collected
    label.pack()

    def fade(alpha, direction):
        alpha += direction * FADE_STEP
        if direction < 0 and alpha <= 0:
            win.destroy()
            return
        if direction > 0 and alpha >= 1:
            win.attributes("-alpha", 1.0)
            win.after(HOLD_MS, fade, 1.0, -1)   #hold then fade
            return
        win.attributes("-alpha", alpha)
        win.after(FADE_INTERVAL, fade, alpha, direction)

    fade(0.0, 1)

def gif_popup():
    play_sound()
    win = play_popup(gif_frames[0].width(), gif_frames[0].height(), 1.0)
    label = tk.Label(win, bg=KEY, bd=0)
    label.pack()

    def animate(i):                             #gif stuff im assuming
        if i >= len(gif_frames):
            win.destroy()                       #destroy feels a bit excessive
            return
        label.config(image=gif_frames[i])
        win.after(gif_durations[i], animate, i+1)

    animate(0)

def shutdown():
    try:
        listener.stop()
    except Exception:
        pass
    pygame.mixer.quit()
    root.destroy()   # ends the event loop and exits the program

def on_press(key):
    if key == keyboard.Key.esc:
        root.after(0, shutdown)
        return False
    try:
        char = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            char = " "
        else:
            return
    if char is None:
        return
    buffer.append(char.lower())
    text = "".join(buffer)
    if text.endswith(TRIGGER):
        root.after(0, image_fade if MODE == "image" else gif_popup)
        buffer.clear()
    elif text.endswith(EXIT_PHRASE):
        root.after(0, shutdown)
        return False

root = tk.Tk()
root.withdraw()

#load MODE asset, image or GIF
if MODE == "image":
    image_frame = load_image(IMAGE, IMAGE_SIZE)
if MODE == "GIF":
    gif_frames, gif_durations = load_gif_frames(GIF, GIF_SIZE)    #preload gif path

listener = keyboard.Listener(on_press = on_press)
listener.start()

root.mainloop()

#lord help me