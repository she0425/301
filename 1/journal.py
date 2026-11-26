import json
import os
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict

DATA_FILE = "journal.json"
VALID_MOODS = ["HAPPY", "NEUTRAL", "SAD", "ANXIOUS", "WORK"]

# --- ANSI COLOR CODES (PYTHON BLUE & YELLOW THEME) ---
CLR_BLUE = "\033[38;5;39m"
CLR_YELLOW = "\033[38;5;220m"
CLR_GREEN = "\033[38;5;82m"
CLR_RED = "\033[38;5;196m"
CLR_CYAN = "\033[38;5;51m"
CLR_GRAY = "\033[38;5;242m"
CLR_RESET = "\033[0m"
BOLD = "\033[1m"

BANNER = f"""{CLR_BLUE}{BOLD}
  ____        _   _                   _ ____  
 |  _ \\ _   _| |_| |__   ___  _ __   | / ___| 
 | |_) | | | | __| '_ \\ / _ \\| '_ \\  | \\___ \\ 
 |  __/| |_| | |_| | | | (_) | | | | | |___) |
 |_|    \\__, |\\__|_| |_|\\___/|_| |_| |_|____/ 
        |___/  {CLR_YELLOW}🐍 Python Journal App v2.0{CLR_RESET}
"""

@dataclass
class JournalEntry:
    id: str
    title: str
    content: str
    mood: str
    created_at: str
    updated_at: str

    @staticmethod
    def create_new(title: str, content: str, mood: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return JournalEntry(
            id=str(uuid.uuid4())[:8],
            title=title,
            content=content,
            mood=mood.upper() if mood.upper() in VALID_MOODS else "NEUTRAL",
            created_at=now,
            updated_at=now
        )

class JournalManager:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [JournalEntry(**entry) for entry in data]
        except Exception:
            return []

    def save_entries(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in self.entries], f, indent=2)

    def create_entry(self, title: str, content: str, mood: str):
        entry = JournalEntry.create_new(title, content, mood)
        self.entries.append(entry)
        self.save_entries()
        print(f"\n{CLR_GREEN}✔ Entry successfully created! ID: [{entry.id}]{CLR_RESET}")

    def list_entries(self):
        if not self.entries:
            print(f"\n{CLR_RED}✖ No journal entries found.{CLR_RESET}")
            return
        
        print(f"\n{CLR_YELLOW}┌───────┬──────────────────────────────┬──────────┬────────────────┐{CLR_RESET}")
        print(f"{CLR_YELLOW}│ ID    │ TITLE                        │ MOOD     │ CREATED AT     │{CLR_RESET}")
        print(f"{CLR_YELLOW}├───────┼──────────────────────────────┼──────────┼────────────────┤{CLR_RESET}")
        for e in self.entries:
            t_short = (e.title[:27] + "...") if len(e.title) > 30 else e.title.ljust(30)
            m_short = e.mood.ljust(8)
            print(f"│ {CLR_CYAN}{e.id:<5}{CLR_RESET} │ {t_short} │ {CLR_GREEN}{m_short}{CLR_RESET} │ {CLR_GRAY}{e.created_at}{CLR_RESET} │")
        print(f"{CLR_YELLOW}└───────┴──────────────────────────────┴──────────┴────────────────┘{CLR_RESET}")

    def get_entry_by_id(self, entry_id: str):
        for e in self.entries:
            if e.id == entry_id:
                return e
        return None

    def view_entry(self, entry_id: str):
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            print(f"\n{CLR_RED}✖ Entry with ID [{entry_id}] not found.{CLR_RESET}")
            return
        print(f"\n{CLR_BLUE}╔═══════════════════════════════════════════════════════════════════╗{CLR_RESET}")
        print(f"{CLR_BLUE}║ {BOLD}{entry.title:<55}{CLR_RESET} {CLR_BLUE}[{entry.id}] ║{CLR_RESET}")
        print(f"{CLR_BLUE}╠═══════════════════════════════════════════════════════════════════╣{CLR_RESET}")
        print(f" {CLR_YELLOW}Mood:{CLR_RESET} {entry.mood} | {CLR_GRAY}Created: {entry.created_at} | Updated: {entry.updated_at}{CLR_RESET}")
        print(f"{CLR_BLUE}───────────── Content ──────────────────────────────────────────────{CLR_RESET}")
        print(f" {entry.content}")
        print(f"{CLR_BLUE}╚═══════════════════════════════════════════════════════════════════╝{CLR_RESET}")

    def update_entry(self, entry_id: str, new_title: str, new_content: str, new_mood: str):
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            print(f"\n{CLR_RED}✖ Entry with ID [{entry_id}] not found.{CLR_RESET}")
            return
        if new_title.strip(): entry.title = new_title
        if new_content.strip(): entry.content = new_content
        if new_mood.strip() and new_mood.upper() in VALID_MOODS: entry.mood = new_mood.upper()
        entry.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.save_entries()
        print(f"\n{CLR_GREEN}✔ Entry [{entry_id}] updated successfully!{CLR_RESET}")

    def delete_entry(self, entry_id: str):
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            print(f"\n{CLR_RED}✖ Entry with ID [{entry_id}] not found.{CLR_RESET}")
            return
        self.entries = [e for e in self.entries if e.id != entry_id]
        self.save_entries()
        print(f"\n{CLR_RED}✔ Entry [{entry_id}] deleted successfully.{CLR_RESET}")

    def search_entries(self, query: str):
        q = query.lower()
        results = [e for e in self.entries if q in e.title.lower() or q in e.content.lower() or q == e.mood.lower()]
        if not results:
            print(f"\n{CLR_RED}✖ No entries matching '{query}' found.{CLR_RESET}")
            return
        print(f"\n{CLR_YELLOW}🔍 Search Results for '{query}' ({len(results)} found):{CLR_RESET}")
        for e in results:
            print(f" • [{CLR_CYAN}{e.id}{CLR_RESET}] {BOLD}{e.title}{CLR_RESET} ({CLR_GREEN}{e.mood}{CLR_RESET})")

def main():
    manager = JournalManager()
    print(BANNER)
    while True:
        print(f"\n{CLR_BLUE}────────────── MENU ──────────────{CLR_RESET}")
        print(f" {CLR_YELLOW}1.{CLR_RESET} Add New Entry")
        print(f" {CLR_YELLOW}2.{CLR_RESET} List All Entries")
        print(f" {CLR_YELLOW}3.{CLR_RESET} View Entry Details")
        print(f" {CLR_YELLOW}4.{CLR_RESET} Edit Entry")
        print(f" {CLR_YELLOW}5.{CLR_RESET} Delete Entry")
        print(f" {CLR_YELLOW}6.{CLR_RESET} Search Entries")
        print(f" {CLR_YELLOW}7.{CLR_RESET} Exit")
        choice = input(f"{CLR_CYAN}Select an option (1-7): {CLR_RESET}").strip()

        if choice == "1":
            t = input("Title: ")
            c = input("Content: ")
            m = input(f"Mood ({'/'.join(VALID_MOODS)}): ")
            manager.create_entry(t, c, m)
        elif choice == "2":
            manager.list_entries()
        elif choice == "3":
            manager.view_entry(input("Enter Entry ID: "))
        elif choice == "4":
            e_id = input("Enter Entry ID to update: ")
            print(f"{CLR_GRAY}(Press Enter to leave field unchanged){CLR_RESET}")
            manager.update_entry(e_id, input("New Title: "), input("New Content: "), input("New Mood: "))
        elif choice == "5":
            manager.delete_entry(input("Enter Entry ID to delete: "))
        elif choice == "6":
            manager.search_entries(input("Search keyword/mood: "))
        elif choice == "7":
            print(f"\n{CLR_YELLOW}Goodbye! 🐍{CLR_RESET}")
            break

if __name__ == "__main__":
    main()
