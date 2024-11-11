import tkinter as tk
from datetime_display import update_time 
from flashcard import generate_flashcards  
import time
import random

BACKGROUND_COLOR = "#2C3E50"  
TEXT_COLOR = "#ECF0F1"        
SECONDARY_TEXT_COLOR = "#BDC3C7"  
ACCENT_COLOR = "#E67E22"      
HOVER_COLOR = "#FFA04B"       
BUTTON_TEXT_COLOR = "#FFFFFF" 
BORDER_COLOR = "#34495E"      


def on_enter(e):
    e.widget['background'] = HOVER_COLOR

def on_leave(e):
    e.widget['background'] = ACCENT_COLOR

def display_flashcards(flashcards, text_widget):
    """Display flashcards in the text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)  

    for keyword, explanation in flashcards.items():
        if isinstance(explanation, list):
            explanation_text = ' '.join(explanation)
        else:
            explanation_text = explanation

        text_widget.insert(tk.END, f"Q:What is  {keyword} ?\n", "bold")  
        text_widget.insert(tk.END, f"A: {explanation_text}\n\n")

    text_widget.config(state=tk.DISABLED)

def update_time_with_day(label, root):
    def refresh():
        current_time = time.strftime("%A, %B %d, %Y - %H:%M:%S")
        label.config(text=current_time)
        root.after(1000, refresh)  
    refresh()

def open_note_popup():
    note_popup = tk.Toplevel(root)
    note_popup.title("Enter Notes")
    note_popup.geometry("1000x600")  
    note_popup.configure(bg=BACKGROUND_COLOR)  

    note_entry = tk.Text(note_popup, wrap=tk.WORD, font=("Helvetica", 12), height=20, width=80, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
    note_entry.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  

    def process_notes():
        notes = note_entry.get("1.0", tk.END).strip()  
        if not notes:
            tk.messagebox.showwarning("Warning", "Please enter some notes before submitting.")
            return
        
        flashcards = generate_flashcards(notes)  
        if flashcards:
            root.flashcards = flashcards
            display_flashcards(flashcards, left_text_area)
            note_popup.destroy()
        else:
            tk.messagebox.showerror("Error", "Failed to generate flashcards from the notes.")

    submit_button = tk.Button(note_popup, text="Submit Notes", command=process_notes, bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, relief=tk.FLAT)
    submit_button.pack(pady=20)


    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)

def test_yourself():
    if not hasattr(root, 'flashcards') or not root.flashcards:
        return
    c = len(root.flashcards)
    questions = list(root.flashcards.items())

    def next_question():
        nonlocal c
        random_number = random.randint(0, c - 1)
        
        question, answer = questions[random_number]

        result_popup = tk.Toplevel(root)
        result_popup.title("Test Yourself")
        result_popup.geometry("600x400")
        result_popup.configure(bg=BACKGROUND_COLOR)  # Set background color

        question_label = tk.Label(result_popup, text=f"Q: {question}", font=("Helvetica", 14), wraplength=550, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        question_label.pack(pady=20)

        answer_entry = tk.Text(result_popup, wrap=tk.WORD, font=("Helvetica", 12), height=8, width=50, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
        answer_entry.pack(pady=20)

        feedback_label = tk.Label(result_popup, text="", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=SECONDARY_TEXT_COLOR)
        feedback_label.pack(pady=20)

        def check_answer():
            user_answer = answer_entry.get("1.0", tk.END).strip().lower()
            
            if isinstance(answer, list):
                correct_answer = ' '.join(answer).strip().lower()
            else:
                correct_answer = answer.strip().lower()

            feedback = "Correct!" if user_answer == correct_answer else f"Incorrect! The correct answer is: {correct_answer}"
            feedback_label.config(text=feedback)

        submit_button = tk.Button(result_popup, text="Submit Answer", command=check_answer, bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, relief=tk.FLAT)
        submit_button.pack(pady=10)

        next_button = tk.Button(result_popup, text="Next Question", command=lambda: [result_popup.destroy(), next_question()], bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, relief=tk.FLAT)
        next_button.pack(pady=10)

        
        submit_button.bind("<Enter>", on_enter)
        submit_button.bind("<Leave>", on_leave)
        next_button.bind("<Enter>", on_enter)
        next_button.bind("<Leave>", on_leave)

    next_question()

root = tk.Tk()
root.title("GUI Layout")
root.geometry("950x600") 
root.configure(bg=BACKGROUND_COLOR)  


top_frame = tk.Frame(root, borderwidth=2, relief="groove", padx=10, pady=10, bg=BORDER_COLOR)
top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)

top_label = tk.Label(top_frame, text="", font=("Helvetica", 16, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
top_label.pack(fill=tk.BOTH, expand=True)


left_frame = tk.Frame(root, borderwidth=2, relief="groove", padx=10, pady=10, bg=BORDER_COLOR)
left_frame.place(relx=0, rely=0.15, relwidth=0.5, relheight=0.85)

left_text_area = tk.Text(left_frame, wrap=tk.WORD, font=("Helvetica", 11), height=10, width=50, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
left_text_area.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(left_frame, command=left_text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
left_text_area.config(yscrollcommand=scrollbar.set)


center_frame = tk.Frame(root, borderwidth=2, relief="groove", padx=10, pady=10, bg=BORDER_COLOR)
center_frame.place(relx=0.5, rely=0.15, relwidth=0.25, relheight=0.35)

center_label = tk.Label(center_frame, text="Performance Overview", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"))
center_label.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(center_frame, bg=BACKGROUND_COLOR)
button_frame.pack(side=tk.BOTTOM, pady=10)

open_note_button = tk.Button(button_frame, text="Enter Notes", command=open_note_popup, bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, relief=tk.FLAT)
open_note_button.pack(side=tk.LEFT, padx=5)

test_button = tk.Button(button_frame, text="Test Yourself", command=test_yourself, bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, relief=tk.FLAT)
test_button.pack(side=tk.LEFT, padx=5)


open_note_button.bind("<Enter>", on_enter)
open_note_button.bind("<Leave>", on_leave)
test_button.bind("<Enter>", on_enter)
test_button.bind("<Leave>", on_leave)


prop_frame = tk.Frame(root, borderwidth=2, relief="groove", padx=10, pady=10, bg=BORDER_COLOR)
prop_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

prop_label = tk.Label(prop_frame, text="Prop Area", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"))
prop_label.pack(fill=tk.BOTH, expand=True)

update_time_with_day(top_label, root)

root.mainloop()
