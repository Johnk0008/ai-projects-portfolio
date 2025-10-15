import customtkinter as ctk
from quotes import QuoteManager
import tkinter as tk
from tkinter import messagebox
import random

class QuoteGeneratorApp:
    def __init__(self):
        # Initialize quote manager
        self.quote_manager = QuoteManager()
        
        # Set up the main window
        self.root = ctk.CTk()
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize UI
        self.setup_ui()
        
        # Show first random quote
        self.show_random_quote()
    
    def setup_ui(self):
        """Set up the user interface with proper layout"""
        # Configure main grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Title section
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="✨ Random Quote Generator ✨",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=5)
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Find inspiration in every click",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 10))
        
        # Main content area
        main_content = ctk.CTkFrame(self.root)
        main_content.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_rowconfigure(1, weight=1)
        
        # Stats label
        self.stats_label = ctk.CTkLabel(
            main_content,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.stats_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        # Quote display frame
        self.quote_frame = ctk.CTkFrame(
            main_content, 
            corner_radius=15,
            fg_color="#2b2b2b",
            border_width=2,
            border_color="#404040"
        )
        self.quote_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.quote_frame.grid_columnconfigure(0, weight=1)
        self.quote_frame.grid_rowconfigure(0, weight=1)
        
        # Quote text
        self.quote_text = ctk.CTkTextbox(
            self.quote_frame,
            font=ctk.CTkFont(size=18, weight="normal"),
            wrap="word",
            fg_color="transparent",
            border_width=0,
            text_color="#ffffff",
            activate_scrollbars=False
        )
        self.quote_text.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.quote_text.configure(state="disabled")
        
        # Author label
        self.author_label = ctk.CTkLabel(
            self.quote_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold", slant="italic"),
            text_color="#e0e0e0"
        )
        self.author_label.grid(row=1, column=0, pady=(0, 20))
        
        # Controls section
        controls_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        controls_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Main button - New Quote
        self.new_quote_button = ctk.CTkButton(
            controls_frame,
            text="🎲 New Quote",
            command=self.show_random_quote,
            width=250,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#4CC9F0",
            hover_color="#4361EE",
            corner_radius=12
        )
        self.new_quote_button.grid(row=0, column=0, pady=15)
        
        # Additional features frame
        features_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        features_frame.grid(row=1, column=0, pady=10, sticky="ew")
        features_frame.grid_columnconfigure(0, weight=1)
        features_frame.grid_columnconfigure(1, weight=1)
        features_frame.grid_columnconfigure(2, weight=1)
        
        # Online quote button
        self.online_quote_button = ctk.CTkButton(
            features_frame,
            text="🌐 Get Online Quote",
            command=self.get_online_quote,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#7209B7",
            hover_color="#560BAD"
        )
        self.online_quote_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Add custom quote button
        self.add_quote_button = ctk.CTkButton(
            features_frame,
            text="✏️ Add Custom Quote",
            command=self.add_custom_quote_dialog,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#F72585",
            hover_color="#B5179E"
        )
        self.add_quote_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Export quotes button
        self.export_button = ctk.CTkButton(
            features_frame,
            text="💾 Export Quotes",
            command=self.export_quotes,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#38b000",
            hover_color="#2d8c00"
        )
        self.export_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Update stats
        self.update_stats()
    
    def show_random_quote(self):
        """Display a random quote"""
        quote = self.quote_manager.get_random_quote()
        self.display_quote(quote)
    
    def display_quote(self, quote: dict):
        """Display the quote in the UI"""
        # Enable text widget for update
        self.quote_text.configure(state="normal")
        self.quote_text.delete("1.0", "end")
        
        # Insert quote text with formatting
        self.quote_text.insert("1.0", f"\"{quote['text']}\"")
        
        # Disable text widget to make it read-only
        self.quote_text.configure(state="disabled")
        
        # Update author label
        self.author_label.configure(text=f"— {quote['author']}")
        
        # Update stats
        self.update_stats()
    
    def get_online_quote(self):
        """Fetch and display a quote from online API"""
        self.online_quote_button.configure(state="disabled", text="🔄 Fetching...")
        self.root.update()
        
        quote = self.quote_manager.fetch_online_quote()
        
        if quote:
            self.display_quote(quote)
            messagebox.showinfo("Success", "Fresh quote fetched from online!")
        else:
            messagebox.showwarning("Offline", "Could not fetch online quote. Showing local quote instead.")
            self.show_random_quote()
        
        self.online_quote_button.configure(state="normal", text="🌐 Get Online Quote")
    
    def add_custom_quote_dialog(self):
        """Open dialog to add custom quote"""
        dialog = AddQuoteDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            text, author = dialog.result
            self.quote_manager.add_custom_quote(text, author)
            self.update_stats()
            messagebox.showinfo("Success", "Custom quote added successfully!")
            # Show the newly added quote
            self.display_quote({"text": text, "author": author})
    
    def export_quotes(self):
        """Export quotes to file"""
        if self.quote_manager.export_quotes():
            messagebox.showinfo("Success", "Quotes exported to 'my_quotes.json'")
        else:
            messagebox.showerror("Error", "Failed to export quotes")
    
    def update_stats(self):
        """Update statistics display"""
        count = self.quote_manager.get_quote_count()
        self.stats_label.configure(text=f"📚 Quote Library: {count} quotes available")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

class AddQuoteDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Custom Quote")
        self.dialog.geometry("550x450")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure grid
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(1, weight=1)
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            self.dialog, 
            text="Add Your Custom Quote",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Main content frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Quote label
        quote_label = ctk.CTkLabel(
            main_frame,
            text="Quote Text:",
            font=ctk.CTkFont(weight="bold")
        )
        quote_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        # Quote text area
        self.quote_text = ctk.CTkTextbox(main_frame, height=150)
        self.quote_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        # Author frame
        author_frame = ctk.CTkFrame(main_frame)
        author_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        author_frame.grid_columnconfigure(1, weight=1)
        
        author_label = ctk.CTkLabel(
            author_frame,
            text="Author:",
            font=ctk.CTkFont(weight="bold")
        )
        author_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        self.author_entry = ctk.CTkEntry(author_frame, height=35)
        self.author_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        # Buttons frame
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=120,
            height=35,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.cancel_button.grid(row=0, column=0, padx=(0, 10), sticky="e")
        
        # Save button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Quote",
            command=self.save,
            width=120,
            height=35,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.save_button.grid(row=0, column=1, sticky="e")
        
        # Set focus
        self.quote_text.focus()
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
    
    def save(self, event=None):
        """Save the custom quote"""
        text = self.quote_text.get("1.0", "end-1c").strip()
        author = self.author_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Input Error", "Quote text cannot be empty!")
            self.quote_text.focus()
            return
        
        if not author:
            author = "Anonymous"
        
        self.result = (text, author)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the operation"""
        self.result = None
        self.dialog.destroy()

if __name__ == "__main__":
    app = QuoteGeneratorApp()
    app.run()