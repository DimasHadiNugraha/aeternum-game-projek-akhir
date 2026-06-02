class JournalNode:
    def __init__(self, text, dream_number=None):
        self.text = text                  # Isi catatan
        self.dream_number = dream_number  # Dari mimpi ke-berapa
        self.next = None                  # Pointer ke entry berikutnya


class DreamJournal:
    def __init__(self):
        self.head = None
        self.total_entries = 0

    def add_entry(self, text, dream_number=None):
        """Tambah entry baru di akhir journal."""
        new_node = JournalNode(text, dream_number)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
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
        """Ambil entry paling baru."""
        if not self.head:
            return None
        current = self.head
        while current.next:
            current = current.next
        return current.text

    def count(self):
        """Kembalikan jumlah total entry."""
        return self.total_entries

    def to_list(self):
        """Konversi semua entry ke list Python untuk keperluan save/load."""
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
        """Load journal dari list saat load_game dipanggil."""
        self.head = None
        self.total_entries = 0
        for entry in data:
            self.add_entry(entry["text"], entry.get("dream_number"))


