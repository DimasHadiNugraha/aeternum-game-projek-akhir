class MemoryStack:
    def __init__(self, max_size=5):
        self.stack = []
        self.max_size = max_size

    def push(self, memory_text):
        if len(self.stack) >= self.max_size:
            lost = self.stack.pop(0)  # Hapus ingatan terlama (index 0)
            print(f"  [~] Ingatan lama terhapus: \"{lost}\"")
        self.stack.append(memory_text)

    def pop(self):
        if not self.stack:
            print("  [!] Tidak ada ingatan tersisa.")
            return None
        return self.stack.pop()

    def peek(self):
        """Lihat ingatan paling baru tanpa menghapusnya."""
        if not self.stack:
            return None
        return self.stack[-1]

    def is_empty(self):
        """Cek apakah stack kosong."""
        return len(self.stack) == 0

    def display(self): 
        """Tampilkan semua ingatan dari yang terbaru ke terlama."""
        if not self.stack:
            print("\n[Tidak ada ingatan tersimpan]\n")
            return

        print("\n" + "=" * 40)
        print("     ✦ MEMORY STACK ✦")
        print("=" * 40)
        for i, mem in enumerate(reversed(self.stack)):
            label = " <- (terbaru)" if i == 0 else ""
            print(f"  {len(self.stack) - i}. {mem}{label}") #ini revisi
        print("=" * 40 + "\n")

    def to_list(self):
        """Konversi stack ke list Python untuk save/load."""
        return list(self.stack)

    def load_from_list(self, data): #tambahin validasi ukuran
        """Load stack dari list saat load_game dipanggil."""
        self.stack = list(data)

"""
catatan:
tambahin komentar pakai bahasa sendiri 
"""
