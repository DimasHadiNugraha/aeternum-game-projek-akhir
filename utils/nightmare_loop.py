import random


class DreamNode:
    """Satu lokasi dalam nightmare loop."""
    def __init__(self, location, description=""):
        self.location = location        # Nama lokasi
        self.description = description  # Deskripsi singkat lokasi
        self.is_corrupted = False       # True kalau anxiety >= 20
        self.next = None                # Selalu menunjuk ke node berikutnya


class NightmareLoop:
    """
    Circular Linked List untuk siklus lokasi dalam satu mimpi.
    Setelah lokasi terakhir, otomatis kembali ke awal — loop tidak pernah berhenti.

    Digunakan untuk:
    - Siklus normal lokasi dalam satu dream
    - Fake awakening: MC pikir sudah bangun tapi loop kembali ke awal
    - Anxiety event: node mulai corrupt saat anxiety >= 20

    Struktur:
    [Kamar] -> [Lorong] -> [Kelas] -> [Rumah Sakit] -> (kembali ke Kamar)
    """

    def __init__(self):
        self.head = None
        self.current = None  # Posisi player saat ini
        self.size = 0

    def add_location(self, location, description=""):
        """Tambah lokasi baru ke dalam loop."""
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

    def move_next(self, anxiety_level=0):
        """
        Pindah ke lokasi berikutnya.
        Jika anxiety >= 20, ada kemungkinan 30% node menjadi corrupt.
        """
        if not self.current:
            return None

        self.current = self.current.next

        if anxiety_level >= 20 and not self.current.is_corrupted:
            if random.random() < 0.3:
                self.current.is_corrupted = True

        return self.get_current_location()

    def get_current_location(self):
        """
        Kembalikan info lokasi saat ini.
        Jika corrupt, tampilkan versi glitchy.
        """
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
        Reset posisi ke head (awal loop).
        MC pikir sudah bangun, tapi mimpi dimulai ulang.
        """
        self.current = self.head
        print("\n  ... Matamu terbuka.")
        print("  Kamu pikir ini sudah berakhir.")
        print("  Tapi langit-langitnya... sama persis.\n")
        return self.get_current_location()

    def reset_corruption(self):
        """Reset semua node corrupt saat mimpi selesai."""
        if not self.head:
            return
        temp = self.head
        while True:
            temp.is_corrupted = False
            temp = temp.next
            if temp == self.head:
                break

    def display_loop(self):
        """Tampilkan seluruh isi loop."""
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

    def to_list(self):
        """Konversi loop ke list Python untuk save/load."""
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
        """Load loop dari list saat load_game dipanggil."""
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
