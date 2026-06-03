# system/dream.py
from system.map import load_world

class MesinMimpi:
    def __init__(self, lokasi_awal="Ruang Kelas", lokasi_target="Rumah Sakit"):
        self.peta = load_world()
        self.lokasi_sekarang = lokasi_awal
        self.lokasi_target = lokasi_target  # Tambahkan target pencarian
        self.level_mimpi = 0
        self.game_selesai = False
        
        # Hitung rute kunci yang benar menggunakan DFS bawaan PetaGame
        self.rute_seharusnya = self.peta.cari_jalan(lokasi_awal, lokasi_target)

    def ambil_jalur(self, lokasi):
        return self.peta.tempat.get(lokasi, [])

    def mulai_mimpi(self):
        lokasi_pilihan = self.ambil_jalur(self.lokasi_sekarang)

        if not lokasi_pilihan:
            print("\n[!] Jalur buntu atau lokasi rusak!")
            return

        print("\n" + "=" * 30)
        print(f" LAPISAN MIMPI KE-{self.level_mimpi + 1} / 5")
        print("=" * 30)
        print(f"Pikiranmu tertuju mencari: ✦ {self.lokasi_target} ✦")
        print(f"Posisi kesadaran saat ini: {self.lokasi_sekarang}")
        print("\nPilih arah langkah kesadaranmu:")

        for nomor, lokasi in enumerate(lokasi_pilihan, start=1):
            print(f"  {nomor}. Pergi ke {lokasi}")
        print("  0. Bangun Paksa (Keluar)")

        pilihan = input("\nMasukkan pilihanmu: ")

        if pilihan == "0":
            print("\n[!] Kamu memaksa bangun... Kesadaran terputus.")
            self.game_selesai = True
            return

        if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(lokasi_pilihan):
            print("[!] Pilihan tidak valid!")
            self.mulai_mimpi()
            return

        tujuan = lokasi_pilihan[int(pilihan) - 1]
        self.level_mimpi += 1
        self.lokasi_sekarang = tujuan

        # EVALUASI LOGIKA: Cek apakah target sudah tercapai
        if self.lokasi_sekarang == self.lokasi_target:
            print(f"\n✨ LUAR BIASA! Kamu berhasil menemukan {self.lokasi_target}!")
            print(f"Rute DFS yang kamu temukan: {' -> '.join(self.rute_seharusnya)}")
            self.game_selesai = True
            return

        # Cek jika langkah sudah habis tapi belum sampai ke tujuan
        if self.level_mimpi >= 5:
            print("\n⚠️  Kesadaranmu tersesat terlalu dalam di alam bawah sadar!")
            print("Kamu gagal menemukan jalan dan terlempar kembali ke awal...")
            self.lokasi_sekarang = "Ruang Kelas" # Reset posisi
            self.level_mimpi = 0                 # Reset level
            input("[ Tekan ENTER untuk mencoba menata ulang pikiran... ]")
            
        # Lanjut rekursi perulangan mimpi
        self.mulai_mimpi()