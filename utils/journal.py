class JournalNode:
    def __init__(self, text, dream_number=None):
        self.text = text                  # Isi catatan
        self.dream_number = dream_number  # Dari mimpi ke-berapa
        self.next = None                  # Pointer ke entry berikutnya
 
 
class DreamJournal:
    def __init__(self):
        self.head = None  #entry pertama
        self.tail = None        #entry terakhir, untuk akses O(1) saat tambah entry baru 
        self.total_entries = 0
 
    def add_entry(self, text, dream_number=None):
        new_node = JournalNode(text, dream_number) #buat node baru
        if not self.head:  #kalau kosong,node baru jadi head dan tail
            self.head = new_node
            self.tail = new_node
            self.tail.next = new_node  
            self.tail = new_node      
        self.total_entries += 1
 
    def display(self):
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
        if not self.tail:
            return None
        return self.tail.text
 
    def count(self):
        return self.total_entries
 
    def clear(self):
        self.head = None
        self.tail = None
        self.total_entries = 0
        print("  [~] Journal berhasil dikosongkan.\n")
 
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
            self.add_entry(entry["text"], entry.get("dream_number"))
             