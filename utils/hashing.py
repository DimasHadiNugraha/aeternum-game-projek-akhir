#class untuk hash table yang menyimpan memory key dan rahasia/narasi yang terkunci. Digunakan untuk menyimpan ingatan karakter yang bisa dibuka dengan memory key tertentu. Hash table ini menggunakan chaining untuk menangani collision, dan memiliki fungsi untuk insert, get, delete, serta menampilkan seluruh isi hash table. Juga ada fungsi khusus untuk membuka rahasia berdasarkan memory key yang dimasukkan pemain.
class HashNode:
    def __init__(self, key, value):
        self.key = key      # Memory key (e.g. "Memory Key #1")
        self.value = value  # Rahasia/narasi yang terkunci
 
#class untuk hash table yang menyimpan memory key dan rahasia/narasi yang terkunci. Digunakan untuk menyimpan ingatan karakter yang bisa dibuka dengan memory key tertentu.
# Hash table ini menggunakan chaining untuk menangani collision, dan memiliki fungsi untuk insert, get, delete, serta menampilkan seluruh isi hash table. 
#Juga ada fungsi khusus untuk membuka rahasia berdasarkan memory key yang dimasukkan pemain.
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # List of lists (untuk chaining)
        self.total_items = 0
    #fungsi untuk menggubah key string menjadi index
    def hash_function(self, key): # menggubah key string menjadi index
        return sum(ord(c) for c in key) % self.size

    #fungsi untuk menambahkan key-value pair baru ke hash table. Jika key sudah ada, update value-nya. 
    #Dipanggil saat player mendapatkan memory key baru atau saat load game untuk mengisi hash table dengan data dari savegame.txt.
    def insert(self, key, value): 
        index = self.hash_function(key)
        bucket = self.table[index]
 
        # Cek apakah key sudah ada
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value) #jika sudah ada, update value-nya
                print(f"  [~] Memory Key '{key}' diupdate.")
                return
 
        # Kalau belum ada, tambahkan ke bucket (chaining)
        bucket.append((key, value))
        self.total_items += 1
        print(f"  [+] Memory Key '{key}' berhasil disimpan.")
 
    #fungsi untuk mendapatkan value berdasarkan key
    def get(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
 
        for k, v in bucket:
            if k == key:
                return v
 
        return None
    #fungsi untuk menghapus key dari hash table
    def delete(self, key): 
        index = self.hash_function(key)
        bucket = self.table[index]
 
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.total_items -= 1
                print(f"  [-] Memory Key '{key}' dihapus.")
                return True
 
        print(f"  [!] Memory Key '{key}' tidak ditemukan.")
        return False
    #fungsi untuk membuka rahasia berdasarkan memory key yang dimasukkan pemain
    def unlock_secret(self, key): 
        secret = self.get(key)
 
        if secret:
            print("\n" + "=" * 40)
            print("  ✦ INGATAN TERKUNCI TERBUKA ✦")
            print("=" * 40)
            print(f"  {secret}")
            print("=" * 40 + "\n")
            return secret
        else:
            print(f"\n  [!] Kunci '{key}' tidak membuka apapun.\n")
            return None
 
    #fungsi untuk menampilkan seluruh isi hash table
    def display(self):
        print("\n" + "=" * 40)
        print("     ✦ HASH TABLE ✦")
        print(f"     Total Keys: {self.total_items}")
        print("=" * 40)
 
        for i, bucket in enumerate(self.table):
            if bucket:
                for k, v in bucket:
                    print(f"  index {i} -> '{k}'")
                    print(f"           └─ {v[:50]}...")
 
        print("=" * 40 + "\n")
    #fungsi untuk mengubah seluruh isi hash table menjadi dict saat save_game dipanggil
    def to_dict(self):
        result = {}
        for bucket in self.table:
            for k, v in bucket:
                result[k] = v
        return result
    #fungsi untuk memuat hash table dari dict saat load_game dipanggil
    def load_from_dict(self, data): 
        self.table = [[] for _ in range(self.size)]
        self.total_items = 0
        for key, value in data.items():
            self.insert(key, value)
#fungsi untuk mengisi hash table dengan rahasia yang bisa dibuka dengan memory key tertentu. Dipanggil saat inisialisasi game untuk mengisi hash table dengan data rahasia yang sudah ditentukan.
def init_secrets(hash_table): 
    secrets = {
        "Memory Key #1": "Kamu pernah melihat seseorang jatuh. Kamu diam saja.",
        "Memory Key #2": "Nama yang selalu kamu hindari tertulis di batu nisan itu.",
        "Memory Key #3": "Suara tangisan itu bukan dari luar kamar. Itu suaramu sendiri."
    }
    for key, value in secrets.items():
        hash_table.insert(key, value)