# =============================================================================
# utils/structures.py
# AETERNUM – Fragments of The Lucid Mind
# Semua implementasi struktur data manual untuk sistem game
# =============================================================================


# =============================================================================
# SINGLY LINKED LIST — Dream Journal / Riwayat Ingatan
# Cocok untuk journal karena sifatnya linear, dibaca urut, tidak perlu
# navigasi bolak-balik. Setiap event penting tersimpan sebagai entry baru.
# =============================================================================

class JournalNode:
    """Satu entry dalam Dream Journal."""
    def __init__(self, text, dream_number=None):
        self.text = text                  # Isi catatan
        self.dream_number = dream_number  # Dari mimpi ke-berapa
        self.next = None


class DreamJournal:
    """
    Singly Linked List untuk menyimpan riwayat narasi/event dalam game.
    Dipanggil setiap kali: mimpi selesai, fragment ditemukan, event penting.

    Contoh penggunaan:
        journal = DreamJournal()
        journal.add_entry("Aku kembali mendengar suara itu di lorong sekolah.", dream_number=1)
        journal.display()
    """

    def __init__(self):
        self.head = None
        self.total_entries = 0

    def add_entry(self, text, dream_number=None):
        """Tambah entry baru di akhir journal (append)."""
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
        """Ambil entry terakhir (ingatan paling baru)."""
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
        """Konversi semua entry ke Python list (untuk save/load)."""
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
        """Load journal dari list (saat load_game)."""
        self.head = None
        self.total_entries = 0
        for entry in data:
            self.add_entry(entry["text"], entry.get("dream_number"))


# =============================================================================
# CIRCULAR LINKED LIST — Nightmare Loop
# Cocok untuk game ini karena konsep mimpi berulang (nightmare loop) secara
# alami bersifat sirkular. Loop terus berputar, dan semakin tinggi anxiety,
# lokasi bisa "corrupt" — player terjebak di putaran yang makin kacau.
# =============================================================================

class DreamNode:
    """Satu lokasi/ingatan dalam nightmare loop."""
    def __init__(self, location, description=""):
        self.location = location        # Nama lokasi (e.g. "Ruang Kelas")
        self.description = description  # Deskripsi singkat
        self.is_corrupted = False       # Jadi True kalau anxiety >= 20
        self.next = None


class NightmareLoop:
    """
    Circular Linked List untuk siklus lokasi dalam satu mimpi.
    Loop berputar terus — setelah lokasi terakhir, kembali ke awal.

    Digunakan untuk:
    - Siklus normal lokasi dalam satu dream
    - "Fake awakening": MC pikir sudah bangun tapi loop kembali ke Bedroom
    - Anxiety event: node-node mulai corrupt saat anxiety >= 20

    Contoh penggunaan:
        loop = NightmareLoop()
        loop.add_location("Kamar Tidur", "Tempat MC terbangun.")
        loop.add_location("Lorong", "Suara langkah kaki terdengar jauh.")
        loop.add_location("Ruang Kelas", "Kursi-kursi tersusun rapi, tapi tidak ada siapa-siapa.")
    """

    def __init__(self):
        self.head = None
        self.current = None  # Posisi player saat ini di loop
        self.size = 0

    def add_location(self, location, description=""):
        """Tambah lokasi baru ke dalam loop (di akhir, sebelum kembali ke head)."""
        new_node = DreamNode(location, description)

        if not self.head:
            self.head = new_node
            new_node.next = self.head  # Circular: tunjuk ke dirinya sendiri
            self.current = self.head
        else:
            # Cari node terakhir (yang next-nya adalah head)
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head  # Sambung kembali ke head

        self.size += 1

    def move_next(self, anxiety_level=0):
        """
        Pindah ke lokasi berikutnya dalam loop.
        Jika anxiety >= 20, ada kemungkinan node corrupt.
        Kembalikan nama lokasi saat ini.
        """
        if not self.current:
            return None

        self.current = self.current.next

        # Corrupt node jika anxiety terlalu tinggi
        if anxiety_level >= 20 and not self.current.is_corrupted:
            import random
            if random.random() < 0.3:  # 30% chance corrupt
                self.current.is_corrupted = True

        return self.get_current_location()

    def get_current_location(self):
        """Kembalikan info lokasi saat ini. Jika corrupt, tampilkan versi glitchy."""
        if not self.current:
            return None

        if self.current.is_corrupted:
            return {
                "location": "??̴?̷ ̵?̸??",
                "description": "I̷n̵g̶a̷t̸a̶n̵ ̷i̵n̸i̵ ̴t̸e̶l̶a̵h̵ ̸r̸u̴s̸a̷k̵...",
                "corrupted": True
            }

        return {
            "location": self.current.location,
            "description": self.current.description,
            "corrupted": False
        }

    def trigger_fake_awakening(self):
        """
        Fake awakening: reset posisi current ke head (Kamar Tidur).
        MC pikir dia bangun, tapi sebenarnya loop dimulai ulang.
        """
        self.current = self.head
        print("\n  ... Matamu terbuka.")
        print("  Kamu pikir ini sudah berakhir.")
        print("  Tapi langit-langitnya... sama persis.\n")
        return self.get_current_location()

    def reset_corruption(self):
        """Reset semua node corrupt (saat anxiety turun / mimpi selesai)."""
        if not self.head:
            return
        temp = self.head
        while True:
            temp.is_corrupted = False
            temp = temp.next
            if temp == self.head:
                break

    def display_loop(self):
        """Tampilkan seluruh isi loop secara visual."""
        if not self.head:
            print("[Loop kosong]\n")
            return

        print("\n" + "=" * 40)
        print("     ✦ NIGHTMARE LOOP ✦")
        print("=" * 40)

        temp = self.head
        index = 1
        while True:
            marker = " ◄ (kamu di sini)" if temp == self.current else ""
            corrupt_tag = " [CORRUPT]" if temp.is_corrupted else ""
            print(f"  {index}. {temp.location}{corrupt_tag}{marker}")
            temp = temp.next
            index += 1
            if temp == self.head:
                break

        print("  ↻ (kembali ke awal)")
        print("=" * 40 + "\n")

    def to_list(self):
        """Konversi loop ke Python list untuk keperluan save/load."""
        result = []
        if not self.head:
            return result
        temp = self.head
        while True:
            result.append({
                "location": temp.location,
                "description": temp.description,
                "is_corrupted": temp.is_corrupted
            })
            temp = temp.next
            if temp == self.head:
                break
        return result

    def load_from_list(self, data):
        """Load loop dari list (saat load_game)."""
        self.head = None
        self.current = None
        self.size = 0
        for entry in data:
            self.add_location(entry["location"], entry["description"])
        # Restore corruption state
        if self.head:
            temp = self.head
            for entry in data:
                temp.is_corrupted = entry.get("is_corrupted", False)
                temp = temp.next
                if temp == self.head:
                    break


# =============================================================================
# DOUBLE LINKED LIST — Memory Vault & Dream Vault
# Cocok untuk inventori item karena player bisa navigasi maju-mundur.
# Memory vault: item/fragment yang dikumpulkan player.
# Dream vault: tempat menyusun fragment emosi sebelum dikombinasikan.
# =============================================================================

class VaultNode:
    """Satu item dalam vault (Memory atau Dream)."""
    def __init__(self, item_name, item_type, description="", value=0):
        self.item_name = item_name      # Nama item
        self.item_type = item_type      # "emotion_fragment" / "rewind_key" / "memory_fragment" / "memory_key"
        self.description = description  # Deskripsi item
        self.value = value              # Nilai fragment / emosi
        self.prev = None
        self.next = None

# =============================================================================
# ITEM TYPES REFERENCE
#
# DREAM VAULT:
#   "emotion_fragment" — potongan emosi dari dialog/event, punya nilai (+5)
#   "rewind_key"       — item sekali pakai, reset anxiety dari pilihan salah
#
# MEMORY VAULT:
#   "memory_fragment"  — potongan ingatan masa lalu MC, punya nilai (+5/+10)
#   "memory_key"       — kunci untuk unlock rahasia di hashing.py
# ============================================================================= 


class MemoryVault:
    """
    Double Linked List untuk menyimpan item yang dikumpulkan player.
    Mendukung navigasi dua arah (scroll kiri-kanan di menu inventori).

    Digunakan untuk:
    - Memory Vault: fragment dan item yang ditemukan
    - Dream Vault: fragment emosi yang menunggu untuk digabungkan

    Contoh penggunaan:
        vault = MemoryVault(name="Memory Vault")
        vault.add_item("Fragment Kesedihan", "emotion", "Rasa kehilangan dari masa kecil.", value=5)
        vault.display()
    """

    def __init__(self, name="Vault"):
        self.name = name
        self.head = None
        self.tail = None
        self.current = None  # Item yang sedang di-highlight/dipilih
        self.size = 0

    def add_item(self, item_name, item_type, description="", value=0):
        """Tambah item baru di akhir vault (append to tail)."""
        new_node = VaultNode(item_name, item_type, description, value)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        print(f"  [+] '{item_name}' ditambahkan ke {self.name}.")

    def remove_item(self, item_name):
        """Hapus item berdasarkan nama dari vault."""
        current = self.head
        while current:
            if current.item_name == item_name:
                # Sambung ulang pointer tetangga
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # Node pertama dihapus

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev  # Node terakhir dihapus

                # Reset current jika node yang dihapus adalah yang aktif
                if self.current == current:
                    self.current = current.next or current.prev

                self.size -= 1
                print(f"  [-] '{item_name}' dihapus dari {self.name}.")
                return True

            current = current.next

        print(f"  [!] Item '{item_name}' tidak ditemukan di {self.name}.")
        return False

    def navigate_next(self):
        """Geser highlight ke item berikutnya (tombol kanan di inventori)."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current
        print("  [!] Sudah di item terakhir.")
        return self.current

    def navigate_prev(self):
        """Geser highlight ke item sebelumnya (tombol kiri di inventori)."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current
        print("  [!] Sudah di item pertama.")
        return self.current

    def get_selected(self):
        """Kembalikan item yang sedang dipilih."""
        if self.current:
            return {
                "name": self.current.item_name,
                "type": self.current.item_type,
                "description": self.current.description,
                "value": self.current.value
            }
        return None

    def use_item(self, item_name, player):
        """
        Pakai item dari vault. Khusus rewind_key: langsung dihapus setelah dipakai.
        Parameter player harus punya attribute anxiety_level.

        Contoh:
            vault.use_item("Rewind Key", player)
        """
        node = self.find_item(item_name)
        if not node:
            print(f"  [!] Item '{item_name}' tidak ada di {self.name}.")
            return False

        if node.item_type == "rewind_key":
            before = player.anxiety_level
            player.anxiety_level = max(0, player.anxiety_level - 10)
            print(f"\n  ✦ Rewind Key digunakan.")
            print(f"  Anxiety berkurang: {before} -> {player.anxiety_level}")
            self.remove_item(item_name)  # Sekali pakai, langsung hapus
            return True

        elif node.item_type == "emotion_fragment":
            print(f"\n  ✦ Emotion Fragment '{item_name}' tersimpan. Nilai: +{node.value} pts")
            return True

        elif node.item_type == "memory_fragment":
            print(f"\n  ✦ Memory Fragment '{item_name}' tersimpan. Nilai: +{node.value} pts")
            return True

        elif node.item_type == "memory_key":
            print(f"\n  ✦ Memory Key '{item_name}' siap digunakan untuk membuka ingatan terkunci.")
            return True

        else:
            print(f"  [!] Tipe item '{node.item_type}' tidak dikenali.")
            return False

    def find_item(self, item_name):
        """Cari item berdasarkan nama. Kembalikan node jika ketemu."""
        current = self.head
        while current:
            if current.item_name.lower() == item_name.lower():
                return current
            current = current.next
        return None

    def get_total_value(self):
        """Hitung total nilai semua fragment dalam vault (untuk scoring)."""
        total = 0
        current = self.head
        while current:
            total += current.value
            current = current.next
        return total

    def display(self):
        """Tampilkan seluruh isi vault dengan highlight pada item aktif."""
        if not self.head:
            print(f"\n[{self.name} kosong]\n")
            return

        print("\n" + "=" * 40)
        print(f"     ✦ {self.name.upper()} ✦")
        print(f"     Total Fragment: {self.get_total_value()} pts")
        print("=" * 40)

        current = self.head
        index = 1
        while current:
            selected = " ◄" if current == self.current else ""
            print(f"  {index}. [{current.item_type}] {current.item_name} (+{current.value}){selected}")
            if current == self.current:
                print(f"      └─ {current.description}")
            current = current.next
            index += 1

        print("=" * 40 + "\n")

    def display_reverse(self):
        """Tampilkan vault dari tail ke head (traversal mundur)."""
        if not self.tail:
            print(f"\n[{self.name} kosong]\n")
            return

        print("\n" + "=" * 40)
        print(f"  ✦ {self.name.upper()} (Terbalik) ✦")
        print("=" * 40)

        current = self.tail
        index = self.size
        while current:
            print(f"  {index}. {current.item_name}")
            current = current.prev
            index -= 1

        print("=" * 40 + "\n")

    def to_list(self):
        """Konversi vault ke Python list untuk save/load."""
        result = []
        current = self.head
        while current:
            result.append({
                "item_name": current.item_name,
                "item_type": current.item_type,
                "description": current.description,
                "value": current.value
            })
            current = current.next
        return result

    def load_from_list(self, data):
        """Load vault dari list (saat load_game)."""
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0
        for entry in data:
            self.add_item(
                entry["item_name"],
                entry["item_type"],
                entry.get("description", ""),
                entry.get("value", 0)
            )


# =============================================================================
# STACK — Memory Stack (Sistem Ingatan LIFO)
# Dari GDD: "Pemain hanya ingat kejadian paling baru yang membekas."
# Ingatan terakhir masuk = pertama diproses. Kalau penuh, ingatan lama hilang.
# =============================================================================

class MemoryStack:
    """
    Stack (LIFO) untuk sistem ingatan jangka pendek MC.
    Kapasitas terbatas — ingatan lama otomatis terhapus saat stack penuh.

    Contoh penggunaan:
        memory = MemoryStack(max_size=5)
        memory.push("Kamu melihat foto keluarga di laci meja.")
        memory.push("Lumiere menatapmu dengan ekspresi aneh.")
        memory.peek()  # Ingatan paling baru
    """

    def __init__(self, max_size=5):
        self.stack = []
        self.max_size = max_size

    def push(self, memory_text):
        """Simpan ingatan baru. Jika penuh, ingatan terlama otomatis hilang."""
        if len(self.stack) >= self.max_size:
            lost = self.stack.pop(0)  # Hapus ingatan paling lama
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
            label = " ← (terbaru)" if i == 0 else ""
            print(f"  {len(self.stack) - i}. {mem}{label}")
        print("=" * 40 + "\n")

    def to_list(self):
        return list(self.stack)

    def load_from_list(self, data):
        self.stack = list(data)


# =============================================================================
# QUICK TEST — Jalankan file ini langsung untuk cek semua struktur
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   AETERNUM — Structures Test")
    print("=" * 50)

    # --- Test Dream Journal (Singly Linked List) ---
    print("\n[TEST: Dream Journal]")
    journal = DreamJournal()
    journal.add_entry("Aku kembali mendengar suara itu di lorong sekolah.", dream_number=1)
    journal.add_entry("Lumiere terlihat gugup hari ini.", dream_number=1)
    journal.add_entry("Ruang kelas itu terasa familiar, tapi berbeda.", dream_number=2)
    journal.display()

    # --- Test Nightmare Loop (Circular Linked List) ---
    print("[TEST: Nightmare Loop]")
    loop = NightmareLoop()
    loop.add_location("Kamar Tidur", "Tempat MC selalu terbangun.")
    loop.add_location("Lorong Gelap", "Suara langkah kaki terdengar jauh.")
    loop.add_location("Ruang Kelas", "Kursi-kursi tersusun rapi, tidak ada siapa-siapa.")
    loop.add_location("Rumah Sakit", "Bau antiseptik yang menyesakkan.")
    loop.display_loop()

    # Simulasi pergerakan dengan anxiety tinggi
    print("[Simulasi pergerakan, anxiety = 25]")
    for _ in range(5):
        loc = loop.move_next(anxiety_level=25)
        status = "[CORRUPT]" if loc["corrupted"] else ""
        print(f"  → {loc['location']} {status}")

    # Fake awakening
    print()
    loop.trigger_fake_awakening()

    # --- Test Memory Vault (Double Linked List) ---
    print("[TEST: Memory Vault]")
    memory_vault = MemoryVault(name="Memory Vault")
    memory_vault.add_item("Fragment Ingatan Sekolah", "memory_fragment", "Ingatan samar tentang koridor sekolah.", value=5)
    memory_vault.add_item("Fragment Ingatan Rumah", "memory_fragment", "Suara pintu yang berderit.", value=5)
    memory_vault.add_item("Memory Key #1", "memory_key", "Membuka ingatan terkunci di perpustakaan.", value=0)
    memory_vault.display()

    print("[TEST: Dream Vault]")
    dream_vault = MemoryVault(name="Dream Vault")
    dream_vault.add_item("Fragment Kesedihan", "emotion_fragment", "Rasa kehilangan dari masa kecil.", value=5)
    dream_vault.add_item("Fragment Ketakutan", "emotion_fragment", "Bayangan yang selalu mengejar.", value=5)
    dream_vault.add_item("Rewind Key", "rewind_key", "Sekali pakai. Reset anxiety -10.", value=0)
    dream_vault.display()

    # Simulasi pakai Rewind Key
    print("[TEST: use_item - Rewind Key]")
    class DummyPlayer:
        anxiety_level = 18
    player = DummyPlayer()
    print(f"  Anxiety sebelum: {player.anxiety_level}")
    dream_vault.use_item("Rewind Key", player)
    dream_vault.display()  # Rewind Key seharusnya sudah hilang

    # Navigasi vault
    print("[TEST: Navigasi Memory Vault]")
    memory_vault.navigate_next()
    memory_vault.display()


    # --- Test Memory Stack ---
    print("[TEST: Memory Stack (kapasitas 3)]")
    memory = MemoryStack(max_size=3)
    memory.push("Kamu melihat foto keluarga di laci meja.")
    memory.push("Lumiere menatapmu dengan ekspresi aneh.")
    memory.push("Ada suara isak tangis dari balik pintu.")
    memory.push("Ruangan itu mulai berputar.")  # Ini akan menghapus ingatan tertua
    memory.display()

"""
revisi:
-ada isi class yang duplicated sama journal.py, memory_stack.py dan nightmare_loop.py
-import library diletakkin dipaling atas sebelum class.
"""