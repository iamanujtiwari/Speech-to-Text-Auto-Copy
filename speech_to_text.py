import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import threading
import pyperclip

recognizer = sr.Recognizer()
is_listening = False

def listen_and_transcribe():
    global is_listening
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while is_listening:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="hi-IN")
                text_display.insert(tk.END, text + '\n')
                text_display.see(tk.END)
                pyperclip.copy(text)  # auto-copy to clipboard
            except sr.UnknownValueError:
                text_display.insert(tk.END, "Could not understand audio\n")
            except sr.RequestError as e:
                text_display.insert(tk.END, f"Request error: {e}\n")
            except Exception as ex:
                text_display.insert(tk.END, f"Error: {str(ex)}\n")

def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        threading.Thread(target=listen_and_transcribe).start()
        status_label.config(text="🎤 Listening...")

def stop_listening():
    global is_listening
    is_listening = False
    status_label.config(text="⛔ Stopped Listening")
    messagebox.showinfo("Stopped", "Speech recognition stopped.")

# UI Setup
root = tk.Tk()
root.title("Hindi Speech to Text")
root.geometry("500x400")

status_label = tk.Label(root, text="Press Start to begin", font=("Helvetica", 12))
status_label.pack(pady=10)

text_display = tk.Text(root, wrap=tk.WORD, height=15, font=("Helvetica", 12))
text_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

start_btn = tk.Button(root, text="Start Listening", command=start_listening, bg="green", fg="white", font=("Helvetica", 12))
start_btn.pack(side=tk.LEFT, padx=20, pady=10)

stop_btn = tk.Button(root, text="Stop Listening", command=stop_listening, bg="red", fg="white", font=("Helvetica", 12))
stop_btn.pack(side=tk.RIGHT, padx=20, pady=10)

root.mainloop()
