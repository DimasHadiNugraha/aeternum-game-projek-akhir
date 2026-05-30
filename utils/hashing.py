class HashNode:
    def __init__(self, key, value):
        self.key = key      # Memory key (e.g. "Memory Key #1")
        self.value = value  # Rahasia/narasi yang terkunci
 
 
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # List of lists (chaining)
        self.total_items = 0
 
    def hash_function(self, key):
        return sum(ord(c) for c in key) % self.size
 
    def insert(self, key, value):

        index = self.hash_function(key)
        bucket = self.table[index]
 
        # Cek apakah key sudah ada — kalau ada update valuenya
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                print(f"  [~] Memory Key '{key}' diupdate.")
                return
 
        # Kalau belum ada, tambahkan ke bucket (chaining)
        bucket.append((key, value))
        self.total_items += 1
        print(f"  [+] Memory Key '{key}' berhasil disimpan.")
 
    def get(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
 
        for k, v in bucket:
            if k == key:
                return v
 
        return None
 
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
 
    def display(self):
        """Tampilkan seluruh isi hash table."""
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
 
    def to_dict(self):
        result = {}
        for bucket in self.table:
            for k, v in bucket:
                result[k] = v
        return result
 
    def load_from_dict(self, data):
        """Load hash table dari dict saat load_game dipanggil."""
        self.table = [[] for _ in range(self.size)]
        self.total_items = 0
        for key, value in data.items():
            self.insert(key, value)

def init_secrets(hash_table):
    """Isi hash table dengan semua rahasia karakter."""
    secrets = {
        "Memory Key #1": "Kamu pernah melihat seseorang jatuh. Kamu diam saja.",
        "Memory Key #2": "Nama yang selalu kamu hindari tertulis di batu nisan itu.",
        "Memory Key #3": "Suara tangisan itu bukan dari luar kamar. Itu suaramu sendiri."
    }
    for key, value in secrets.items():
        hash_table.insert(key, value)