import json
import os

# Path file savegame (absolute path)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVEGAME_FILE = os.path.join(PROJECT_ROOT, "game_data", "savegame.txt")

#class untuk node di dalam journal, menyimpan teks catatan dan nomor mimpi terkait (jika ada)
class JournalNode:
    def __init__(self, text, dream_number=None):
        self.text = text                  # Isi catatan
        self.dream_number = dream_number  # Dari mimpi ke-berapa
        self.next = None                  # Pointer ke entry berikutnya

#class untuk mengelola seluruh journal, menyimpan catatan dalam linked list dan menyediakan fungsi untuk menambah, menampilkan, dan mengelola catatan
class DreamJournal:
    def __init__(self):
        self.head = None
        self.tail = None        # ← Cache pointer ke entry terakhir
        self.total_entries = 0
    #fungsi untuk menambahkan entry baru kedalam journal
    def add_entry(self, text, dream_number=None):
        new_node = JournalNode(text, dream_number)
        if not self.head:
            self.head = new_node
            self.tail = new_node  # ← Update tail
        else:
            self.tail.next = new_node  # ← Direct append ke tail (O(1))
            self.tail = new_node        # ← Update tail pointer
        self.total_entries += 1

    def display(self): #fungsi untuk menampilkan seluruh isi journal secara urut
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

    def get_last_entry(self): #fungsi untuk mengambil entry paling baru dari journal
        if not self.tail:
            return None
        return self.tail.text

    def count(self): #fungsi untuk menghitung jumlah total entry dalam journal
        return self.total_entries

    def clear(self):#fungsi menghapus isi dari savegame.txt dan mengosongkan journal
        self.head = None
        self.tail = None
        self.total_entries = 0
        
        # Hapus file savegame juga
        if os.path.exists(SAVEGAME_FILE):
            os.remove(SAVEGAME_FILE)
        
        print("  [~] Journal dan savegame berhasil dikosongkan.\n")

    def clear_dream_entries(self, dream_number): # Traverse dan hapus entry dengan dream_number yang sama
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

    def to_list(self): #fungsi untuk mengonversi journal ke dalam bentuk list
        result = []
        current = self.head
        while current:
            result.append({
                "text": current.text,
                "dream_number": current.dream_number
            })
            current = current.next
        return result

    def load_from_list(self, data): #fungsi untuk memuat data journal dari list saat load_game dipanggil
        self.head = None
        self.tail = None
        self.total_entries = 0
        for entry in data:
            self.add_entry(entry["text"], entry.get("dream_number"))          