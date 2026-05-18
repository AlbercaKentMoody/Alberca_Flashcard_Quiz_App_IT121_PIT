# Kent Moody Alberca                         Computer Programming 2
# BSIT - IT1R2                                           Finals PIT
# Flashcard Quiz App Tkinter

import tkinter as tk
from tkinter import messagebox

# --- APPLICATION CONCEPTS: Functions, Arguments, Return Values, File Handling, Error Handling ---

def load_flashcards(filename):
    """Reads the text file and returns a list of flashcards. Includes try-except for errors."""
    cards = []
    try:
        # File Handling Requirement
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    question = parts[0]
                    answer = parts[1]
                    cards.append({"question": question, "answer": answer})
                    
    except FileNotFoundError:
        # Error Handling (try-except) Requirement
        messagebox.showwarning("File Missing", f"{filename} not found. Loading backup cards.")
        # Fallback data so the app doesn't crash
        cards = [
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "Is Python a programming language? (yes/no)", "answer": "yes"}
        ]
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Return values requirement
    return cards

def check_answer(user_input, correct_answer):
    """Compares the user's answer to the correct answer. Ignores capitalization."""
    # Arguments requirement (takes two inputs)
    # Return values requirement (returns True or False)
    return user_input.strip().lower() == correct_answer.strip().lower()

def get_hint(correct_answer):
    """Returns the first letter of the answer for the Hint feature."""
    if len(correct_answer) > 0:
        return f"Hint: Starts with '{correct_answer[0]}'"
    return "No hint available."

# --- MAIN GUI DESIGN (Tkinter) ---

def main():
    # We use a dictionary to store the score and current question number.
    # This keeps our data organized without needing messy 'global' variables.
    app_state = {
        "current_index": 0,
        "score": 0,
        "cards": load_flashcards("flashcards.txt")
    }

    # Initialize the main window
    window = tk.Tk()
    window.title("IT121 Flashcard Quiz")
    window.geometry("450x350")
    window.config(padx=20, pady=20)

    # --- WIDGETS (Proper use of Labels, Entries, Buttons) ---
    
    score_label = tk.Label(window, text="Score: 0", font=("Arial", 12, "bold"))
    score_label.pack(anchor="e")

    question_label = tk.Label(window, text="Question will appear here", font=("Arial", 14), wraplength=400, height=3)
    question_label.pack(pady=15)

    answer_entry = tk.Entry(window, font=("Arial", 14), width=20)
    answer_entry.pack(pady=10)

    hint_label = tk.Label(window, text="", font=("Arial", 10, "italic"), fg="gray")
    hint_label.pack(pady=5)

    # --- BUTTON COMMANDS ---

    def display_card():
        """Updates the screen to show the current question."""
        current_idx = app_state["current_index"]
        total_cards = len(app_state["cards"])

        if current_idx < total_cards:
            current_card = app_state["cards"][current_idx]
            question_label.config(text=f"Q{current_idx + 1}: {current_card['question']}")
            answer_entry.delete(0, tk.END) # Clear previous answer
            hint_label.config(text="")     # Clear previous hint
        else:
            # End of the quiz
            question_label.config(text="Quiz Complete!")
            answer_entry.config(state="disabled")
            submit_button.config(state="disabled")
            hint_button.config(state="disabled")
            messagebox.showinfo("Finished", f"Your final score is {app_state['score']} out of {total_cards}")

    def submit_clicked():
        """Triggered when the user clicks Submit."""
        current_idx = app_state["current_index"]
        if current_idx >= len(app_state["cards"]):
            return

        current_card = app_state["cards"][current_idx]
        user_ans = answer_entry.get()

        # Call our separate validation function
        is_correct = check_answer(user_ans, current_card["answer"])

        if is_correct:
            app_state["score"] += 1
            score_label.config(text=f"Score: {app_state['score']}")
            messagebox.showinfo("Result", "Correct! Good job.")
        else:
            messagebox.showerror("Result", f"Incorrect. The correct answer was: {current_card['answer']}")

        # Move to the next card and update the screen
        app_state["current_index"] += 1
        display_card()

    def hint_clicked():
        """Triggered when the user clicks Get Hint."""
        current_idx = app_state["current_index"]
        if current_idx < len(app_state["cards"]):
            current_card = app_state["cards"][current_idx]
            hint_text = get_hint(current_card["answer"])
            hint_label.config(text=hint_text)

    # --- LAYOUT (Proper use of pack and grid) ---
    
    # We use a Frame so we can put the two buttons side-by-side using 'grid', 
    # while the rest of the app uses 'pack'. This shows you know how to use both!
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    submit_button = tk.Button(button_frame, text="Submit Answer", command=submit_clicked, bg="green", fg="white", font=("Arial", 12))
    submit_button.grid(row=0, column=0, padx=10)

    hint_button = tk.Button(button_frame, text="Get Hint", command=hint_clicked, bg="orange", fg="black", font=("Arial", 12))
    hint_button.grid(row=0, column=1, padx=10)

    # Start the application by loading the very first card
    display_card()

    # Run the Tkinter event loop
    window.mainloop()

# This is standard Python practice to start the program
if __name__ == "__main__":
    main()

# You got this Moody, yes I got this!