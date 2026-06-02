"""
main.py ini berfungsi untuk menyatukan semua kode dan desain ui
"""
#import library internal
import os
import sys
import time
import json

#import modul-modul game yang udah dibikin
from entities.player import Player
from entities.fragments import MemoryFragment, EmotionFragment, EMOTION_FRAGMENTS, MEMORY_FRAGMENTS
from system.state_manager import save_game, load_game, check_dream_over, save_exists
from utils.journal import DreamJournal
from utils.vault import MemoryVault
from utils.memory_stack import MemoryStack
from utils.hashing import HashTable, init_secrets
from system.dream import MesinMimpi

#======================
#1. utility & fungsi ui
#======================

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear') #hapus layar terminal biar ui game nya bersih & rapi

def typewriter(text, speed=0.015): #kasih efek ngetik
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def draw_hud(player): #fungsi buat nampilin hud(konstan) di bagian atas layar terminal
    max_bars = 15
    #hitung bar jumlah anxiety 
    current_bars = int((player.anxiety_level / player.max_anxiety) * max_bars)
    current_bars = min(current_bars, max_bars)
    anxiety_bar = "█" * current_bars + "░" * (max_bars - current_bars)

    total_fragments = player.dream_vault.size + player.memory_vault.size #hitung total fragment yang udah dikumpulin player

    # Tentukan lebar area di dalam kotak (60 karakter)
    lebar = 60

    print("┌" + "─" * lebar + "┐")
    print("│ " + "✦ AETERNUM | STATUS".ljust(lebar - 1) + "│")
    print("├" + "─" * lebar + "┤")
    print("│ " + f"Pemain         : {player.name}".ljust(lebar - 1) + "│")
    print("│ " + f"Tingkat Mimpi  : Mimpi #{player.current_dream}".ljust(lebar - 1) + "│")
    print("│ " + f"Anxiety        : [{anxiety_bar}] {player.anxiety_level}/{player.max_anxiety}".ljust(lebar - 1) + "│")
    print("│ " + f"Total Fragment : {total_fragments}".ljust(lebar - 1) + "│")
    print("└" + "─" * lebar + "┘\n")

def display_welcome_screen(): #nampilin splash/welcome screen
    clear_terminal
    print("""
 █████╗ ███████╗████████╗███████╗██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║████╗ ████║
███████║█████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║██║   ██║██╔████╔██║
██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██║╚██╔╝██║
██║  ██║███████╗   ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
    """)
    print("       ✦ FRAGMENTS OF THE LUCID MIND 1.0 ✦        ")
    print("  ✦═══════════════════════════════════════════════════════════════════✦")
    print("  la bienvenue, Aeterie! Ayo mulai berkelana di dunia Aeternum ✨")
    print("  Tujuanmu hanya satu: kumpulkan serpihan memori dan keluar dari")
    print("  mimpi buruk ini. Semoga kamu berhasil mendapatkan ingatanmu")
    print("  kembali, Aeterie! Enjoy the game ♡ ")
    print("  ✦═══════════════════════════════════════════════════════════════════✦")
    print("  [ Dev Note  ]: Game ini dibuat oleh kelompok 5 untuk memenuhi tugas")
    print("                 akhir case-based Algoritma Pemrograman & Struktur Data")
    print("  ✦═══════════════════════════════════════════════════════════════════✦\n")

#====================
#2. Sistem Notifikasi
#====================

def trigger_notifications(node, player):
    """Mengecek perubahan stat atau reward fragment dari pilihan dialog."""
    # KUNCI PERBAIKAN: Lebar kotak diperbesar jadi 75 agar teks panjang tidak jebol
    lebar_notif = 75 

    # 1. Logika Perubahan Tingkat Anxiety
    anxiety_change = node.get("anxiety_change", 0)
    if anxiety_change > 0:
        print("┌" + "─" * lebar_notif + "┐")
        print("│ " + "⚠️  NOTIFICATION".center(lebar_notif - 1) + "│")
        print("│ " + "".ljust(lebar_notif - 1) + "│")
        print("│ " + "Something feels off...".center(lebar_notif - 1) + "│")
        print("│ " + f"Anxiety (+{anxiety_change})".center(lebar_notif - 1) + "│")
        print("└" + "─" * lebar_notif + "┘\n")
        player.increase_anxiety(anxiety_change)
        
    elif anxiety_change < 0:
        print("┌" + "─" * lebar_notif + "┐")
        print("│ " + "✨ NOTIFICATION".center(lebar_notif - 1) + "│")
        print("│ " + "".ljust(lebar_notif - 1) + "│")
        print("│ " + "Pikiranmu sedikit tenang...".center(lebar_notif - 1) + "│")
        print("│ " + f"Anxiety ({anxiety_change})".center(lebar_notif - 1) + "│")
        print("└" + "─" * lebar_notif + "┘\n")
        player.decrease_anxiety(abs(anxiety_change))

    # 2. Logika Reward Fragment Baru
    fragment_id = node.get("fragment_reward")
    if fragment_id and fragment_id != "lucid_key":
        frag_obj = EMOTION_FRAGMENTS.get(fragment_id) or MEMORY_FRAGMENTS.get(fragment_id)
        if frag_obj:
            # Menyimpan item ke vault
            player.add_fragment(frag_obj) 
            
            # Mencetak box notifikasi fragment
            print("┌" + "─" * lebar_notif + "┐")
            print("│ " + "◈ New fragment! ◈".center(lebar_notif - 1) + "│")
            print("│ " + "".ljust(lebar_notif - 1) + "│")
            print("│ " + "A forgotten piece returns to you.".ljust(lebar_notif - 1) + "│")
            print("│ " + f"Name: {frag_obj.name}".ljust(lebar_notif - 1) + "│")
            print("│ " + f"Type: {frag_obj.fragment_type.upper()}".ljust(lebar_notif - 1) + "│")
            print("│ " + f"Desc: {frag_obj.description}".ljust(lebar_notif - 1) + "│")
            print("└" + "─" * lebar_notif + "┘\n")
            time.sleep(1.5)
            
#================
#narrative engine
#================

def execute_narrative_loop(file_path, root_key, player, journal, memory_stack):
    #membaca data narasi JSON dan eksekusi dialog tree
    if not os.path.exists(file_path):
        print(f"[!] File data narasi {file_path} tidak ditemukan")
        return False
    
    with open(file_path, "r") as f:
        story_data = json.load(f)

    scene = story_data[root_key]
    current_node_id = scene["start_node"]
    nodes = scene["nodes"]

    while current_node_id:
        node = nodes.get(current_node_id)
        if not node:
            break

        clear_terminal()
        draw_hud(player)
        trigger_notifications(node, player)

        #cek apakah tingkat kecemasan lebihin batas
        if player.anxiety_level >= player.max_anxiety:
            player.dream_over = True
            return "DREAM_OVER"
        
        #menampilkan pembicara atau narator teks
        speaker = node.get("speaker")
        if speaker:
            spk_name = player.name if speaker == player else speaker
            print(f"◉ [{spk_name.upper()}]")
        else:
            print("NARRATOR")
        print("═══════════✦")

        #efek ngetik baris teks
        for line in node.get("text", []):
            if "{player.name}" in line:
                line = line.format(player_name=player.name)
            if "{player_name}" in line:
                line = line.replace("{player_name}", player.name)
            typewriter(line, speed=0.01)
            time.sleep(0.2)
        print("─" * 60 + "\n")

        #cek pencatatan ingatan ke LIFO Stack atau Linked List Journal
        if node.get("ending") is False and speaker == "player":
            #menyimpan ingatan terakhir ke stack jangka pendek
            last_text = node.get("text", [""])[0]
            memory_stack.push(last_text)
            journal.add_entry(last_text, player.current_dream)

        #penanganan tipe input khusus (Pengisian nama manual)
        if node.get("input_type") == "player_name":
            nama_input = input("✍️  Ketikkan namamu di sini: ")
            if nama_input.strip():
                player.name = nama_input
            current_node_id = node.get("auto_next")
            continue

        #penanganan cabang pilihan keputusan (Decision Tree)
        choices = node.get("choices", [])
        if choices:
            print("Pilih respon tindakan kesadaranmu:")
            for idx, choice in enumerate(choices, start=1):
                print(f"  {idx}. {choice['text']}")
            print()

            while True:
                pilihan = input("Masukkan angka pilihanmu: ")
                if pilihan.isdigit() and 1 <= int(pilihan) <= len(choices):
                    chosen_choice = choices[int(pilihan) - 1]
                    current_node_id = chosen_choice["next_node"]
                    break
                else:
                    print("[!] Masukan tidak valid. Pilih angka yang tersedia di menu.")
        else:
            # Jika tidak ada pilihan jawaban
            if node.get("ending") is True:
                # Jeda khusus agar pemain bisa membaca kalimat terakhir sebelum layar dibersihkan
                input("\n[ Tekan ENTER untuk mengakhiri memori ini... ]")
                break
                
            auto_next = node.get("auto_next")
            if auto_next:
                input("\n[ Tekan ENTER untuk melanjutkan penelusuran... ]")
                current_node_id = auto_next
            else:
                break

    return "SCENE_COMPLETED"

# ==========================================
# 4. GAME MAIN CONTROL CENTER
# ==========================================

def main():
    # Menginisialisasi objek dasar player (Nama default sebelum diinput)
    player = Player(name="Aethel")
    # Patch atribut fragment_count agar sesuai dengan kebutuhan state_manager
    player.fragment_count = 0 
    
    # Menyiapkan instansiasi struktur data
    journal = DreamJournal()
    dream_vault = MemoryVault("Dream Vault")
    memory_vault = MemoryVault("Memory Vault")
    memory_stack = MemoryStack(max_size=5)
    hash_table = HashTable()
    init_secrets(hash_table)

    display_welcome_screen()

    # Sistem Menu Awal Game (Save / Load Game Handling)
    if save_exists():
        print("  [!] Progress ingatan masa lalu terdeteksi di sistem.")
        print("  1. Lanjutkan Mimpi Jangka Pendek (Load Game)")
        print("  2. Hancurkan Ingatan Lama & Mulai Baru (New Game)")
        print("─" * 68)
        while True:
            pilihan = input("Pilih langkah awalmu (1/2): ")
            if pilihan == "1":
                # Memuat seluruh struktur data dari file eksternal
                saved_dream = load_game(player, journal, dream_vault, memory_vault, memory_stack, hash_table)
                if saved_dream:
                    player.current_dream = saved_dream
                break
            elif pilihan == "2":
                print("\nMengubur trauma lama...")
                time.sleep(1)
                break
    else:
        input("  [ Tekan ENTER Untuk Memulai Permainan... ]")

    # Alur Urutan Eksekusi Tahapan Mimpi Game
    dream_sequence = [
        {"file": "game_data/dialog/prologue.json", "root": "prologue", "label": "Prologue: Awakening"},
        {"file": "game_data/dialog/dream1.json", "root": "dream_1", "label": "Mimpi 1: The Betrayal"},
        {"file": "game_data/dialog/dream2.json", "root": "dream_2", "label": "Mimpi 2: Requiem of Silence"},
        {"file": "game_data/dialog/dream3.json", "root": "dream_3", "label": "Mimpi 3: His Heartbeat"}
        
    ]

    while player.current_dream <= len(dream_sequence):
        current_idx = player.current_dream - 1
        active_scene = dream_sequence[current_idx]

        # ==========================================
        # integrasi graph & DFS (eksplorasi lokasi)
        # ==========================================
        # panggil map eksplorasi HANYA setelah prolog selesai (Sebelum Mimpi 1 & 2)
        if active_scene["root"] != "prologue":
            clear_terminal()
            print("─" * 60)
            print(" 🧭  MEMASUKI LABIRIN MEMORI (GRAPH EXPLORATION)  🧭")
            print("─" * 60)
            print(" [Narator]: Kamu harus mencari letak ingatan selanjutnya di alam bawah sadar...")
            time.sleep(2)
            
            # Memanggil class MesinMimpi dari dream.py
            mesin_eksplorasi = MesinMimpi()
            mesin_eksplorasi.mulai_mimpi() 
            
            # 1. CEK JIKA PEMAIN MEMILIH '0' UNTUK KELUAR PAKSA
            if mesin_eksplorasi.game_selesai and mesin_eksplorasi.level_mimpi < 5:
                print("\n ⚠️  Eksplorasi dihentikan secara paksa oleh pemain.")
                print(" Kesadaranmu terputus dari labirin mimpi...")
                time.sleep(2)
                break  # Ini akan menghentikan game sepenuhnya dan keluar ke terminal

            # 2. JIKA BERHASIL MENCAPAI LEVEL 5 (SELESAI EKSPLORASI)
            clear_terminal()
            print("─" * 60)
            print(" ✨  JALUR DITEMUKAN MENGGUNAKAN DFS!  ✨")
            print("─" * 60)
            time.sleep(2)
        # ==========================================

        print(f"\n[~] Menyelami {active_scene['label']}...")
        time.sleep(1.5)

        # Menjalankan mesin narasi (Decision Tree)
        result = execute_narrative_loop(
            file_path=active_scene["file"],
            root_key=active_scene["root"],
            player=player,
            journal=journal,
            memory_stack=memory_stack
        )
        
        # ... (sisa kode di bawahnya tetap sama seperti sebelumnya)

        # Mengatasi Kejadian Overwhelmed / Dream Over
        # Mengatasi Kejadian Overwhelmed / Dream Over
        if result == "DREAM_OVER":
            clear_terminal()
            ascii_art = """
██████  ██████  ███████  █████  ███    ███      ██████  ██    ██ ███████ ██████  
██   ██ ██   ██ ██      ██   ██ ████  ████     ██    ██ ██    ██ ██      ██   ██ 
██   ██ ██████  █████   ███████ ██ ████ ██     ██    ██ ██    ██ █████   ██████  
██   ██ ██   ██ ██      ██   ██ ██  ██  ██     ██    ██  ██  ██  ██      ██   ██ 
██████  ██   ██ ███████ ██   ██ ██      ██      ██████    ████   ███████ ██   ██ 
                                                                                 
                                                                                 ]
            """
           
            print("\n" * 2)
            for line in ascii_art.strip().split('\n'):
                print(line.center(80))
            
            print("\n")
            print("❌ KESADARAN ANDA HANCUR (DREAM OVER) ❌".center(80))
            print("Anxiety Level mencapai batas puncak pertahanan mental.".center(80))
            print("Jiwamu terlempar kembali ke awal lapisan mimpi ini...".center(80))
            print("\n")
            print("═" * 80)
            
            player.reset_dream_state() 
            
            # Input untuk lanjut dengan posisi di tengah
            print("\n")
            input("[ Tekan ENTER untuk menyusun ulang kesadaran... ]".center(80))
            continue

        # Jika Scene Berhasil Diselesaikan, Simpan Otomatis dan Lanjut Tahap Berikutnya
        if result == "SCENE_COMPLETED":
            clear_terminal()
            print("─" * 60)
            print(f" 🎉   TAHAPAN {active_scene['label'].upper()} TERSURAT   🎉")
            print(" Kesadaranmu berhasil bertahan melampaui manifestasi trauma.")
            print("─" * 60)
            
            # Tampilkan Ringkasan Memory Stack Jangka Pendek Saat Ini
            memory_stack.display()
            
            player.current_dream += 1
            # Menyimpan progress real-time ke savegame.txt
            save_game(player, journal, dream_vault, memory_vault, memory_stack, hash_table, player.current_dream)
            
            if player.current_dream <= len(dream_sequence):
                input("\n[ Tekan ENTER untuk menyelami lapisan mimpi berikutnya... ]")

    # Ending Utama Permainan
    clear_terminal()
    print("═" * 60)
    print(" 🌟  CONGRATULATIONS: KESADARAN TERBENTUK SEMPURNA  🌟")
    print("═" * 60)
    print(f" Selamat, {player.name}. Kamu telah berhasil menelusuri seluruh")
    print(" labirin mimpi buruk dan menghadapi bayang-bayang masa lalu.")
    print(" Jiwamu kini telah stabil dan siap untuk terbangun seutuhnya.")
    print("═" * 60 + "\n")
    journal.display()

if __name__ == "__main__":
    main()





