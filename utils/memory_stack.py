#class untuk menyimpan ingatan pemain dalam bentuk stack. Stack ini akan menyimpan ingatan terbaru di atas dan menghapus ingatan terlama jika kapasitas stack terlampaui. 
#Stack ini juga untuk menampilkan seluruh isi stack dengan format yang menarik.
class MemoryStack:
    def __init__(self, max_size=5):
        self.stack = []
        self.max_size = max_size
    #fungsi untuk menambahkan ingatan baru ke stack. Jika stack sudah penuh, ingatan terlama akan dihapus terlebih dahulu sebelum menambahkan ingatan baru.
    def push(self, memory_text):
        if len(self.stack) >= self.max_size:
            lost = self.stack.pop(0)  # Hapus ingatan terlama (index 0)
            print(f"  [~] Ingatan lama terhapus: \"{lost}\"")
        self.stack.append(memory_text)

    #fungsi untuk memeriksa apakah stack kosong
    def is_empty(self):
        return len(self.stack) == 0
    
    #fungsi untuk menampilkan seluruh isi stack dengan format yang menarik, menampilkan ingatan terbaru di atas dan memberikan label pada ingatan terbaru.
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

    #fungsi untuk mengonversi memory stack ke dalam bentuk list
    def to_list(self): 
        return list(self.stack)
    #fungsi untuk memuat data memory stack dari list saat load_game dipanggil
    def load_from_list(self, data): 
        self.stack = list(data)
        if len(self.stack) > self.max_size:
            self.stack = self.stack[-self.max_size:]    
        else:
            self.stack = list(data)
