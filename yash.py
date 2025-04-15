# import os
# import random
# import time
# import tkinter as tk
# from tkinter import scrolledtext, messagebox, ttk, filedialog
# from PIL import Image, ImageDraw, ImageFont, ImageTk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import webbrowser
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from fpdf import FPDF
# import speech_recognition as sr
# import threading
# import ollama  # Added Ollama integration

# # Suppress macOS warnings
# os.environ['XPC_SERVICE_NAME'] = '0'

# class MentalHealthAIBot:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Mental Health Companion Pro+")
#         self.root.geometry("1400x900")
#         self.style = ttk.Style(theme='minty')
#         self.depression_score = 0
#         self.current_question = 0
#         self.diagnosis_active = False
#         self.user_responses = []
#         self.recognizer = sr.Recognizer()
#         self.conversation_history = []  # For AI context
        
#         # Hospital Database
#         self.hospitals = [
#             {
#                 "name": "Fortis Hospital",
#                 "address": "B-22, Sector 62, Gautam Budh Nagar, Greater Noida",
#                 "phone": "0120-240-2100",
#                 "specialty": "Psychiatry & Mental Health"
#             },
#             {
#                 "name": "Kailash Hospital",
#                 "address": "Gamma-I, Greater Noida, Uttar Pradesh 201310",
#                 "phone": "0120-232-6021",
#                 "specialty": "Mental Health Services"
#             }
#         ]

#         # Relaxation Exercises
#         self.relaxation_exercises = {
#             "4-7-8 Breathing": self.guide_478_breathing,
#             "Progressive Relaxation": self.guide_progressive_relaxation,
#             "5-4-3-2-1 Grounding": self.guide_54321_grounding
#         }

#         # Healing Music
#         self.healing_music = [
#             {"title": "Weightless", "url": "https://youtu.be/UfcAVejslrU"},
#             {"title": "Clair de Lune", "url": "https://youtu.be/CvFH_6DNRCY"}
#         ]

#         # GUI Setup
#         self.create_widgets()
#         self.show_typing_indicator("Welcome to Mental Health Companion Pro+! 🤖\nHow can I assist you today?")
        
#         # Diagnosis questions
#         self.diagnosis_questions = [
#             "How often do you feel sad or hopeless? (1: Never - 5: Always)",
#             "How would you rate your sleep quality? (1: Excellent - 5: Very Poor)",
#             "How is your appetite recently? (1: Normal - 5: No Appetite)",
#             "Do you have trouble concentrating? (1: Never - 5: Always)",
#             "How often do you feel fatigued? (1: Never - 5: Always)"
#         ]

#     # ... (Keep all existing methods unchanged until process_input)

#     def process_input(self, event=None):
#         user_text = self.user_input.get()
#         if not user_text:
#             return
        
#         self.show_message("You", user_text)
#         self.user_input.delete(0, tk.END)
        
#         if self.diagnosis_active:
#             self.handle_diagnosis(user_text)
#         else:
#             self.handle_ai_response(user_text)  # Changed to AI response handler

#     def handle_ai_response(self, user_input):
#         """Handle responses using Ollama AI"""
#         self.conversation_history.append({"role": "user", "content": user_input})
        
#         # Start a thread for AI processing
#         threading.Thread(target=self.generate_ai_response, args=(user_input,), daemon=True).start()

#     def generate_ai_response(self, user_input):
#         """Generate response using Ollama model"""
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=self.conversation_history,
#                 options={'temperature': 0.7}
#             )
#             ai_response = response['message']['content']
#             self.conversation_history.append({"role": "assistant", "content": ai_response})
#             self.show_typing_indicator(ai_response)
#         except Exception as e:
#             self.show_message("Bot", f"⚠️ AI Service Error: {str(e)}")
#             self.handle_basic_response(user_input)  # Fallback to basic responses

#     def generate_affirmation(self):
#         """Generate positive affirmation using AI"""
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=[{"role": "user", "content": "Provide a positive affirmation for someone struggling with mental health"}]
#             )
#             return response['message']['content']
#         except Exception as e:
#             return "Remember: You're stronger than you think! 💪"

#     def generate_meditation_guide(self):
#         """Generate guided meditation using AI"""
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=[{"role": "user", "content": "Provide a 5-minute guided meditation script for stress relief"}]
#             )
#             return response['message']['content']
#         except Exception as e:
#             return "Close your eyes and focus on your breath. Inhale deeply for 4 counts, hold for 4, exhale for 6. Repeat."

#     def create_action_buttons(self, parent):
#         action_frame = ttk.Frame(parent)
#         action_frame.pack(fill=tk.X, pady=10)
        
#         buttons = [
#             ("Start Diagnosis", self.start_diagnosis, 'primary'),
#             ("View Report", self.generate_report, 'info'),
#             ("Music Therapy", self.recommend_music, 'success'),
#             ("Find Hospitals", self.show_hospitals, 'warning'),
#             ("Positive Affirmation", self.show_affirmation, 'light'),
#             ("Guided Meditation", self.show_meditation, 'dark'),
#             ("Exit", self.root.destroy, 'danger')
#         ]
        
#         for text, command, style in buttons:
#             ttk.Button(
#                 action_frame,
#                 text=text,
#                 command=command,
#                 bootstyle=style,
#                 width=20
#             ).pack(side=tk.LEFT, padx=5, pady=2)

#     def show_affirmation(self):
#         """Show AI-generated affirmation"""
#         def generate_and_show():
#             affirmation = self.generate_affirmation()
#             self.show_typing_indicator(f"✨ Affirmation: {affirmation}")
        
#         threading.Thread(target=generate_and_show, daemon=True).start()

#     def show_meditation(self):
#         """Show AI-generated meditation guide"""
#         def generate_and_show():
#             meditation = self.generate_meditation_guide()
#             self.show_typing_indicator(f"🧘 Guided Meditation:\n\n{meditation}")
        
#         threading.Thread(target=generate_and_show, daemon=True).start()

#     def handle_basic_response(self, user_input):
#         """Fallback responses when AI isn't available"""
#         responses = {
#             'hello': "Hello! How can I help you today?",
#             'help': "I'm here to listen. You can:\n- Chat naturally with me\n- Start a diagnosis\n- Try relaxation exercises\n- Request music recommendations\n- Find local hospitals",
#             'stress': "Let's try a quick breathing exercise! Check the relaxation panel →",
#             'sad': "I'm sorry to hear that. Would you like to try the 5-4-3-2-1 grounding exercise?",
#             'default': "I'm here to support you. Could you tell me more about how you're feeling?"
#         }
        
#         response = responses.get(user_input.lower(), responses['default'])
#         self.show_typing_indicator(response)

#     # ... (Keep all other existing methods unchanged)

# if __name__ == "__main__":
#     root = ttk.Window()
#     bot = MentalHealthAIBot(root)
#     root.mainloop()


# import os
# import random
# import time
# import tkinter as tk
# from tkinter import scrolledtext, messagebox, ttk, filedialog
# from PIL import Image, ImageDraw, ImageFont, ImageTk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import webbrowser
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from fpdf import FPDF
# import speech_recognition as sr
# import threading
# import ollama

# # Suppress macOS warnings
# os.environ['XPC_SERVICE_NAME'] = '0'

# class MentalHealthAIBot:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Mental Health Companion Pro+")
#         self.root.geometry("1400x900")
#         self.style = ttk.Style(theme='minty')
#         self.depression_score = 0
#         self.current_question = 0
#         self.diagnosis_active = False
#         self.user_responses = []
#         self.recognizer = sr.Recognizer()
#         self.conversation_history = []
        
#         # Hospital Database
#         self.hospitals = [
#             {
#                 "name": "Fortis Hospital",
#                 "address": "B-22, Sector 62, Gautam Budh Nagar, Greater Noida",
#                 "phone": "0120-240-2100",
#                 "specialty": "Psychiatry & Mental Health"
#             },
#             {
#                 "name": "Kailash Hospital",
#                 "address": "Gamma-I, Greater Noida, Uttar Pradesh 201310",
#                 "phone": "0120-232-6021",
#                 "specialty": "Mental Health Services"
#             }
#         ]

#         # Relaxation Exercises (moved after method definitions)
#         self.relaxation_exercises = {
#             "4-7-8 Breathing": self.guide_478_breathing,
#             "Progressive Relaxation": self.guide_progressive_relaxation,
#             "5-4-3-2-1 Grounding": self.guide_54321_grounding
#         }

#         # Healing Music
#         self.healing_music = [
#             {"title": "Weightless", "url": "https://youtu.be/UfcAVejslrU"},
#             {"title": "Clair de Lune", "url": "https://youtu.be/CvFH_6DNRCY"}
#         ]

#         # GUI Setup
#         self.create_widgets("jd")
#         self.show_typing_indicator("Welcome to Mental Health Companion Pro+! 🤖\nHow can I assist you today?")
        
#         # Diagnosis questions
#         self.diagnosis_questions = [
#             "How often do you feel sad or hopeless? (1: Never - 5: Always)",
#             "How would you rate your sleep quality? (1: Excellent - 5: Very Poor)",
#             "How is your appetite recently? (1: Normal - 5: No Appetite)",
#             "Do you have trouble concentrating? (1: Never - 5: Always)",
#             "How often do you feel fatigued? (1: Never - 5: Always)"
#         ]

#     # ... [Keep all other methods the same until relaxation exercises]

#     def guide_478_breathing(self):
#         steps = [
#             ("🔄 Sit comfortably and relax your shoulders", 2000),
#             ("🌬️ Empty your lungs completely", 1000),
#             ("🫁 Inhale quietly through nose for 4 seconds...", 4000),
#             ("⏳ Hold breath for 7 seconds...", 7000),
#             ("😮💨 Exhale completely through mouth for 8 seconds...", 8000),
#             ("✨ Repeat this cycle 3-4 times", 2000)
#         ]
#         self.guided_exercise(steps)

#     def guide_progressive_relaxation(self):
#         steps = [
#             ("🪑 Sit or lie down comfortably", 2000),
#             ("👊 Tense your hand muscles for 5 seconds...", 5000),
#             ("✋ Release and relax for 30 seconds...", 30000),
#             ("👣 Move to feet muscles: Tense...", 5000),
#             ("🦶 Release and relax...", 30000),
#             ("🔄 Continue through all muscle groups", 2000)
#         ]
#         self.guided_exercise(steps)

#     def guide_54321_grounding(self):
#         steps = [
#             ("🌍 Notice 5 things you can see around you", 5000),
#             ("✋ Name 4 things you can touch", 4000),
#             ("👂 Identify 3 sounds you can hear", 3000),
#             ("👃 Notice 2 things you can smell", 2000),
#             ("💪 Name 1 thing you can do right now", 1000),
#             ("🌈 Grounding complete. Feel more present?", 2000)
#         ]
#         self.guided_exercise(steps)

#     # ... [Rest of the code remains unchanged]

# if __name__ == "__main__":
#     root = ttk.Window()
#     bot = MentalHealthAIBot(root)
#     root.mainloop()


# import os
# import random
# import time
# import tkinter as tk
# from tkinter import scrolledtext, messagebox, ttk, filedialog
# from PIL import Image, ImageDraw, ImageFont, ImageTk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import webbrowser
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from fpdf import FPDF
# import speech_recognition as sr
# import threading
# import ollama

# # Suppress macOS warnings
# os.environ['XPC_SERVICE_NAME'] = '0'

# class MentalHealthAIBot:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Mental Health Companion Pro+")
#         self.root.geometry("1400x900")
#         self.style = ttk.Style(theme='minty')
#         self.depression_score = 0
#         self.current_question = 0
#         self.diagnosis_active = False
#         self.user_responses = []
#         self.recognizer = sr.Recognizer()
#         self.conversation_history = []
        
#         # Hospital Database
#         self.hospitals = [
#             {
#                 "name": "Fortis Hospital",
#                 "address": "B-22, Sector 62, Gautam Budh Nagar, Greater Noida",
#                 "phone": "0120-240-2100",
#                 "specialty": "Psychiatry & Mental Health"
#             },
#             {
#                 "name": "Kailash Hospital",
#                 "address": "Gamma-I, Greater Noida, Uttar Pradesh 201310",
#                 "phone": "0120-232-6021",
#                 "specialty": "Mental Health Services"
#             }
#         ]

#         # Relaxation Exercises
#         self.relaxation_exercises = {
#             "4-7-8 Breathing": self.guide_478_breathing,
#             "Progressive Relaxation": self.guide_progressive_relaxation,
#             "5-4-3-2-1 Grounding": self.guide_54321_grounding
#         }

#         # Healing Music
#         self.healing_music = [
#             {"title": "Weightless", "url": "https://youtu.be/UfcAVejslrU"},
#             {"title": "Clair de Lune", "url": "https://youtu.be/CvFH_6DNRCY"}
#         ]

#         # Initialize GUI components
#         self.create_widgets()
#         self.show_typing_indicator("Welcome to Mental Health Companion Pro+! 🤖\nHow can I assist you today?")
        
#         # Diagnosis questions
#         self.diagnosis_questions = [
#             "How often do you feel sad or hopeless? (1: Never - 5: Always)",
#             "How would you rate your sleep quality? (1: Excellent - 5: Very Poor)",
#             "How is your appetite recently? (1: Normal - 5: No Appetite)",
#             "Do you have trouble concentrating? (1: Never - 5: Always)",
#             "How often do you feel fatigued? (1: Never - 5: Always)"
#         ]

#     def load_image(self, emoji, size=40):
#         """Create emoji image with proper font handling"""
#         img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
#         d = ImageDraw.Draw(img)
#         try:
#             font = ImageFont.truetype("seguiemj.ttf", 32)
#         except:
#             try:
#                 font = ImageFont.truetype("Apple Color Emoji.ttf", 32)
#             except:
#                 font = ImageFont.load_default()
#         d.text((10, 0), emoji, font=font, fill="black")
#         return ImageTk.PhotoImage(img)

#     def create_widgets(self):
#         main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
#         main_paned.pack(fill=tk.BOTH, expand=True)

#         # Left Panel (Main Chat)
#         left_frame = ttk.Frame(main_paned)
#         main_paned.add(left_frame, weight=3)

#         # Right Panel (Relaxation Exercises)
#         right_frame = ttk.Frame(main_paned)
#         main_paned.add(right_frame, weight=1)

#         # Chat Components
#         header_frame = ttk.Frame(left_frame)
#         header_frame.pack(fill=tk.X, pady=10)
        
#         self.logo = self.load_image("🧠", size=40)
#         ttk.Label(header_frame, image=self.logo).pack(side=tk.LEFT, padx=10)
#         ttk.Label(header_frame, text="Mental Health Companion Pro", 
#                  font=('Arial', 18, 'bold')).pack(side=tk.LEFT)
        
#         self.viz_frame = ttk.Frame(left_frame)
#         self.viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         self.chat_history = scrolledtext.ScrolledText(
#             left_frame, 
#             wrap=tk.WORD, 
#             state='disabled',
#             font=('Arial', 12),
#             background='#ffffff',
#             padx=15,
#             pady=15
#         )
#         self.chat_history.pack(fill=tk.BOTH, expand=True, pady=10)

#         input_frame = ttk.Frame(left_frame)
#         input_frame.pack(fill=tk.X, pady=10)
        
#         self.user_input = ttk.Entry(
#             input_frame, 
#             font=('Arial', 14),
#             bootstyle='primary'
#         )
#         self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
#         self.user_input.bind("<Return>", self.process_input)
        
#         ttk.Button(
#             input_frame,
#             text="🎤 Speak",
#             command=self.start_voice_recognition,
#             bootstyle='info'
#         ).pack(side=tk.LEFT, padx=5)
        
#         ttk.Button(
#             input_frame, 
#             text="Send", 
#             command=self.process_input,
#             bootstyle='success'
#         ).pack(side=tk.LEFT, padx=5)

#         self.create_action_buttons(left_frame)
#         self.create_relaxation_panel(right_frame)

#     def create_relaxation_panel(self, parent):
#         exercise_frame = ttk.Labelframe(parent, text="Relaxation Exercises", padding=10)
#         exercise_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         for exercise in self.relaxation_exercises:
#             ttk.Button(
#                 exercise_frame,
#                 text=exercise,
#                 command=lambda e=exercise: self.start_exercise(e),
#                 bootstyle="light",
#                 width=25
#             ).pack(pady=5, fill=tk.X)

#         ttk.Separator(exercise_frame).pack(fill=tk.X, pady=10)
#         ttk.Label(exercise_frame, text="Quick Stress Relief:", font=('Arial', 10)).pack()
#         ttk.Button(
#             exercise_frame,
#             text="Instant Calm",
#             command=lambda: self.guided_exercise([
#                 ("🌬️ Take a deep breath", 2000),
#                 ("🤚 Hold for 3 seconds", 3000),
#                 ("😮💨 Exhale slowly", 4000),
#                 ("🔄 Repeat 3 times", 1000)
#             ]),
#             bootstyle="outline"
#         ).pack(pady=5)

#     def start_exercise(self, exercise_name):
#         self.show_typing_indicator(f"Starting {exercise_name}...")
#         self.root.after(1500, self.relaxation_exercises[exercise_name])

#     def guide_478_breathing(self):
#         steps = [
#             ("🔄 Sit comfortably and relax your shoulders", 2000),
#             ("🌬️ Empty your lungs completely", 1000),
#             ("🫁 Inhale quietly through nose for 4 seconds...", 4000),
#             ("⏳ Hold breath for 7 seconds...", 7000),
#             ("😮💨 Exhale completely through mouth for 8 seconds...", 8000),
#             ("✨ Repeat this cycle 3-4 times", 2000)
#         ]
#         self.guided_exercise(steps)

#     def guide_progressive_relaxation(self):
#         steps = [
#             ("🪑 Sit or lie down comfortably", 2000),
#             ("👊 Tense your hand muscles for 5 seconds...", 5000),
#             ("✋ Release and relax for 30 seconds...", 30000),
#             ("👣 Move to feet muscles: Tense...", 5000),
#             ("🦶 Release and relax...", 30000),
#             ("🔄 Continue through all muscle groups", 2000)
#         ]
#         self.guided_exercise(steps)

#     def guide_54321_grounding(self):
#         steps = [
#             ("🌍 Notice 5 things you can see around you", 5000),
#             ("✋ Name 4 things you can touch", 4000),
#             ("👂 Identify 3 sounds you can hear", 3000),
#             ("👃 Notice 2 things you can smell", 2000),
#             ("💪 Name 1 thing you can do right now", 1000),
#             ("🌈 Grounding complete. Feel more present?", 2000)
#         ]
#         self.guided_exercise(steps)

#     def guided_exercise(self, steps):
#         def next_step(index=0):
#             if index < len(steps):
#                 text, delay = steps[index]
#                 self.show_message("Guide", text)
#                 self.root.after(delay, next_step, index+1)
#             else:
#                 self.show_message("Guide", "Exercise complete! 🎉")
        
#         threading.Thread(target=next_step, daemon=True).start()

#     def create_action_buttons(self, parent):
#         action_frame = ttk.Frame(parent)
#         action_frame.pack(fill=tk.X, pady=10)
        
#         buttons = [
#             ("Start Diagnosis", self.start_diagnosis, 'primary'),
#             ("View Report", self.generate_report, 'info'),
#             ("Music Therapy", self.recommend_music, 'success'),
#             ("Find Hospitals", self.show_hospitals, 'warning'),
#             ("Positive Affirmation", self.show_affirmation, 'light'),
#             ("Guided Meditation", self.show_meditation, 'dark'),
#             ("Exit", self.root.destroy, 'danger')
#         ]
        
#         for text, command, style in buttons:
#             ttk.Button(
#                 action_frame,
#                 text=text,
#                 command=command,
#                 bootstyle=style,
#                 width=20
#             ).pack(side=tk.LEFT, padx=5, pady=2)

#     def show_typing_indicator(self, message):
#         self.chat_history.configure(state='normal')
#         self.chat_history.insert(tk.END, "🤖 Bot is typing...\n")
#         self.chat_history.see(tk.END)
#         self.chat_history.configure(state='disabled')
#         self.root.after(1500, lambda: self.update_message(message))

#     def update_message(self, message):
#         self.chat_history.configure(state='normal')
#         self.chat_history.delete("end-2l", "end-1c")
#         self.chat_history.insert(tk.END, f"🤖 Bot: {message}\n\n")
#         self.chat_history.configure(state='disabled')
#         self.chat_history.see(tk.END)

#     def show_message(self, sender, message):
#         self.chat_history.configure(state='normal')
#         self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
#         self.chat_history.configure(state='disabled')
#         self.chat_history.see(tk.END)

#     def process_input(self, event=None):
#         user_text = self.user_input.get()
#         if not user_text:
#             return
        
#         self.show_message("You", user_text)
#         self.user_input.delete(0, tk.END)
        
#         if self.diagnosis_active:
#             self.handle_diagnosis(user_text)
#         else:
#             self.handle_ai_response(user_text)

#     def handle_ai_response(self, user_input):
#         self.conversation_history.append({"role": "user", "content": user_input})
#         threading.Thread(target=self.generate_ai_response, daemon=True).start()

#     def generate_ai_response(self):
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=self.conversation_history,
#                 options={'temperature': 0.7}
#             )
#             ai_response = response['message']['content']
#             self.conversation_history.append({"role": "assistant", "content": ai_response})
#             self.show_typing_indicator(ai_response)
#         except Exception as e:
#             self.show_message("Bot", f"⚠️ AI Service Error: {str(e)}")
#             self.handle_basic_response()

#     def generate_affirmation(self):
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=[{"role": "user", "content": "Provide a positive affirmation for someone struggling with mental health"}]
#             )
#             return response['message']['content']
#         except:
#             return "Remember: You're stronger than you think! 💪"

#     def generate_meditation_guide(self):
#         try:
#             response = ollama.chat(
#                 model="llama3:8b",
#                 messages=[{"role": "user", "content": "Provide a 5-minute guided meditation script for stress relief"}]
#             )
#             return response['message']['content']
#         except:
#             return "Close your eyes and focus on your breath. Inhale deeply for 4 counts, hold for 4, exhale for 6. Repeat."

#     def show_affirmation(self):
#         def generate_and_show():
#             affirmation = self.generate_affirmation()
#             self.show_typing_indicator(f"✨ Affirmation: {affirmation}")
#         threading.Thread(target=generate_and_show, daemon=True).start()

#     def show_meditation(self):
#         def generate_and_show():
#             meditation = self.generate_meditation_guide()
#             self.show_typing_indicator(f"🧘 Guided Meditation:\n\n{meditation}")
#         threading.Thread(target=generate_and_show, daemon=True).start()

#     def handle_basic_response(self):
#         responses = {
#             'hello': "Hello! How can I help you today?",
#             'help': "I'm here to listen. You can:\n- Chat naturally with me\n- Start a diagnosis\n- Try relaxation exercises\n- Request music recommendations\n- Find local hospitals",
#             'stress': "Let's try a quick breathing exercise! Check the relaxation panel →",
#             'sad': "I'm sorry to hear that. Would you like to try the 5-4-3-2-1 grounding exercise?",
#             'default': "I'm here to support you. Could you tell me more about how you're feeling?"
#         }
#         response = responses.get('default', responses['default'])
#         self.show_typing_indicator(response)

#     # Rest of the original methods (diagnosis, visualization, report generation, etc.)
#     # ... [Include all other methods from previous implementation]

# if __name__ == "__main__":
#     root = ttk.Window()
#     bot = MentalHealthAIBot(root)
#     root.mainloop()


import os
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF
import threading
from datetime import datetime

# Suppress macOS warnings
os.environ['XPC_SERVICE_NAME'] = '0'

class MentalHealthAIBot:
    def __init__(self, root):
        self.root = root
        self.root.title("SoulSupport – A digital friend for mental wellness")
        self.root.geometry("1400x900")
        self.style = ttk.Style(theme='minty')  # Default theme
        self.dark_mode = False
        self.mood_data = {}  # Stores mood data: {date: mood_score}
        self.depression_score = 0
        self.current_question = 0
        self.diagnosis_active = False
        self.user_responses = []

        # Hospital Database
        self.hospitals = [
            {
                "name": "Fortis Hospital",
                "address": "B-22, Sector 62, Gautam Budh Nagar, Greater Noida",
                "phone": "0120-240-2100",
                "specialty": "Psychiatry & Mental Health"
            },
            {
                "name": "Kailash Hospital",
                "address": "Gamma-I, Greater Noida, Uttar Pradesh 201310",
                "phone": "0120-232-6021",
                "specialty": "Mental Health Services"
            }
        ]

        # Healing Music
        self.healing_music = [
            {"title": "Weightless", "url": "https://youtu.be/UfcAVejslrU"},
            {"title": "Clair de Lune", "url": "https://youtu.be/CvFH_6DNRCY"}
        ]

        # Diagnosis questions
        self.diagnosis_questions = [
            "How often do you feel sad or hopeless? (1: Never - 5: Always)",
            "How would you rate your sleep quality? (1: Excellent - 5: Very Poor)",
            "How is your appetite recently? (1: Normal - 5: No Appetite)",
            "Do you have trouble concentrating? (1: Never - 5: Always)",
            "How often do you feel fatigued? (1: Never - 5: Always)"
        ]

        # GUI Setup
        self.create_widgets()
        self.show_typing_indicator("Welcome to SoulSupport – A digital friend for mental wellness 🤖\nHow can I assist you today?")

    def create_widgets(self):
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # Left Panel (Main Chat)
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)

        # Chat Components
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=tk.X, pady=10)

        ttk.Label(header_frame, text="SoulSupport – A digital friend for mental wellness",
                 font=('Arial', 18, 'bold')).pack(side=tk.LEFT)

        # Dark Mode Toggle
        self.dark_mode_button = ttk.Button(
            header_frame,
            text="🌙 Dark Mode",
            command=self.toggle_dark_mode,
            bootstyle="outline"
        )
        self.dark_mode_button.pack(side=tk.RIGHT, padx=10)

        self.viz_frame = ttk.Frame(left_frame)
        self.viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.chat_history = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            state='disabled',
            font=('Arial', 12),
            background='#ffffff',
            foreground='#000000',
            padx=15,
            pady=15
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=10)

        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X, pady=10)

        self.user_input = ttk.Entry(
            input_frame,
            font=('Arial', 14),
            bootstyle='primary'
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind("<Return>", self.process_input)

        ttk.Button(
            input_frame,
            text="Send",
            command=self.process_input,
            bootstyle='success'
        ).pack(side=tk.LEFT, padx=5)

        self.create_action_buttons(left_frame)

        # Safe Space Section
        self.create_safe_space(left_frame)

    def create_safe_space(self, parent):
        """Create a Safe Space section for users to express themselves."""
        safe_space_frame = ttk.Labelframe(parent, text="Safe Space", padding=10)
        safe_space_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.safe_space_text = scrolledtext.ScrolledText(
            safe_space_frame,
            wrap=tk.WORD,
            font=('Arial', 12),
            height=10,
            padx=10,
            pady=10
        )
        self.safe_space_text.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(safe_space_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            button_frame,
            text="Save Entry",
            command=self.save_safe_space_entry,
            bootstyle="info"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Share with Bot",
            command=self.share_with_bot,
            bootstyle="success"
        ).pack(side=tk.LEFT, padx=5)

    def save_safe_space_entry(self):
        """Save the Safe Space entry to a local file."""
        entry = self.safe_space_text.get("1.0", tk.END).strip()
        if not entry:
            messagebox.showwarning("Empty Entry", "Please write something before saving.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if filename:
            with open(filename, "w") as file:
                file.write(entry)
            messagebox.showinfo("Entry Saved", "Your Safe Space entry has been saved successfully.")

    def share_with_bot(self):
        """Share the Safe Space entry with the bot for a supportive response."""
        entry = self.safe_space_text.get("1.0", tk.END).strip()
        if not entry:
            messagebox.showwarning("Empty Entry", "Please write something before sharing.")
            return

        self.show_typing_indicator("Thank you for sharing your thoughts. I'm here to listen and support you. 🤗")
        self.safe_space_text.delete("1.0", tk.END)  # Clear the text box after sharing

    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.style.theme_use('darkly')
            self.chat_history.configure(background='#2d2d2d', foreground='#ffffff')
            self.dark_mode_button.configure(text="☀️ Light Mode")
        else:
            self.style.theme_use('minty')
            self.chat_history.configure(background='#ffffff', foreground='#000000')
            self.dark_mode_button.configure(text="🌙 Dark Mode")

    def create_action_buttons(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=10)

        buttons = [
            ("Start Diagnosis", self.start_diagnosis, 'primary'),
            ("View Report", self.generate_report, 'info'),
            ("Music Therapy", self.recommend_music, 'success'),
            ("Find Hospitals", self.show_hospitals, 'warning'),
            ("Track Mood", self.track_mood, 'secondary'),
            ("Exit", self.root.destroy, 'danger')
        ]

        for text, command, style in buttons:
            ttk.Button(
                action_frame,
                text=text,
                command=command,
                bootstyle=style
            ).pack(side=tk.LEFT, padx=5)

    def start_diagnosis(self):
        self.diagnosis_active = True
        self.depression_score = 0
        self.current_question = 0
        self.user_responses = []
        self.show_typing_indicator(self.diagnosis_questions[self.current_question])

    def handle_diagnosis(self, answer):
        try:
            score = int(answer)
            if 1 <= score <= 5:
                self.user_responses.append(score)
                self.depression_score += score
                self.current_question += 1

                if self.current_question < len(self.diagnosis_questions):
                    self.show_typing_indicator(self.diagnosis_questions[self.current_question])
                else:
                    self.visualize_depression_level()
                    self.show_results()
            else:
                self.show_typing_indicator("Please enter a number between 1-5")
        except ValueError:
            self.show_typing_indicator("Please enter a valid number")

    def visualize_depression_level(self):
        fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        categories = ['Sadness', 'Sleep', 'Appetite', 'Concentration', 'Fatigue']
        values = self.user_responses[-5:]

        ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD'])
        ax.set_ylim(0, 5)
        ax.set_title('Depression Level Analysis')

        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_results(self):
        total = self.depression_score
        if total <= 10:
            msg = "🌼 Mild Symptoms: Practice self-care!"
        elif total <= 15:
            msg = "📞 Moderate Symptoms: Consider professional help"
        else:
            msg = "🚨 Severe Symptoms: Immediate consultation recommended"
            self.show_hospitals()

        msg += f"\n\nYour score: {total}/25"
        self.show_typing_indicator(msg)
        self.diagnosis_active = False

    def generate_report(self):
        if not self.user_responses:
            self.show_message("Bot", "⚠️ No assessment data available!")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        plt.savefig("temp_chart.png", bbox_inches='tight')

        pdf.cell(200, 10, txt="Mental Health Assessment Report", ln=1, align='C')
        pdf.ln(10)

        for idx, response in enumerate(self.user_responses):
            pdf.multi_cell(0, 10,
                f"Q{idx+1}: {self.diagnosis_questions[idx]}\nScore: {response}\n")

        pdf.image("temp_chart.png", x=10, y=100, w=180)

        pdf.add_page()
        pdf.cell(200, 10, txt="Recommendations:", ln=1)
        recommendations = [
            "1. Practice mindfulness daily",
            "2. Maintain regular sleep schedule",
            "3. Engage in physical activity",
            "4. Consider professional counseling"
        ]
        for rec in recommendations:
            pdf.cell(200, 10, txt=rec, ln=1)

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if filename:
            pdf.output(filename)
            self.show_message("Bot", f"✅ Report saved: {filename}")

    def show_hospitals(self):
        hospital_info = "\n\n".join([
            f"🏥 {h['name']}\n📍 {h['address']}\n📞 {h['phone']}\nSpecialty: {h['specialty']}"
            for h in self.hospitals
        ])
        self.show_typing_indicator(f"Mental Health Hospitals in Greater Noida:\n\n{hospital_info}")

    def recommend_music(self):
        music_list = "\n".join([f"🎵 {song['title']}" for song in self.healing_music])
        self.show_typing_indicator(f"Recommended Music:\n{music_list}")
        webbrowser.open(self.healing_music[0]['url'])

    def track_mood(self):
        """Track user's mood and visualize it."""
        mood_window = tk.Toplevel(self.root)
        mood_window.title("Track Your Mood")
        mood_window.geometry("300x200")

        ttk.Label(mood_window, text="How are you feeling today?", font=('Arial', 12)).pack(pady=10)

        mood_score = tk.IntVar()
        ttk.Scale(
            mood_window,
            from_=1,
            to=5,
            variable=mood_score,
            length=200,
            orient=tk.HORIZONTAL
        ).pack(pady=10)

        ttk.Button(
            mood_window,
            text="Submit",
            command=lambda: self.save_mood(mood_score.get(), mood_window),
            bootstyle="success"
        ).pack(pady=10)

    def save_mood(self, score, window):
        """Save mood data and update visualization."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.mood_data[today] = score
        self.visualize_mood()
        window.destroy()
        self.show_message("Bot", f"✅ Mood logged for today: {score}/5")

    def visualize_mood(self):
        """Visualize mood data using a line chart."""
        if not self.mood_data:
            return

        dates = list(self.mood_data.keys())
        scores = list(self.mood_data.values())

        fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, scores, marker='o', color='#4ECDC4')
        ax.set_title('Mood Tracker')
        ax.set_ylim(0, 5)
        ax.set_xlabel('Date')
        ax.set_ylabel('Mood Score')

        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_typing_indicator(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, "🤖 Bot is typing...\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')
        self.root.after(1500, lambda: self.update_message(message))

    def update_message(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.delete("end-2l", "end-1c")
        self.chat_history.insert(tk.END, f"🤖 Bot: {message}\n\n")
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def show_message(self, sender, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def process_input(self, event=None):
        user_text = self.user_input.get()
        if not user_text:
            return

        self.show_message("You", user_text)
        self.user_input.delete(0, tk.END)

        if self.diagnosis_active:
            self.handle_diagnosis(user_text)
        else:
            self.handle_basic_response(user_text)

    def handle_basic_response(self, user_input):
        responses = {
            'hello': "Hello! How can I help you today?",
            'help': "I'm here to listen. You can:\n- Start a diagnosis\n- Try relaxation exercises\n- Request music recommendations\n- Find local hospitals",
            'stress': "Let's try a quick breathing exercise! Check the relaxation panel →",
            'sad': "I'm sorry to hear that. Would you like to try the 5-4-3-2-1 grounding exercise?",
            'default': "I'm here to support you. Could you tell me more about how you're feeling?"
        }

        response = responses.get(user_input.lower(), responses['default'])
        self.show_typing_indicator(response)

if __name__ == "__main__":
    root = ttk.Window()
    bot = MentalHealthAIBot(root)
    root.mainloop()