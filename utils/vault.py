# =============================================================================
# utils/vault.py
# AETERNUM – Fragments of The Lucid Mind
# Double Linked List — Memory Vault & Dream Vault
# =============================================================================

# =============================================================================
# ITEM TYPES:
#
# DREAM VAULT:
#   "emotion_fragment" — potongan emosi dari dialog/event, punya nilai (+5)
#   "rewind_key"       — item sekali pakai, reset anxiety -10
#
# MEMORY VAULT:
#   "memory_fragment"  — potongan ingatan masa lalu MC, punya nilai (+5/+10)
#   "memory_key"       — kunci untuk unlock rahasia di hashing.py
# =============================================================================


class VaultNode:
    """Satu item dalam vault."""
    def __init__(self, item_name, item_type, description="", value=0):
        self.item_name = item_name      # Nama item
        self.item_type = item_type      # Tipe item (lihat referensi di atas)
        self.description = description  # Deskripsi item
        self.value = value              # Nilai fragment
        self.prev = None               # Pointer ke item sebelumnya
        self.next = None               # Pointer ke item berikutnya


class MemoryVault:
    """
    Double Linked List untuk menyimpan item player.
    Mendukung navigasi dua arah — scroll kiri dan kanan di menu inventori.

    Dipakai dua kali:
        dream_vault  = MemoryVault(name="Dream Vault")
        memory_vault = MemoryVault(name="Memory Vault")

    Struktur:
    None <- [Item 1] <-> [Item 2] <-> [Item 3] -> None
    """

    def __init__(self, name="Vault"):
        self.name = name
        self.head = None
        self.tail = None
        self.current = None  # Item yang sedang di-highlight
        self.size = 0

    def add_item(self, item_name, item_type, description="", value=0):
        """Tambah item baru di akhir vault."""
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
        """Hapus item berdasarkan nama."""
        current = self.head
        while current:
            if current.item_name == item_name:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                if self.current == current:
                    self.current = current.next or current.prev

                self.size -= 1
                print(f"  [-] '{item_name}' dihapus dari {self.name}.")
                return True
            current = current.next

        print(f"  [!] '{item_name}' tidak ditemukan di {self.name}.")
        return False

    def use_item(self, item_name, player):
        """
        Pakai item dari vault.
        Rewind key langsung dihapus setelah dipakai (sekali pakai).
        Parameter player harus punya attribute anxiety_level.
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
            self.remove_item(item_name)  # Sekali pakai langsung hapus
            return True

        elif node.item_type == "emotion_fragment":
            print(f"\n  ✦ Emotion Fragment '{item_name}' tersimpan.")
            print(f"  Nilai: +{node.value} pts")
            return True

        elif node.item_type == "memory_fragment":
            print(f"\n  ✦ Memory Fragment '{item_name}' tersimpan.")
            print(f"  Nilai: +{node.value} pts")
            return True

        elif node.item_type == "memory_key":
            print(f"\n  ✦ Memory Key '{item_name}' siap digunakan.")
            print(f"  Gunakan di lokasi yang tepat untuk membuka ingatan terkunci.")
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

    def navigate_next(self):
        """Geser highlight ke item berikutnya."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current
        print("  [!] Sudah di item terakhir.")
        return self.current

    def navigate_prev(self):
        """Geser highlight ke item sebelumnya."""
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

    def get_total_value(self):
        """Hitung total nilai semua fragment dalam vault."""
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
        print(f"     Total Nilai: {self.get_total_value()} pts")
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
        print(f"  ✦ {self.name.upper()} (Mundur) ✦")
        print("=" * 40)
        current = self.tail
        index = self.size
        while current:
            print(f"  {index}. {current.item_name}")
            current = current.prev
            index -= 1
        print("=" * 40 + "\n")

    def to_list(self):
        """Konversi vault ke list Python untuk save/load."""
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
        """Load vault dari list saat load_game dipanggil."""
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
