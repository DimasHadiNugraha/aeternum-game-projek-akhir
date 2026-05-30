import json

class PetaGame:
    def __init__(self):
        # Menyimpan semua tempat dan jalur yang terhubung
        self.tempat = {}

# Menambahkan hubungan dua arah antar tempat
    def tambah_jalan(self, tempat1, tempat2): 
        if tempat1 not in self.tempat:
            self.tempat[tempat1] = []

        if tempat2 not in self.tempat:
            self.tempat[tempat2] = []

        # Cek apakah koneksi sudah ada
        if tempat2 not in self.tempat[tempat1]:
            self.tempat[tempat1].append(tempat2)

        if tempat1 not in self.tempat[tempat2]:
            self.tempat[tempat2].append(tempat1)

    def get_tempat(self):
        # Getter untuk mengambil seluruh data tempat

        return self.tempat

    def get_jalur(self, tempat):
        # Getter untuk mengambil jalur dari suatu tempat

        return self.tempat.get(tempat, [])

    def tampilkan_peta(self):
        for tempat in self.tempat:
            print(f"{tempat} -> {self.tempat[tempat]}")

    def cari_jalan(self, awal, tujuan, sudah_dikunjungi=None):
        # Mencari jalur dari titik awal ke tujuan menggunakan DFS

        if sudah_dikunjungi is None:
            sudah_dikunjungi = []

        # Validasi node awal dan tujuan
        if awal not in self.tempat:
            print(f"Tempat '{awal}' tidak ditemukan!")
            return None

        if tujuan not in self.tempat:
            print(f"Tempat '{tujuan}' tidak ditemukan!")
            return None

        # Tandai node sudah dikunjungi
        sudah_dikunjungi.append(awal)

        if awal == tujuan:
            return sudah_dikunjungi

        # Telusuri semua jalur yang terhubung
        for tempat_tujuan in self.tempat[awal]:

            # Hindari mengunjungi node yang sama
            if tempat_tujuan not in sudah_dikunjungi:

                hasil = self.cari_jalan(
                    tempat_tujuan,
                    tujuan,
                    sudah_dikunjungi.copy()
                )

                if hasil:
                    return hasil # jika jalan ditemukan

        return None # jika jalan buntu


def load_world():
    
    # Membaca JSON dan membangun graph
    with open("game_data/locations.json", "r") as file:
        data = json.load(file)

    peta_game = PetaGame()

    # Memasukkan semua jalur dari JSON ke graph
    for tempat, jalan in data["locations"].items():
        for tujuan in jalan:
            peta_game.tambah_jalan(tempat, tujuan)

    return peta_game