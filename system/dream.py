from system.map import load_world


class MesinMimpi:
    def __init__(self, lokasi_awal="Ruang Kelas"):
        self.peta = load_world()
        self.lokasi_sekarang = lokasi_awal
        self.level_mimpi = 0
        self.game_selesai = False

    def ambil_jalur(self, lokasi):
        return self.peta.tempat.get(lokasi, [])

    def mulai_mimpi(self):
        lokasi_tujuan = self.ambil_jalur(self.lokasi_sekarang)

        # Validasi apakah lokasi sekarang ada di peta
        if not lokasi_tujuan:
            print("\nLokasi tidak valid atau tidak memiliki jalur!")
            return

        print("\n======================")
        print(f"LAPISAN MIMPI KE-{self.level_mimpi + 1}")
        print("======================")

        print(f"\nMC berada di: {self.lokasi_sekarang}")

        print("\nJalur yang tersedia:")

        # Menampilkan daftar tujuan
        for nomor, lokasi in enumerate(lokasi_tujuan, start=1):
            print(f"{nomor}. {lokasi}")

        print("0. Keluar dari mimpi")

        pilihan = input("\nPilih tujuan: ")

        # Exit condition jika player ingin keluar
        if pilihan == "0":
            print("\nMC memutuskan keluar dari mimpi...")
            print("Dream Over.")
            self.game_selesai = True
            return

        # Validasi input harus angka
        if not pilihan.isdigit():
            print("Input harus berupa angka!")
            self.mulai_mimpi()
            return

        pilihan = int(pilihan)

        # Validasi pilihan sesuai daftar
        if pilihan < 1 or pilihan > len(lokasi_tujuan):
            print("Pilihan tidak tersedia!")
            self.mulai_mimpi()
            return

        # Level mimpi hanya bertambah jika input benar
        self.level_mimpi += 1

        tujuan = lokasi_tujuan[pilihan - 1]

        print(f"\nMC berpindah ke {tujuan}...")

        # Update lokasi pemain
        self.lokasi_sekarang = tujuan

        # Ending condition
        if self.level_mimpi >= 5:
            print("\nMC terlalu dalam masuk ke alam bawah sadar...")
            print("Lapisan mimpi telah stabil.")
            print("ENDING TERCAPAI.")
            self.game_selesai = True
            return

        # Rekursi untuk melanjutkan permainan
        self.mulai_mimpi()