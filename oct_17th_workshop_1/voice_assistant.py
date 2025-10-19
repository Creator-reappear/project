import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess
import platform
import psutil
import threading
import speech_recognition as sr
import pyttsx3
import time
import math
import os

# === SETTINGS ===
user_name = "Creator"   # Change to your name!
circle_color = "#6c63ff"  # Panda's background circle color
panda_size = 180     # Size

engine = pyttsx3.init()
engine_lock = threading.Lock()

def speak(text):
    with engine_lock:
        engine.say(text)
        engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, phrase_time_limit=10)
            query = r.recognize_google(audio)
            print("You said:", query)
            return query
        except Exception:
            return ""

def handle_command(text):
    text = text.lower()

    def is_process_running(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] is not None and proc.info['name'].lower() == process_name.lower():
                return True
        return False

    # --- Closing Apps ---
    if "close chrome" in text:
        if is_process_running("chrome.exe"):
            subprocess.call('taskkill /IM chrome.exe /F', shell=True)
            return "Chrome has been closed!"
        else:
            return "Chrome is not opened!"
    if "close whatsapp" in text:
        if is_process_running("WhatsApp.exe"):
            subprocess.call('taskkill /IM WhatsApp.exe /F', shell=True)
            return "WhatsApp closed!"
        else:
            return "WhatsApp is not opened!"
    if "close camera" in text:
        if is_process_running("WindowsCamera.exe"):
            subprocess.call('taskkill /IM WindowsCamera.exe /F', shell=True)
            return "Camera closed!"
        else:
            return "Camera is not opened!"

    # --- Opening Apps ---
    if "open google" in text:
        os.startfile("https://www.google.com/?zx=1760805251126&no_sw_cr=1")
        return "Google is opened!"
    if "open camera" in text or "camera" in text:
        os.system("start microsoft.windows.camera:")
        return "Camera is opened!"
    if "open whatsapp" in text or "whatsapp" in text:
        try:
            os.startfile(r"https://web.whatsapp.com/")
            return "WhatsApp opened!"
        except Exception:
            return "Couldn't find WhatsApp."

            # --- ONLY exit the agent if these commands ---
    if text in ["bye", "close yourself", "exit for now", "exit program", "quit agent"]:
        return f"Goodbye, {user_name}! (Agent will now exit)"

    # --- Other Commands ---
    if "joke" in text:
        return "Why do pandas love coding? Because it's full of bamboo-zling logic!"
    if "bye" in text or "close" in text or "exit" in text:
        return f"Goodbye, {user_name}!"
    if "how are you" in text:
        return f"I'm all smiles, {user_name}!"
    if "your name" in text or "who are you" in text or "what is your name" in text or "what's your name" in text:
        return "I'm your friendly Panda Assistant!"    
    if text.strip():
        return "You said: " + text
    else:
        return "Sorry, I didn't catch that."

def create_circle_panda_with_bg(img_path, size, circle_color):
    panda = Image.open(img_path).convert("RGBA").resize((size-8, size-8), Image.Resampling.LANCZOS)
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    draw.ellipse((0, 0, size, size), fill=circle_color)
    bg.paste(panda, (4, 4), mask=panda)
    return bg

class PandaAssistant:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'white')
        self.width, self.height = 250, 130
        self.root.config(bg='white')
        self.root.geometry(f"{self.width}x{self.height}+0+250")

        panda_img = create_circle_panda_with_bg("panda.png", panda_size, circle_color)
        self.panda_photo = ImageTk.PhotoImage(panda_img)
        self.panda_label = tk.Label(root, image=self.panda_photo, bg='white', bd=0, highlightthickness=0)
        self.panda_label.place(x=10, y=17)

        self.bubble = tk.Label(root, text="", bg="#fafafa", fg="#111111",
            font=("Arial", 13), wraplength=142, justify="right",
            bd=2, relief="solid", padx=8, pady=5)
        self.bubble.place(x=105, y=28, width=135, height=62)

        self.glow_canvas = tk.Canvas(root, width=panda_size, height=panda_size, bg='white', highlightthickness=0)
        self.glow_canvas.place(x=10, y=17)
        self.glow_id = None

        tk.Button(root, text="✖", command=self.root.destroy, bg="#f94449", fg="#fff",
                  font=("Arial", 9, "bold"), bd=0, highlightthickness=0, activebackground="#fff"
        ).place(x=self.width-26, y=8, width=18, height=18)

        self.animate_wave_in()

    def animate_wave_in(self):
        frames = 35
        amplitude = 32
        dest_x = self.root.winfo_screenwidth() - self.width - 14
        start_x = 0
        for i in range(frames+1):
            progress = i / frames
            x = int(start_x + (dest_x - start_x) * progress)
            y = int(250 + amplitude * math.sin(math.pi * progress))
            self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
            self.root.update()
            time.sleep(0.016)
        self.root.geometry(f"{self.width}x{self.height}+{dest_x}+{y}")
        self.start_glow()
        self.bubble.config(text=f"Hey {user_name}! What should I do for you?")
        threading.Thread(target=speak, args=(f"Hey {user_name}! What should I do for you?",), daemon=True).start()
        self.root.after(1200, self.start_chat)

    def start_glow(self):
        for r in range(31, 43, 2):
            self.glow_canvas.delete("glow")
            self.glow_canvas.create_oval(panda_size//2 - r, panda_size//2 - r, panda_size//2 + r, panda_size//2 + r,
                                         fill="#dedcff", outline="", tags="glow")
            self.root.update()
            time.sleep(0.018)
        self.glow_canvas.delete("glow")
        self.glow_canvas.create_oval(25, 25, 67, 67, fill="#cecfff", outline="", tags="glow")
        self.root.update()

    def start_chat(self):
        def loop():
            while True:
                user_input = listen()
                if user_input.lower() in ["bye", "close yourself", "exit for now"]:
                    self.bubble.config(text=f"Goodbye, {user_name}!")
                    speak(f"Goodbye, {user_name}!")
                    time.sleep(1)
                    self.root.destroy()
                    break
                if user_input:
                    response = handle_command(user_input)
                    self.bubble.config(text=response)
                    threading.Thread(target=speak, args=(response,), daemon=True).start()
                else:
                    #self.bubble.config(text="Didn't catch that, try again!")
                    threading.Thread(target=speak, args=("Didn't catch that, try again!",), daemon=True).start()
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PandaAssistant(root)
    root.mainloop()