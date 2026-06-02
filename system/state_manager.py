import json
import os

SAVE_FILE = "game_data/savegame.txt"


def reset_dream(player, nightmare_loop, journal):
    """
    Dipanggil saat anxiety_level mencapai 30 (DREAM OVER).
    Hanya mereset anxiety dan nightmare loop — item vault tetap ada.

    Yang direset:
    - anxiety_level kembali ke 0
    - Posisi loop kembali ke head
    - Semua node corrupt di loop direset
    - Journal dikosongkan (mimpi dimulai dari awal)

    Yang TIDAK direset:
    - fragment_count
    - Isi dream vault dan memory vault
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
    journal.clear()  # ← Reset journal saat dream over


def check_dream_over(player, nightmare_loop, journal):
    """
    Cek apakah anxiety sudah mencapai 30.
    Kalau iya, panggil reset_dream() secara otomatis.
    Kembalikan True kalau dream over, False kalau belum.
    """
    if player.anxiety_level >= 30:
        reset_dream(player, nightmare_loop, journal)
        return True
    return False


def delete_save():
    """
    Hapus file save game.
    Dipanggil kalau player mau mulai dari awal.
    """
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\n  ✦ Save game dihapus. Memulai dari awal.\n")
    else:
        print("\n  [!] Tidak ada file save yang ditemukan.\n")


def save_exists():
    """Cek apakah file save sudah ada atau belum."""
    return os.path.exists(SAVE_FILE)