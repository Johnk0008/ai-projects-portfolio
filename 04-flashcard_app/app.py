import customtkinter as ctk
from flashcards import FlashcardManager
import tkinter as tk
from tkinter import messagebox

class FlashcardApp:
    def __init__(self):
        # Initialize flashcard manager
        self.flashcard_manager = FlashcardManager()
        
        # Set up the main window
        self.root = ctk.CTk()
        self.root.title("Flashcard Quiz App")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize UI
        self.setup_ui()
        
        # Show first card
        self.show_current_card()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Flashcard Quiz App", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Card count display
        self.count_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.count_label.pack(pady=(0, 10))
        
        # Flashcard display frame
        card_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        card_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Question/Answer display
        self.card_text = ctk.CTkTextbox(
            card_frame,
            font=ctk.CTkFont(size=16),
            wrap="word",
            height=200
        )
        self.card_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.card_text.configure(state="disabled")
        
        # Answer visibility control
        self.answer_visible = False
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(control_frame)
        nav_frame.pack(fill="x", pady=5)
        
        self.prev_button = ctk.CTkButton(
            nav_frame,
            text="← Previous",
            command=self.previous_card,
            width=120
        )
        self.prev_button.pack(side="left", padx=(0, 10))
        
        self.show_answer_button = ctk.CTkButton(
            nav_frame,
            text="Show Answer",
            command=self.toggle_answer,
            width=120
        )
        self.show_answer_button.pack(side="left", padx=10)
        
        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Next →",
            command=self.next_card,
            width=120
        )
        self.next_button.pack(side="left", padx=(10, 0))
        
        # Management buttons frame
        manage_frame = ctk.CTkFrame(control_frame)
        manage_frame.pack(fill="x", pady=5)
        
        self.add_button = ctk.CTkButton(
            manage_frame,
            text="Add Flashcard",
            command=self.add_flashcard_dialog,
            width=120
        )
        self.add_button.pack(side="left", padx=(0, 10))
        
        self.edit_button = ctk.CTkButton(
            manage_frame,
            text="Edit Flashcard",
            command=self.edit_flashcard_dialog,
            width=120
        )
        self.edit_button.pack(side="left", padx=10)
        
        self.delete_button = ctk.CTkButton(
            manage_frame,
            text="Delete Flashcard",
            command=self.delete_current_flashcard,
            width=120,
            fg_color="#d13438",
            hover_color="#a4262c"
        )
        self.delete_button.pack(side="left", padx=(10, 0))
        
        # Update card count
        self.update_card_count()
    
    def show_current_card(self):
        """Display the current flashcard"""
        card = self.flashcard_manager.get_current_flashcard()
        self.answer_visible = False
        
        self.card_text.configure(state="normal")
        self.card_text.delete("1.0", "end")
        
        if card:
            self.card_text.insert("1.0", f"Question:\n\n{card['question']}")
            self.show_answer_button.configure(text="Show Answer", state="normal")
            # Enable edit and delete buttons when cards exist
            self.edit_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            self.card_text.insert("1.0", "No flashcards available.\n\nClick 'Add Flashcard' to create your first card!")
            self.show_answer_button.configure(state="disabled")
            # Disable edit and delete buttons when no cards
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
        
        self.card_text.configure(state="disabled")
        self.update_card_count()
    
    def toggle_answer(self):
        """Toggle between showing question and answer"""
        card = self.flashcard_manager.get_current_flashcard()
        if not card:
            return
        
        self.card_text.configure(state="normal")
        self.card_text.delete("1.0", "end")
        
        if not self.answer_visible:
            self.card_text.insert("1.0", f"Answer:\n\n{card['answer']}")
            self.show_answer_button.configure(text="Show Question")
            self.answer_visible = True
        else:
            self.card_text.insert("1.0", f"Question:\n\n{card['question']}")
            self.show_answer_button.configure(text="Show Answer")
            self.answer_visible = False
        
        self.card_text.configure(state="disabled")
    
    def next_card(self):
        """Move to next card"""
        if self.flashcard_manager.get_card_count() > 0:
            self.flashcard_manager.next_card()
            self.show_current_card()
    
    def previous_card(self):
        """Move to previous card"""
        if self.flashcard_manager.get_card_count() > 0:
            self.flashcard_manager.previous_card()
            self.show_current_card()
    
    def update_card_count(self):
        """Update the card count display"""
        total = self.flashcard_manager.get_card_count()
        current = self.flashcard_manager.current_index + 1 if total > 0 else 0
        self.count_label.configure(text=f"Card {current} of {total}")
    
    def add_flashcard_dialog(self):
        """Open dialog to add new flashcard"""
        dialog = AddEditFlashcardDialog(self.root, "Add Flashcard")
        
        # Wait for the dialog to close
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            question, answer = dialog.result
            self.flashcard_manager.add_flashcard(question, answer)
            # Move to the newly added card
            self.flashcard_manager.current_index = self.flashcard_manager.get_card_count() - 1
            self.show_current_card()
            messagebox.showinfo("Success", "Flashcard added successfully!")
    
    def edit_flashcard_dialog(self):
        """Open dialog to edit current flashcard"""
        card = self.flashcard_manager.get_current_flashcard()
        if not card:
            messagebox.showwarning("No Card", "No flashcard to edit!")
            return
        
        dialog = AddEditFlashcardDialog(
            self.root, 
            "Edit Flashcard", 
            card['question'], 
            card['answer']
        )
        
        # Wait for the dialog to close
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            question, answer = dialog.result
            self.flashcard_manager.edit_flashcard(
                self.flashcard_manager.current_index, 
                question, 
                answer
            )
            self.show_current_card()
            messagebox.showinfo("Success", "Flashcard updated successfully!")
    
    def delete_current_flashcard(self):
        """Delete the current flashcard"""
        card = self.flashcard_manager.get_current_flashcard()
        if not card:
            messagebox.showwarning("No Card", "No flashcard to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this flashcard?"):
            self.flashcard_manager.delete_flashcard(self.flashcard_manager.current_index)
            self.show_current_card()
            messagebox.showinfo("Success", "Flashcard deleted successfully!")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

class AddEditFlashcardDialog:
    def __init__(self, parent, title, question="", answer=""):
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x450")  # Increased height to accommodate buttons
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Main frame with proper packing
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Question frame
        question_frame = ctk.CTkFrame(main_frame)
        question_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(question_frame, text="Question:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        self.question_text = ctk.CTkTextbox(question_frame, height=80)
        self.question_text.pack(fill="x", padx=10, pady=(0, 10))
        self.question_text.insert("1.0", question)
        
        # Answer frame
        answer_frame = ctk.CTkFrame(main_frame)
        answer_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(answer_frame, text="Answer:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        self.answer_text = ctk.CTkTextbox(answer_frame, height=80)
        self.answer_text.pack(fill="x", padx=10, pady=(0, 10))
        self.answer_text.insert("1.0", answer)
        
        # Buttons frame - FIXED LAYOUT
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", side="bottom", pady=(10, 0))  # Ensure it stays at bottom
        
        # Use grid layout for better button control
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        
        # Spacer on left
        spacer_left = ctk.CTkLabel(button_frame, text="")
        spacer_left.grid(row=0, column=0, sticky="ew")
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=100,
            fg_color="#d13438",
            hover_color="#a4262c"
        )
        self.cancel_button.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        # Save button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Card",
            command=self.save,
            width=100,
            fg_color="#107c10",
            hover_color="#0e6a0e"
        )
        self.save_button.grid(row=0, column=2, padx=0, pady=5)
        
        # Set focus to question field if empty
        if not question:
            self.question_text.focus()
        else:
            self.answer_text.focus()
            
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        
        # Make sure dialog is fully visible
        self.dialog.after(100, self._ensure_visible)
    
    def _ensure_visible(self):
        """Ensure the dialog is fully visible on screen"""
        self.dialog.lift()
        self.dialog.focus_force()
    
    def save(self, event=None):
        """Save the flashcard"""
        question = self.question_text.get("1.0", "end-1c").strip()
        answer = self.answer_text.get("1.0", "end-1c").strip()
        
        if not question:
            messagebox.showwarning("Input Error", "Question cannot be empty!")
            self.question_text.focus()
            return
        
        if not answer:
            messagebox.showwarning("Input Error", "Answer cannot be empty!")
            self.answer_text.focus()
            return
        
        self.result = (question, answer)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the operation"""
        self.result = None
        self.dialog.destroy()

if __name__ == "__main__":
    app = FlashcardApp()
    app.run()