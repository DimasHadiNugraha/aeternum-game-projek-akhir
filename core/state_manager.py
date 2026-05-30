import json
import os


# Path file save game
SAVE_FILE = "data/savegame.txt"


def save_game(player, journal, dream_vault, memory_vault, memory_stack, hash_table, dream_number):
    """
    Simpan seluruh progress game ke file savegame.txt dalam format JSON.
    Dipanggil setiap kali mimpi selesai atau player keluar dari game.

    Data yang disimpan:
    - anxiety_level dan fragment_count dari player
    - Nomor mimpi yang sedang berjalan
    - Isi journal, dream vault, memory vault, memory stack
    - Isi hash table (memory key dan rahasianya)
    """
    data = {
        "anxiety_level"  : player.anxiety_level,
        "fragment_count" : player.fragment_count,
        "dream_number"   : dream_number,
        "journal"        : journal.to_list(),
        "dream_vault"    : dream_vault.to_list(),
        "memory_vault"   : memory_vault.to_list(),
        "memory_stack"   : memory_stack.to_list(),
        "hash_table"     : hash_table.to_dict()
    }

    # Buat folder data kalau belum ada
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("\n  ✦ Progress berhasil disimpan.\n")


def load_game(player, journal, dream_vault, memory_vault, memory_stack, hash_table):
    """
    Load progress game dari file savegame.txt.
    Kembalikan dream_number kalau berhasil, None kalau file tidak ada.

    Semua struktur data diisi ulang menggunakan load_from_list()
    dan load_from_dict() dari masing-masing class.
    """
    if not os.path.exists(SAVE_FILE):
        print("\n  [!] File save tidak ditemukan. Mulai dari awal.\n")
        return None

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # Restore data player
    player.anxiety_level  = data.get("anxiety_level", 0)
    player.fragment_count = data.get("fragment_count", 0)

    # Restore semua struktur data
    journal.load_from_list(data.get("journal", []))
    dream_vault.load_from_list(data.get("dream_vault", []))
    memory_vault.load_from_list(data.get("memory_vault", []))
    memory_stack.load_from_list(data.get("memory_stack", []))
    hash_table.load_from_dict(data.get("hash_table", {}))

    dream_number = data.get("dream_number", 1)

    print("\n  ✦ Progress berhasil dimuat.")
    print(f"  Melanjutkan dari Mimpi #{dream_number}.\n")

    return dream_number


def reset_dream(player, nightmare_loop):
    """
    Dipanggil saat anxiety_level mencapai 30 (DREAM OVER).
    Hanya mereset anxiety dan nightmare loop — item vault tetap ada.

    Yang direset:
    - anxiety_level kembali ke 0
    - Posisi loop kembali ke head
    - Semua node corrupt di loop direset

    Yang TIDAK direset:
    - fragment_count
    - Isi dream vault dan memory vault
    - Isi journal
    - Isi memory stack
    """
    print("\n" + "=" * 40)
    print("        ✦ DREAM OVER ✦")
    print("  Anxiety terlalu tinggi.")
    print("  Kamu terbangun dari mimpi...")
    print("  Mimpi ini akan dimulai ulang.")
    print("=" * 40 + "\n")

    player.anxiety_level = 0
    nightmare_loop.reset_corruption()
    nightmare_loop.current = nightmare_loop.head


def check_dream_over(player, nightmare_loop):
    """
    Cek apakah anxiety sudah mencapai 30.
    Kalau iya, panggil reset_dream() secara otomatis.
    Kembalikan True kalau dream over, False kalau belum.
    """
    if player.anxiety_level >= 30:
        reset_dream(player, nightmare_loop)
        return True
    return False


def delete_save():
    """
    Hapus file save game.
    Dipanggil kalau player mau mulai dari awal.
    """
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\n  Save game dihapus. Memulai dari awal.\n")
    else:
        print("\n Tidak ada file save yang ditemukan.\n")


def save_exists():
    """Cek apakah file save sudah ada atau belum."""
    return os.path.exists(SAVE_FILE)
