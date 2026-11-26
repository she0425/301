import json
import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Local JSON file path for data persistence
STORAGE_FILE = "journal_entries.json"

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Journal")
        self.root.geometry("850x550")
        self.root.configure(bg="#f4f5f7")

        self.entries = []
        self.active_entry_id = None
        self.auto_save_job = None

        self._setup_styles()
        self._create_layout()
        self.load_entries()

    def _setup_styles(self):
        """Configure clean, modern UI styles."""
        self.style = ttk.Style()
        self.style.theme_use("clamp")

        # Color palette definition
        self.bg_color = "#f4f5f7"
        self.card_bg = "#ffffff"
        self.border_color = "#e2e8f0"
        self.text_muted = "#718096"
        self.primary = "#2b6cb0"
        self.danger = "#e53e3e"

        # Frame styles
        self.style.configure("Sidebar.TFrame", background="#fafafa")
        self.style.configure("Main.TFrame", background=self.card_bg)

        # Button styles
        self.style.configure(
            "Primary.TButton",
            background=self.primary,
            foreground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
            padding=6,
        )
        self.style.map("Primary.TButton", background=[("active", "#2c5282")])

        self.style.configure(
            "Danger.TButton",
            background=self.card_bg,
            foreground=self.danger,
            font=("Segoe UI", 9),
            borderwidth=1,
            relief="solid",
            padding=5,
        )
        self.style.map("Danger.TButton", background=[("active", self.danger)], foreground=[("active", "#ffffff")])

    def _create_layout(self):
        """Builds the main container and split panels."""
        # Parent Container
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Sidebar Panel (Left)
        sidebar = ttk.Frame(container, style="Sidebar.TFrame", width=260)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        title_lbl = tk.Label(sidebar, text="My Journal", font=("Segoe UI", 14, "bold"), bg="#fafafa", fg="#1a202c")
        title_lbl.pack(anchor="w", padx=12, pady=(12, 6))

        # Search Field
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_list())
        search_entry = tk.Entry(sidebar, textvariable=self.search_var, font=("Segoe UI", 9), relief="solid", bd=1)
        search_entry.pack(fill="x", padx=12, pady=4)

        # Create Button
        new_btn = ttk.Button(sidebar, text="+ New Entry", style="Primary.TButton", command=self.create_entry)
        new_btn.pack(fill="x", padx=12, pady=(6, 12))

        # Entry Listbox
        self.entry_listbox = tk.Listbox(
            sidebar,
            font=("Segoe UI", 9),
            bd=0,
            highlightthickness=0,
            bg="#fafafa",
            selectbackground="#ebf8ff",
            selectforeground="#1a202c",
            activestyle="none",
        )
        self.entry_listbox.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.entry_listbox.bind("<<ListboxSelect>>", self.on_select_entry)

        # Main Panel (Right)
        self.main_frame = ttk.Frame(container, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Default Placeholder View
        self.placeholder_label = tk.Label(
            self.main_frame,
            text="Select or create an entry to start writing.",
            font=("Segoe UI", 10),
            fg=self.text_muted,
            bg=self.card_bg,
        )
        self.placeholder_label.pack(expand=True)

        # Editor View
        self.editor_frame = tk.Frame(self.main_frame, bg=self.card_bg)

        self.date_label = tk.Label(self.editor_frame, text="", font=("Segoe UI", 8), fg=self.text_muted, bg=self.card_bg)
        self.date_label.pack(anchor="w", pady=(0, 4))

        self.title_entry = tk.Entry(self.editor_frame, font=("Segoe UI", 16, "bold"), bd=0, bg=self.card_bg, relief="flat")
        self.title_entry.pack(fill="x", pady=(0, 8))
        self.title_entry.bind("<KeyRelease>", self.schedule_auto_save)

        ttk.Separator(self.editor_frame, orient="horizontal").pack(fill="x", pady=(0, 8))

        self.body_text = tk.Text(
            self.editor_frame,
            font=("Segoe UI", 10),
            bd=0,
            bg=self.card_bg,
            wrap="word",
            undo=True,
            highlightthickness=0,
        )
        self.body_text.pack(fill="both", expand=True, pady=(0, 8))
        self.body_text.bind("<KeyRelease>", self.schedule_auto_save)

        # Bottom Toolbar
        toolbar = tk.Frame(self.editor_frame, bg=self.card_bg)
        toolbar.pack(fill="x", side="bottom", pady=(8, 0))

        self.save_status = tk.Label(toolbar, text="", font=("Segoe UI", 8), fg=self.text_muted, bg=self.card_bg)
        self.save_status.pack(side="left")

        delete_btn = ttk.Button(toolbar, text="Delete Entry", style="Danger.TButton", command=self.delete_entry)
        delete_btn.pack(side="right")

    # Storage & Helper Methods
    def format_date(self, timestamp):
        dt = datetime.fromtimestamp(timestamp / 1000.0)
        return dt.strftime("%b %d, %Y, %I:%M %p")

    def load_entries(self):
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, "r") as f:
                    self.entries = json.load(f)
            except Exception:
                self.entries = []
        else:
            self.entries = []

        self.entries.sort(key=lambda x: x.get("updatedAt", 0), reverse=True)
        self.render_list()

    def save_entries_to_file(self):
        try:
            with open(STORAGE_FILE, "w") as f:
                json.dump(self.entries, f, indent=2)
        except Exception:
            self.save_status.config(text="Error saving!")

    # UI Rendering
    def render_list(self):
        query = self.search_var.get().strip().lower()
        self.filtered_entries = [
            e for e in self.entries
            if query in e.get("title", "").lower() or query in e.get("body", "").lower()
        ]

        self.entry_listbox.delete(0, tk.END)

        for entry in self.filtered_entries:
            title = entry.get("title") or "Untitled"
            self.entry_listbox.insert(tk.END, f"  {title}")

    def on_select_entry(self, event):
        selection = self.entry_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        selected_entry = self.filtered_entries[index]
        self.open_entry(selected_entry["id"])

    def open_entry(self, entry_id):
        self.active_entry_id = entry_id
        entry = next((e for e in self.entries if e["id"] == entry_id), None)
        if not entry:
            return

        self.placeholder_label.pack_forget()
        self.editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.date_label.config(text=f"Last updated: {self.format_date(entry.get('updatedAt', 0))}")
        
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, entry.get("title", ""))

        self.body_text.delete("1.0", tk.END)
        self.body_text.insert("1.0", entry.get("body", ""))

        self.save_status.config(text="")

    # CRUD Operations
    def create_entry(self):
        now = int(time.time() * 1000)
        new_entry = {"id": str(now), "title": "", "body": "", "updatedAt": now}
        self.entries.insert(0, new_entry)
        self.save_entries_to_file()
        self.render_list()
        self.open_entry(new_entry["id"])
        self.title_entry.focus()

    def schedule_auto_save(self, event=None):
        self.save_status.config(text="Saving...")
        if self.auto_save_job:
            self.root.after_cancel(self.auto_save_job)
        self.auto_save_job = self.root.after(400, self.perform_save)

    def perform_save(self):
        entry = next((e for e in self.entries if e["id"] == self.active_entry_id), None)
        if not entry:
            return

        entry["title"] = self.title_entry.get().strip()
        entry["body"] = self.body_text.get("1.0", tk.END).strip()
        entry["updatedAt"] = int(time.time() * 1000)

        self.entries.sort(key=lambda x: x.get("updatedAt", 0), reverse=True)
        self.save_entries_to_file()

        self.date_label.config(text=f"Last updated: {self.format_date(entry['updatedAt'])}")
        self.save_status.config(text="Saved")
        self.render_list()

    def delete_entry(self):
        if not self.active_entry_id:
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            self.entries = [e for e in self.entries if e["id"] != self.active_entry_id]
            self.active_entry_id = None
            self.save_entries_to_file()

            self.editor_frame.pack_forget()
            self.placeholder_label.pack(expand=True)
            self.render_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()