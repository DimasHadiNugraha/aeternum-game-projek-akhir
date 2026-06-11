import json
import os

SAVE_FILE = "game_data/savegame.txt"




def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\n  ✦ Save game dihapus. Memulai dari awal.\n")
    else:
        print("\n  [!] Tidak ada file save yang ditemukan.\n")


#fungsi untuk meyimpan semua data game ke dalam file savegame.txt dalam format JSON. Dipanggil saat player memilih opsi "Save Game" di menu.
def save_game(journal, player, dream_vault, memory_vault,memory_stack, current_dream, current_node):
    data = {
        # Data player
        "player": {
            "name": getattr(player, 'name', 'MC'),
            "anxiety_level": getattr(player, 'anxiety_level', 0),
            "fragment_count": getattr(player, 'fragment_count', 0),
        },
        
        # Data vault
        "dream_vault": {
            "total_items": dream_vault.size if hasattr(dream_vault, 'size') else 0,
            "items": dream_vault.to_list() if hasattr(dream_vault, 'to_list') else []
        },
        "memory_vault": {
            "total_items": memory_vault.size if hasattr(memory_vault, 'size') else 0,
            "items": memory_vault.to_list() if hasattr(memory_vault, 'to_list') else []
        },
        "memory_stack": {
            "items": memory_stack.to_list() if hasattr(memory_stack, 'to_list') else []
        },
        # Info mimpi/dialog
        "dream_info": {
            "current_dream": current_dream,
            "current_node": current_node
        },
        
        # Journal entries
        "journal_entries": journal.to_list()
    }
    
    # Buat folder game_data kalau belum ada
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    
    # Tulis ke file JSON
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    
    print("  [✓] Game berhasil disimpan.\n")

#fungsi untuk memuat data game dari file savegame.txt. Dipanggil saat player memilih opsi "Load Game" di menu, atau saat game pertama kali dijalankan jika file save ditemukan.
def load_game(journal, player, dream_vault, memory_vault, memory_stack):
    if not os.path.exists(SAVE_FILE):
        print("  [!] File save tidak ditemukan. Mulai dari awal.\n")
        return None, None
    
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        
        # Restore data player
        if hasattr(player, 'name'):
            player.name = data["player"].get("name", "MC")
        if hasattr(player, 'anxiety_level'):
            player.anxiety_level = data["player"].get("anxiety_level", 0)
        if hasattr(player, 'fragment_count'):
            player.fragment_count = data["player"].get("fragment_count", 0)
        
        # Restore vault items
        if hasattr(dream_vault, 'load_from_list'):
            dream_vault.load_from_list(data["dream_vault"].get("items", []))
        if hasattr(memory_vault, 'load_from_list'):
            memory_vault.load_from_list(data["memory_vault"].get("items", []))
        if hasattr(memory_stack, 'load_from_list'):
            memory_stack.load_from_list(data["memory_stack"].get("items", []))
        # Restore journal
        if hasattr(journal, 'load_from_list'):
            journal.load_from_list(data.get("journal_entries", []))
        
        # Ambil info mimpi/dialog
        current_dream = data["dream_info"].get("current_dream", 1)
        current_node = data["dream_info"].get("current_node", 0)
        
        print(f"  [✓] Game dimuat. Lanjut dari Mimpi #{current_dream}.\n")
        return current_dream, current_node
    #jika file save rusak atau formatnya salah, tangani error dengan baik   
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  [!] Error membaca file save: {e}\n")
        return None, None