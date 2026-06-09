class VaultNode:
    def __init__(self, item_name, item_type, description="", value=0):
        self.item_name = item_name      # Nama item
        self.item_type = item_type      # Tipe item (lihat referensi di atas)
        self.description = description  # Deskripsi item
        self.value = value              # Nilai fragment
        self.prev = None               # Pointer ke item sebelumnya
        self.next = None               # Pointer ke item berikutnya


#class untuk menyimpan item-item yang dikumpulkan pemain selama permainan. Item ini bisa berupa memory fragment, emotion fragment, atau rewind key yang bisa digunakan untuk mengurangi anxiety.
#Vault ini menggunakan struktur data linked list untuk menyimpan item-item tersebut, dengan pointer ke item pertama (head), terakhir (tail),
#dan item yang sedang di-highlight (current). Vault juga menyediakan fungsi untuk menambah, menghapus, menggunakan item, serta menampilkan seluruh isi vault dengan format yang menarik.
class MemoryVault:
    def __init__(self, name="Vault"):
        self.name = name
        self.head = None
        self.tail = None
        self.current = None  # Item yang sedang di-highlight
        self.size = 0

    #fungsi untuk menambahkan item baru ke vault
    def add_item(self, item_name, item_type, description="", value=0):
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

    #fungsi untuk menghapus item dari vault berdasarkan nama item
    def remove_item(self, item_name):
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
    
    #fungsimengurutkan item di vault 
    def sort_by_value(self):
        #kalau vault kosong atau cuma ada 1 item, tidak perlu diurutkan
        if not self.head or not self.head.next:
            return

        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current.next:
                #jika value node saat ini lebih kecil dari node berikutnya, tukar posisinya
                if current.value < current.next.value:
                    #tukar isi datanya
                    current.item_name, current.next.item_name = current.next.item_name, current.item_name
                    current.item_type, current.next.item_type = current.next.item_type, current.item_type
                    current.description, current.next.description = current.next.description, current.description
                    current.value, current.next.value = current.next.value, current.value
                    
                    swapped = True
                current = current.next
                
        print(f"\n  [~] Fragment di {self.name} telah diurutkan berdasarkan nilainya.")

    #fungsi untuk menggunakan item dari vault
    def use_item(self, item_name, player):
        node = self.find_item(item_name)
        if not node:
            print(f"  [!] Item '{item_name}' tidak ada di {self.name}.")
            return False

        if node.item_type == "rewind_key":
            before = player.anxiety_level
            player.anxiety_level = max(0, player.anxiety_level - 10)
            print(f"\n  ✦ Rewind Key digunakan.")
            print(f"  Anxiety berkurang: {before} -> {player.anxiety_level}")
            self.remove_item(item_name)  #sekali pakai langsung hapus
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

    #fungsi untuk mencari item di vault berdasarkan nama item
    def find_item(self, item_name):
        current = self.head
        while current:
            if current.item_name.lower() == item_name.lower():
                return current
            current = current.next
        return None

    #fungsi untuk menavigasi keitem berikutnya di vault
    def navigate_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current
        print("  [!] Sudah di item terakhir.")
        return self.current

    #fungsi untuk menavigasi ke item sebelumnya di vault
    def navigate_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current
        print("  [!] Sudah di item pertama.")
        return self.current

    #fungsi untuk melihat item yang sedang di-highlight di vault
    def get_selected(self):
        if self.current:
            return {
                "name": self.current.item_name,
                "type": self.current.item_type,
                "description": self.current.description,
                "value": self.current.value
            }
        return None

    #fungsi untuk menghitung total nilai fragment yang ada di vault
    def get_total_value(self):
        total = 0
        current = self.head
        while current:
            total += current.value
            current = current.next
        return total

    #fungsi untuk menampilkan seluruh isi vault
    def display(self):
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

    #fungsi untuk menampilkan seluruh isi vault secara terbalik (dari item terakhir ke pertama)
    def display_reverse(self):
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

    #fungsi untuk mengonversi vault ke dalam bentuk list
    def to_list(self):
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

    #fungsi untuk memuat data vault dari list saat load_game dipanggil
    def load_from_list(self, data):
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
