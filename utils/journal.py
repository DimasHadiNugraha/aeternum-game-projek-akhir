import json
import os


# Path file savegame
SAVEGAME_FILE = "game_data/savegame.txt"


class JournalNode:
    def __init__(self, text, dream_number=None):
        self.text = text                  # Isi catatan
        self.dream_number = dream_number  # Dari mimpi ke-berapa
        self.next = None                  # Pointer ke entry berikutnya


class DreamJournal:
    def __init__(self):
        self.head = None
        self.tail = None        # ← Cache pointer ke entry terakhir
        self.total_entries = 0

    def add_entry(self, text, dream_number=None):
        """Tambah entry baru di akhir journal. O(1) performance dengan tail pointer."""
        new_node = JournalNode(text, dream_number)
        if not self.head:
            self.head = new_node
            self.tail = new_node  # ← Update tail
        else:
            self.tail.next = new_node  # ← Direct append ke tail (O(1))
            self.tail = new_node        # ← Update tail pointer
        self.total_entries += 1

    def display(self):
        """Tampilkan seluruh isi journal secara urut."""
        if not self.head:
            print("\n[Journal kosong. Belum ada ingatan yang tercatat.]\n")
            return

        print("\n" + "=" * 40)
        print("       ✦ DREAM JOURNAL ✦")
        print("=" * 40)
        current = self.head
        index = 1
        while current:
            prefix = f"[Mimpi {current.dream_number}] " if current.dream_number else ""
            print(f"  {index}. {prefix}{current.text}")
            current = current.next
            index += 1
        print("=" * 40 + "\n")

    def get_last_entry(self):
        """Ambil entry paling baru. O(1) dengan tail pointer."""
        if not self.tail:
            return None
        return self.tail.text

    def count(self):
        """Kembalikan jumlah total entry."""
        return self.total_entries

    def clear(self):
        """
        Hapus semua entry dari journal.
        Dipanggil saat:
        - Dream over (mimpi dimulai ulang)
        - Reset game (player mau mulai dari awal)
        - New game (permainan baru)
        
        Juga menghapus file savegame.txt
        """
        self.head = None
        self.tail = None
        self.total_entries = 0
        
        # Hapus file savegame juga
        if os.path.exists(SAVEGAME_FILE):
            os.remove(SAVEGAME_FILE)
        
        print("  [~] Journal dan savegame berhasil dikosongkan.\n")

    def save_game(self, player, dream_vault, memory_vault, current_dream, current_node):
        """
        Simpan semua data game ke savegame.txt.
        
        Parameter:
        - player: object player dengan nama, anxiety_level, dll
        - dream_vault: inventory fragment emosi
        - memory_vault: inventory memory fragment dan key
        - current_dream: nomor mimpi sekarang (1, 2, atau 3)
        - current_node: node/dialog ke berapa saat ini
        """
        data = {
            # Data player
            "player": {
                "name": getattr(player, 'name', 'MC'),
                "anxiety_level": getattr(player, 'anxiety_level', 0),
                "fragment_count": getattr(player, 'fragment_count', 0),
            },
            
            # Data vault
            "dream_vault": {
                "total_items": dream_vault.size if hasattr(dream_vault, 'size') else 0,
                "items": dream_vault.to_list() if hasattr(dream_vault, 'to_list') else []
            },
            "memory_vault": {
                "total_items": memory_vault.size if hasattr(memory_vault, 'size') else 0,
                "items": memory_vault.to_list() if hasattr(memory_vault, 'to_list') else []
            },
            
            # Info mimpi/dialog
            "dream_info": {
                "current_dream": current_dream,
                "current_node": current_node
            },
            
            # Journal entries
            "journal_entries": self.to_list()
        }
        
        # Buat folder game_data kalau belum ada
        os.makedirs(os.path.dirname(SAVEGAME_FILE), exist_ok=True)
        
        # Tulis ke file JSON
        with open(SAVEGAME_FILE, "w") as f:
            json.dump(data, f, indent=4)
        
        print("  [✓] Game berhasil disimpan.\n")

    def load_game(self, player, dream_vault, memory_vault):
        """
        Load semua data game dari savegame.txt.
        
        Return: (current_dream, current_node) atau (None, None) kalau tidak ada file
        """
        if not os.path.exists(SAVEGAME_FILE):
            print("  [!] File save tidak ditemukan. Mulai dari awal.\n")
            return None, None
        
        try:
            with open(SAVEGAME_FILE, "r") as f:
                data = json.load(f)
            
            # Restore data player
            if hasattr(player, 'name'):
                player.name = data["player"].get("name", "MC")
            if hasattr(player, 'anxiety_level'):
                player.anxiety_level = data["player"].get("anxiety_level", 0)
            if hasattr(player, 'fragment_count'):
                player.fragment_count = data["player"].get("fragment_count", 0)
            
            # Restore vault items
            if hasattr(dream_vault, 'load_from_list'):
                dream_vault.load_from_list(data["dream_vault"].get("items", []))
            if hasattr(memory_vault, 'load_from_list'):
                memory_vault.load_from_list(data["memory_vault"].get("items", []))
            
            # Restore journal
            self.load_from_list(data.get("journal_entries", []))
            
            # Ambil info mimpi/dialog
            current_dream = data["dream_info"].get("current_dream", 1)
            current_node = data["dream_info"].get("current_node", 0)
            
            print(f"  [✓] Game dimuat. Lanjut dari Mimpi #{current_dream}.\n")
            return current_dream, current_node
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [!] Error membaca file save: {e}\n")
            return None, None

    def clear_dream_entries(self, dream_number):

        # Traverse dan hapus entry dengan dream_number yang sama
        current = self.head
        prev = None
        
        while current:
            if current.dream_number == dream_number:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                
                # Update tail kalau yang dihapus adalah tail
                if current == self.tail:
                    self.tail = prev
                
                self.total_entries -= 1
                current = current.next
            else:
                prev = current
                current = current.next

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append({
                "text": current.text,
                "dream_number": current.dream_number
            })
            current = current.next
        return result

    def load_from_list(self, data):
        self.head = None
        self.tail = None
        self.total_entries = 0
        for entry in data:
<<<<<<< HEAD
            self.add_entry(entry["text"], entry.get("dream_number"))          
=======
            self.add_entry(entry["text"], entry.get("dream_number"))


>>>>>>> c7a75b45af4e8e8c407d863d581b5f59e00e9d28
