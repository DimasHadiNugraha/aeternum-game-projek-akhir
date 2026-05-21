# =============================================================================
# utils/memory_stack.py
# AETERNUM – Fragments of The Lucid Mind
# Stack LIFO — Sistem Ingatan Jangka Pendek MC
# =============================================================================


class MemoryStack:
    """
    Stack (LIFO) untuk sistem ingatan jangka pendek MC.
    Kapasitas terbatas — ingatan lama otomatis terhapus saat stack penuh.

    Dari GDD:
    "Pemain hanya ingat kejadian paling baru yang membekas.
     Ingatan terakhir masuk yang pertama kali diproses."

    Struktur (terbaru di atas):
    [ Ingatan 3 ] ← paling baru (top)
    [ Ingatan 2 ]
    [ Ingatan 1 ] ← paling lama (bottom)
    """

    def __init__(self, max_size=5):
        self.stack = []
        self.max_size = max_size

    def push(self, memory_text):
        """
        Simpan ingatan baru ke stack.
        Jika sudah penuh, ingatan paling lama otomatis dihapus.
        """
        if len(self.stack) >= self.max_size:
            lost = self.stack.pop(0)  # Hapus ingatan terlama (index 0)
            print(f"  [~] Ingatan lama terhapus: \"{lost}\"")
        self.stack.append(memory_text)

    def pop(self):
        """Ambil dan hapus ingatan paling baru."""
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
            print(f"  {len(self.stack) - i}. {mem}{label}")
        print("=" * 40 + "\n")

    def to_list(self):
        """Konversi stack ke list Python untuk save/load."""
        return list(self.stack)

    def load_from_list(self, data):
        """Load stack dari list saat load_game dipanggil."""
        self.stack = list(data)
