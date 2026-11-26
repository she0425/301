import tkinter as tk
from tkinter import messagebox


class ContactsApp:
    """A minimalist Contacts Management application styled identically to the web/JS version.

    Uses individual contact cards with embedded delete buttons.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Contacts App")

        # Simulate smartphone screen size & background
        self.root.geometry("360x620")
        self.root.configure(bg="#E5E5E5")
        self.root.resizable(False, False)

        # In-memory contact data list (matching JS state structure)
        self.contacts = [
            {"name": "Alice Smith", "phone": "0917-123-4567"},
            {"name": "Bob Johnson", "phone": "0918-987-6543"},
        ]

        self._create_widgets()
        self.render_contacts()

    def _create_widgets(self):
        """Builds the main phone container card and inner form elements."""
        # Phone Frame Container (320px width, rounded background feel)
        self.phone_card = tk.Frame(self.root, bg="#F2F2F7", bd=0, relief="flat")
        self.phone_card.place(x=20, y=20, width=320, height=580)

        # Title
        title = tk.Label(
            self.phone_card,
            text="Contacts",
            font=("Helvetica", 16, "bold"),
            bg="#F2F2F7",
            fg="#000000",
        )
        title.pack(pady=(15, 10))

        # Input Fields
        self.entry_name = tk.Entry(
            self.phone_card,
            font=("Helvetica", 11),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
        )
        self.entry_name.pack(fill="x", padx=15, pady=4, ipady=4)
        self._set_placeholder(self.entry_name, "Name")

        self.entry_phone = tk.Entry(
            self.phone_card,
            font=("Helvetica", 11),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
        )
        self.entry_phone.pack(fill="x", padx=15, pady=4, ipady=4)
        self._set_placeholder(self.entry_phone, "Phone Number")

        # Add Contact Button
        btn_add = tk.Button(
            self.phone_card,
            text="Add Contact",
            font=("Helvetica", 10, "bold"),
            bg="#007AFF",
            fg="white",
            activebackground="#0056B3",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.add_contact,
        )
        btn_add.pack(fill="x", padx=15, pady=(5, 10), ipady=4)

        # Search Input Field
        self.entry_search = tk.Entry(
            self.phone_card,
            font=("Helvetica", 11),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
        )
        self.entry_search.pack(fill="x", padx=15, pady=(0, 10), ipady=4)
        self._set_placeholder(self.entry_search, "Search contacts...")
        self.entry_search.bind("<KeyRelease>", self.search_contacts)

        # Contact List Display Frame (Scrollable Container)
        self.list_container = tk.Frame(self.phone_card, bg="#FFFFFF")
        self.list_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.canvas = tk.Canvas(
            self.list_container, bg="#FFFFFF", highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw", width=288
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _set_placeholder(self, entry, text):
        """Simulates HTML input placeholder behavior."""
        entry.insert(0, text)
        entry.config(fg="#8E8E93")

        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg="#000000")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="#8E8E93")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def render_contacts(self, data=None):
        """Renders individual contact item rows dynamically, matching JS DOM construction."""
        # Clear existing rows
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        items = data if data is not None else self.contacts

        for index, contact in enumerate(items):
            # Row Frame container (simulates JS .contact-item class)
            row = tk.Frame(
                self.scrollable_frame,
                bg="#FFFFFF",
                highlightthickness=1,
                highlightbackground="#EEEEEE",
            )
            row.pack(fill="x", pady=2, ipady=4)

            # Contact Details (Name + Phone)
            text_frame = tk.Frame(row, bg="#FFFFFF")
            text_frame.pack(side="left", fill="both", expand=True, padx=8)

            lbl_name = tk.Label(
                text_frame,
                text=contact["name"],
                font=("Helvetica", 10, "bold"),
                bg="#FFFFFF",
                anchor="w",
            )
            lbl_name.pack(fill="x")

            lbl_phone = tk.Label(
                text_frame,
                text=contact["phone"],
                font=("Helvetica", 8),
                fg="#666666",
                bg="#FFFFFF",
                anchor="w",
            )
            lbl_phone.pack(fill="x")

            # Inline Delete Button per contact item
            btn_del = tk.Button(
                row,
                text="Delete",
                font=("Helvetica", 8, "bold"),
                bg="#FF3B30",
                fg="white",
                activebackground="#D70000",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda idx=index: self.delete_contact(idx),
            )
            btn_del.pack(side="right", padx=8)

    def add_contact(self):
        """Adds a contact to array after verifying input field validity."""
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()

        if name in ("", "Name") or phone in ("", "Phone Number"):
            messagebox.showwarning(
                "Input Error", "Please fill in both Name and Phone fields."
            )
            return

        self.contacts.append({"name": name, "phone": phone})

        # Reset inputs
        self.entry_name.delete(0, tk.END)
        self.entry_name.focus_set()
        self._set_placeholder(self.entry_name, "Name")

        self.entry_phone.delete(0, tk.END)
        self._set_placeholder(self.entry_phone, "Phone Number")

        self.render_contacts()

    def delete_contact(self, index):
        """Deletes contact item by index matching JS array splice logic."""
        del self.contacts[index]
        self.render_contacts()

    def search_contacts(self, event=None):
        """Filters contact list dynamically upon key press."""
        query = self.entry_search.get().lower()
        if query == "search contacts...":
            query = ""

        filtered = [
            c
            for c in self.contacts
            if query in c["name"].lower() or query in c["phone"].lower()
        ]
        self.render_contacts(filtered)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactsApp(root)
    root.mainloop()