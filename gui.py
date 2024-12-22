import tkinter as tk
from datetime_display import update_time
from flashcard import generate_flashcards
import time
import random
from tkinter import messagebox


def display_flashcards(flashcards, text_widget):
    """Display flashcards in the text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)

    for keyword, explanation in flashcards.items():
        explanation_text = ' '.join(explanation) if isinstance(explanation, list) else explanation
        text_widget.insert(tk.END, f"Q: What is {keyword}?\n", "bold")
        text_widget.insert(tk.END, f"A: {explanation_text}\n\n")
    
    text_widget.config(state=tk.DISABLED)


def update_time_with_day(label, root):
    """Continuously update the current time and day."""
    def refresh():
        current_time = time.strftime("%A, %B %d, %Y - %H:%M:%S")
        label.config(text=current_time)
        root.after(1000, refresh)
    refresh()


def open_note_popup():
    """Open a popup for entering notes."""
    note_popup = tk.Toplevel(root)
    note_popup.title("Enter Notes")
    note_popup.geometry("1000x600")

    note_entry = tk.Text(note_popup, wrap=tk.WORD, font=("Helvetica", 12), height=20, width=80)
    note_entry.pack(fill=tk.BOTH, expand=True)

    def process_notes():
        notes = note_entry.get("1.0", tk.END).strip()
        if not notes:
            messagebox.showwarning("Warning", "Please enter some notes before submitting.")
            return
        
        flashcards = generate_flashcards(notes)
        if flashcards:
            root.flashcards = flashcards
            display_flashcards(flashcards, left_text_area)
            note_popup.destroy()
        else:
            messagebox.showerror("Error", "Failed to generate flashcards from the notes.")

    submit_button = tk.Button(note_popup, text="Submit Notes", command=process_notes)
    submit_button.pack(pady=10)


def test_yourself():
    """Test the user with flashcard questions."""
    if not hasattr(root, 'flashcards') or not root.flashcards:
        messagebox.showinfo("Info", "No flashcards available. Please add notes first.")
        return

    questions = list(root.flashcards.items())

    def show_question():
        if not questions:
            messagebox.showinfo("Info", "You've completed all questions!")
            return
        
        question, answer = random.choice(questions)
        questions.remove((question, answer))

        result_popup = tk.Toplevel(root)
        result_popup.title("Test Yourself")
        result_popup.geometry("600x400")

        tk.Label(result_popup, text=f"Q: {question}", font=("Helvetica", 14), wraplength=550).pack(pady=10)

        answer_entry = tk.Text(result_popup, wrap=tk.WORD, font=("Helvetica", 12), height=8, width=50)
        answer_entry.pack(pady=10)

        feedback_label = tk.Label(result_popup, text="", font=("Helvetica", 12))
        feedback_label.pack(pady=10)

        def check_answer():
            user_answer = answer_entry.get("1.0", tk.END).strip().lower()
            correct_answer = ' '.join(answer).strip().lower() if isinstance(answer, list) else answer.strip().lower()
            feedback = "Correct!" if user_answer == correct_answer else f"Incorrect! The correct answer is: {correct_answer}"
            feedback_label.config(text=feedback)

        tk.Button(result_popup, text="Submit Answer", command=check_answer).pack(pady=10)
        tk.Button(result_popup, text="Next Question", command=lambda: [result_popup.destroy(), show_question()]).pack(pady=10)

    show_question()


# Main Application
root = tk.Tk()
root.title("Flashcard Learning Tool")
root.geometry("800x400")

# Top Frame for Time Display
top_frame = tk.Frame(root, borderwidth=1, relief="solid")
top_frame.place(relx=0, rely=0, relwidth=0.75, relheight=0.15)

top_label = tk.Label(top_frame, text="", font=("Helvetica", 14))
top_label.pack(fill=tk.BOTH, expand=True)

# Left Frame for Flashcard Display
left_frame = tk.Frame(root, borderwidth=1, relief="solid")
left_frame.place(relx=0, rely=0.15, relwidth=0.5, relheight=0.85)

left_text_area = tk.Text(left_frame, wrap=tk.WORD, font=("Helvetica", 10), state=tk.DISABLED)
left_text_area.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(left_frame, command=left_text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
left_text_area.config(yscrollcommand=scrollbar.set)

# Center Frame for Buttons
center_frame = tk.Frame(root, borderwidth=1, relief="solid")
center_frame.place(relx=0.5, rely=0.15, relwidth=0.25, relheight=0.35)

center_label = tk.Label(center_frame, text="Performance Overview")
center_label.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(center_frame)
button_frame.pack(side=tk.BOTTOM, pady=10)

tk.Button(button_frame, text="Enter Notes", command=open_note_popup).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Test Yourself", command=test_yourself).pack(side=tk.LEFT, padx=5)

# Prop Frame for Future Features
prop_frame = tk.Frame(root, borderwidth=1, relief="solid")
prop_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

prop_label = tk.Label(prop_frame, text="Prop Area")
prop_label.pack(fill=tk.BOTH, expand=True)

# Start Time Display
update_time_with_day(top_label, root)

root.mainloop()
