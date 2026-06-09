import random


class DreamNode:
    def __init__(self, location, description=""):
        self.location = location        # Nama lokasi
        self.description = description  # Deskripsi singkat lokasi
        self.is_corrupted = False       # True kalau anxiety >= 20
        self.next = None                # Selalu menunjuk ke node berikutnya


class NightmareLoop:

    def __init__(self):
        self.head = None
        self.current = None  # Posisi player saat ini
        self.size = 0

    #fungsi untuk menambahkan lokasi baru ke dalam nightmare loop. Dipanggil saat memulai mimpi baru untuk mengisi loop dengan lokasi-lokasi yang akan dilalui player.
    def add_location(self, location, description=""):
        new_node = DreamNode(location, description)

        if not self.head:
            self.head = new_node
            new_node.next = self.head  # Tunjuk ke diri sendiri
            self.current = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head  # Sambung kembali ke head

        self.size += 1

    #fungsi untuk pindah ke lokasi berikutnya dalam nightmare loop. Dipanggil saat player memilih opsi dialog yang mengarahkan mereka ke lokasi baru.
    def move_next(self, anxiety_level=0):

        if not self.current:
            return None

        self.current = self.current.next

        if anxiety_level >= 20 and not self.current.is_corrupted:
            if random.random() < 0.3:
                self.current.is_corrupted = True

        return self.get_current_location()

    #fungsi untuk melihat lokasi saat ini
    def get_current_location(self):
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

    #fungsi untuk memulai ulang mimpi saat anxiety mencapai 30. Posisi player di-reset ke awal loop, dan journal dikosongkan.
    def trigger_fake_awakening(self):
        """
        Reset posisi ke head (awal loop).
        MC pikir sudah bangun, tapi mimpi dimulai ulang.
        """
        self.current = self.head
        print("\n  ... Matamu terbuka.")
        print("  Kamu pikir ini sudah berakhir.")
        print("  Tapi langit-langitnya... sama persis.\n")
        return self.get_current_location()

    #fungsi untuk meriset saat dream over terjadi (anxiety >= 30). 
    def reset_corruption(self):
        if not self.head:
            return
        temp = self.head
        while True:
            temp.is_corrupted = False
            temp = temp.next
            if temp == self.head:
                break

    #menampilkan seluruh isi loop
    def display_loop(self):
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
            corrupt = " [CORRUPT]" if temp.is_corrupted else ""
            print(f"  {index}. {temp.location}{corrupt}{marker}")
            temp = temp.next
            index += 1
            if temp == self.head:
                break
        print("  ↻ (kembali ke awal)")
        print("=" * 40 + "\n")

    #fungsi untuk mengonversi nightmare loop ke dalam bentuk list
    def to_list(self):
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

    #fungsi untuk memuat data nightmare loop dari list saat load_game dipanggil
    def load_from_list(self, data):
        self.head = None
        self.current = None
        self.size = 0
        for entry in data:
            self.add_location(entry["location"], entry["description"])
        if self.head:
            temp = self.head
            for entry in data:
                temp.is_corrupted = entry.get("is_corrupted", False)
                temp = temp.next
                if temp == self.head:
                    break
