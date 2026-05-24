from system.map import load_world

class MesinMimpi:
    def __init__(self):
        self.peta = load_world()
        self.lokasi_sekarang = "Ruang Kelas"
        self.level_mimpi = 0

    def mulai_mimpi(self):
        self.level_mimpi += 1

        print("\n======================")
        print(f"LAPISAN MIMPI KE-{self.level_mimpi}")
        print("======================")

        print(f"\nMC berada di: {self.lokasi_sekarang}")

        lokasi_tujuan = self.peta.tempat[self.lokasi_sekarang]

        print("\nJalur yang tersedia:")

        for nomor, lokasi in enumerate(lokasi_tujuan, start=1):
            print(f"{nomor}. {lokasi}")

        pilihan = input("\nPilih tujuan: ")

        if not pilihan.isdigit():
            print("Input harus berupa angka!")
            self.mulai_mimpi()
            return

        pilihan = int(pilihan)

        if pilihan < 1 or pilihan > len(lokasi_tujuan):
            print("Pilihan tidak tersedia!")
            self.mulai_mimpi()
            return

        tujuan = lokasi_tujuan[pilihan - 1]

        print(f"\nMC berpindah ke {tujuan}...")

        self.lokasi_sekarang = tujuan

        if self.level_mimpi >= 5:

            print("\nMC terlalu dalam masuk ke alam bawah sadar...")
            print("Lapisan mimpi telah stabil.")

            return

        self.mulai_mimpi()