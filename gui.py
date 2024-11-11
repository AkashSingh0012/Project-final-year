import tkinter as tk
from datetime_display import update_time 
from flashcard import generate_flashcards  
import time
import random

def display_flashcards(flashcards, text_widget):
    """Display flashcards in the text widget."""
    text_widget.delete("1.0", tk.END)  

   
    for keyword, explanation in flashcards.items():
        
        if isinstance(explanation, list):
            explanation_text = ' '.join(explanation)
        else:
            explanation_text = explanation  

        
        text_widget.insert(tk.END, f"Q:what is  {keyword} ?\n", "bold")  
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

    note_entry = tk.Text(note_popup, wrap=tk.WORD, font=("Helvetica", 12), height=20, width=80)
    note_entry.pack(fill=tk.BOTH, expand=True)

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

    submit_button = tk.Button(note_popup, text="Submit Notes", command=process_notes)
    submit_button.pack(pady=10)

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

        question_label = tk.Label(result_popup, text=f"Q: {question}", font=("Helvetica", 14), wraplength=550)
        question_label.pack(pady=10)

       
        answer_entry = tk.Text(result_popup, wrap=tk.WORD, font=("Helvetica", 12), height=8, width=50)
        answer_entry.pack(pady=10)

        feedback_label = tk.Label(result_popup, text="", font=("Helvetica", 12))
        feedback_label.pack(pady=10)

        def check_answer():
            user_answer = answer_entry.get("1.0", tk.END).strip().lower()  
            
            if isinstance(answer, list):
                correct_answer = ' '.join(answer).strip().lower()
            else:
                correct_answer = answer.strip().lower()

            if user_answer == correct_answer:
                feedback = "Correct!"
            else:
                feedback = f"Incorrect! The correct answer is: {correct_answer}"

            feedback_label.config(text=feedback)  

        submit_button = tk.Button(result_popup, text="Submit Answer", command=check_answer)
        submit_button.pack(pady=10)

        next_button = tk.Button(result_popup, text="Next Question", command=lambda: [result_popup.destroy(), next_question()])
        next_button.pack(pady=10)

    next_question()  
  
'''#future implementation code<gui code working is ok but responses are wrong>
def chatbot_response(user_input):
    user_input = user_input.lower()  # Normalize user input
    for keyword, explanation in root.flashcards.items():
        if keyword.lower() in user_input:  # Check if any keyword matches
            return f"{explanation}"  # Return the explanation for the matched keyword
    return "I'm not sure how to respond to that."

def display_chat_response():
    user_input = chat_entry.get().strip()  
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n")  
        response = chatbot_response(user_input)  
        chat_display.insert(tk.END, f"Bot: {response}\n\n")  
        chat_entry.delete(0, tk.END)  

'''
root = tk.Tk()
root.title("GUI Layout")
root.geometry("800x400")  

top_frame = tk.Frame(root, borderwidth=1, relief="solid")
top_frame.place(relx=0, rely=0, relwidth=0.75, relheight=0.15)

top_label = tk.Label(top_frame, text="", font=("Helvetica", 14))  
top_label.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(root, borderwidth=1, relief="solid")
left_frame.place(relx=0, rely=0.15, relwidth=0.5, relheight=0.85) 

left_text_area = tk.Text(left_frame, wrap=tk.WORD, font=("Helvetica", 10), height=10, width=50)
left_text_area.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(left_frame, command=left_text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
left_text_area.config(yscrollcommand=scrollbar.set)

center_frame = tk.Frame(root, borderwidth=1, relief="solid")
center_frame.place(relx=0.5, rely=0.15, relwidth=0.25, relheight=0.35)

center_label = tk.Label(center_frame, text="Performance Overview")
center_label.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(center_frame)
button_frame.pack(side=tk.BOTTOM, pady=10)

open_note_button = tk.Button(button_frame, text="Enter Notes", command=open_note_popup)
open_note_button.pack(side=tk.LEFT, padx=5)

test_button = tk.Button(button_frame, text="Test Yourself", command=test_yourself)
test_button.pack(side=tk.LEFT, padx=5)

# Chat functionality
'''chat_frame = tk.Frame(root, borderwidth=1, relief="solid")
chat_frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

chat_display = tk.Text(chat_frame, wrap=tk.WORD, font=("Helvetica", 10))
chat_display.pack(fill=tk.BOTH, expand=True)

chat_entry = tk.Entry(chat_frame, width=50)
chat_entry.pack(pady=10)

send_button = tk.Button(chat_frame, text="Send", command=display_chat_response)
send_button.pack(pady=1)'''

prop_frame = tk.Frame(root, borderwidth=1, relief="solid")
prop_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

prop_label = tk.Label(prop_frame, text="Prop Area")
prop_label.pack(fill=tk.BOTH, expand=True)

update_time_with_day(top_label, root)

root.mainloop()
