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
        if not self.stack:
            return None
        return self.stack[-1]

    def is_empty(self):
        """Cek apakah stack kosong."""
        return len(self.stack) == 0

    def display(self): 
        if not self.stack:
            print("\n[Tidak ada ingatan tersimpan]\n")
            return

        print("\n" + "=" * 40)
        print("     ✦ MEMORY STACK ✦")
        print("=" * 40)
        for i in range(len(self.stack) - 1, -1, -1):
            is_latest = (i == len(self.stack) - 1)
            label = " <- (terbaru)" if is_latest else ""
            position = len(self.stack) - i
            print(f"  {position}. {self.stack[i]}{label}")
        
        print("=" * 40 + "\n")

    def to_list(self):
        return list(self.stack)

    def load_from_list(self, data): #tambahin validasi ukuran
        self.stack = list(data)
        if len(self.stack) > self.max_size:
            self.stack = self.stack[-self.max_size:]    
        else:
            self.stack = list(data)
