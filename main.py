"""
main.py ini berfungsi untuk menyatukan semua kode dan desain ui
"""
#import library internal
import os
import sys
import time
import json

# Import modul-modul game
from entities.player import Player
from entities.fragments import MemoryFragment, EmotionFragment, EMOTION_FRAGMENTS, MEMORY_FRAGMENTS
from utils.journal import DreamJournal          
from utils.vault import MemoryVault
from utils.memory_stack import MemoryStack
from utils.hashing import HashTable, init_secrets
from system.dream import MesinMimpi
from system.state_manager import check_dream_over  

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
    print("                 ✦ FRAGMENTS OF THE LUCID MIND 1.0 ✦        ")
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
#2.notifikasi
#====================

def trigger_notifications(node, player):
    """Mengecek perubahan stat atau reward fragment dari pilihan dialog."""
    lebar_notif = 75 

    #logika perubahan tingkat anxiety
    anxiety_change = node.get("anxiety_change", 0)
    if anxiety_change > 0:
        print("┌" + "─" * lebar_notif + "┐")
        print("│" + "▶ NOTIFICATION".center(lebar_notif - 1) + " │") 
        print("│" + "".center(lebar_notif) + "│")
        print("│" + "Something feels off...".center(lebar_notif) + "│")
        print("│" + f"Anxiety (+{anxiety_change})".center(lebar_notif) + "│")
        print("└" + "─" * lebar_notif + "┘\n")
        player.increase_anxiety(anxiety_change)
        
    elif anxiety_change < 0:
        print("┌" + "─" * lebar_notif + "┐")
        print("│" + "✨ NOTIFICATION".center(lebar_notif - 1) + " │")
        print("│" + "".center(lebar_notif) + "│")
        print("│" + "Pikiranmu sedikit tenang...".center(lebar_notif) + "│")
        print("│" + f"Anxiety ({anxiety_change})".center(lebar_notif) + "│")
        print("└" + "─" * lebar_notif + "┘\n")
        player.decrease_anxiety(abs(anxiety_change))

    #logika reward fragment baru
    fragment_id = node.get("fragment_reward")
    if fragment_id and fragment_id != "lucid_key":
        frag_obj = EMOTION_FRAGMENTS.get(fragment_id) or MEMORY_FRAGMENTS.get(fragment_id)
        if frag_obj:
            #menyimpan item ke vault
            player.add_fragment(frag_obj) 
            
            #mencetak box notifikasi fragment
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
#narasi
#================

def execute_narrative_loop(file_path, root_key, player, journal, memory_stack):
    """Membaca data narasi JSON dan mengeksekusi pohon keputusan dialog."""
    if not os.path.exists(file_path):
        print(f"[!] File data narasi {file_path} tidak ditemukan!")
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

        #===========================================
        #penggunaan rewind key pas anxiety level max
        #===========================================
        if player.anxiety_level >= player.max_anxiety:
            #cek apakah player memiliki rewind key dan memiliki riwayat pilihan di Stack
            if hasattr(player, 'rewind_keys') and player.rewind_keys > 0 and player.decision_history:
                print("\n┌" + "─" * 65 + "┐")
                print("│ " + "⏳ KESADARAN TERANCAM HANCUR (REWIND DETECTED) ⏳".center(64) + "│")
                print("├" + "─" * 65 + "┤")
                print("│ " + f"Kamu memiliki {player.rewind_keys} Rewind Key tersisa.".ljust(64) + "│")
                print("│ " + "Apakah kamu ingin memutar balik waktu ke pilihan sebelumnya?".ljust(64) + "│")
                print("└" + "─" * 65 + "┘")
                pilihan_rewind = input("👉 Gunakan Rewind Key? (Y/N): ")
                
                if pilihan_rewind.lower() == 'y':
                    player.rewind_keys -= 1
                    #turunkan kecemasan agar terhindar dari dream over
                    player.anxiety_level = player.max_anxiety - 15 
                    
                    #POP STACK: ambil node terakhir tempat pilihan dibuat
                    current_node_id = player.decision_history.pop()
                    print("\n⏳ Memutar balik takdir... Menata kembali pertahanan mental.")
                    time.sleep(2)
                    continue  #mengulang loop kesadaran dari node masa lalu
            
            player.dream_over = True
            return "DREAM_OVER"

        speaker = node.get("speaker")
        if speaker:
            spk_name = player.name if speaker == "player" else speaker
            print(f"🗣️  [{spk_name.upper()}]")
        else:
            print("👁️  [ALAM BAWAH SADAR]")
        print("─" * 60)

        for line in node.get("text", []):
            if "{player_name}" in line:
                line = line.replace("{player_name}", player.name)
            typewriter(line, speed=0.01)
            time.sleep(0.2)
        print("─" * 60 + "\n")

        if node.get("ending") is False and speaker == "player":
            last_text = node.get("text", [""])[0]
            memory_stack.push(last_text)
            journal.add_entry(last_text, player.current_dream)

        if node.get("input_type") == "player_name":
            nama_input = input("✍️  Ketikkan namamu di sini: ")
            if nama_input.strip():
                player.name = nama_input
            current_node_id = node.get("auto_next")
            continue

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
                    
                    #PUSH STACK: simpan node saat ini sebelum melangkah ke cabang baru
                    if hasattr(player, 'decision_history'):
                        player.decision_history.append(current_node_id)
                    
                    current_node_id = chosen_choice["next_node"]
                    break
                else:
                    print("[!] Masukan tidak valid. Pilih angka yang tersedia di menu.")
        else:
            if node.get("ending") is True:
                input("\n[ Tekan ENTER untuk mengakhiri memori ini... ]")
                break
                
            auto_next = node.get("auto_next")
            if auto_next:
                input("\n[ Tekan ENTER untuk melanjutkan penelusuran... ]")
                current_node_id = auto_next
            else:
                break

    return "SCENE_COMPLETED"

#============================
#4.GAME MAIN CONTROL CENTER
#============================

def main():
    #inisialisasi objek dasar player (nama default sebelum diinput)
    player = Player(name="Aeterie")
    player.fragment_count = 0 
    
    #menyiapkan instansiasi struktur data
    journal = DreamJournal()
    dream_vault = MemoryVault("Dream Vault")
    memory_vault = MemoryVault("Memory Vault")
    memory_stack = MemoryStack(max_size=5)
    hash_table = HashTable()
    init_secrets(hash_table)

    display_welcome_screen()

    #menu awal Game (save / load game handling)
    current_dream = 1
    current_node = 0
    
    #cek apakah ada save file
    save_file_path = "game_data/savegame.txt"
    
    if os.path.exists(save_file_path):
        #kalau ada file tersimpan, tanya pemain
        print("  [!] Progress ingatan masa lalu terdeteksi di sistem.")
        print("  1. Lanjutkan Mimpi Jangka Pendek (Load Game)")
        print("  2. Hancurkan Ingatan Lama & Mulai Baru (New Game)")
        print("─" * 68)
        
        while True:
            pilihan = input("Pilih langkah awalmu (1/2): ")
            if pilihan == "1":
                #load game dari file
                result = journal.load_game(player, dream_vault, memory_vault)
                if result[0]:  #result = (current_dream, current_node)
                    current_dream, current_node = result
                    player.current_dream = current_dream
                    print(f"  [✓] Game dimuat. Lanjut dari Mimpi #{current_dream}.\n")
                break
            elif pilihan == "2":
                #new game, hapus save lama
                print("\nMengubur trauma lama...")
                journal.clear()  #hapus journal dan savegame.txt
                time.sleep(1)
                current_dream = 1
                current_node = 0
                break
            else:
                print("  [!] Pilihan tidak valid, coba lagi.")
    
    else:
        #tidak ada save, mulai baru
        input("  [ Tekan ENTER Untuk Memulai Permainan... ]")
<<<<<<< HEAD

    # Di dalam fungsi main() pada file main.py
    # Tambahkan parameter "target_node" yang sesuai dengan peta lokasi JSON kamu
=======
        current_dream = 1
        current_node = 0
    #alur urutan eksekusi tahapan mimpi
>>>>>>> 9788fe868ab1d1f53b0c0345946d2bbb18914eca
    dream_sequence = [
        {"file": "game_data/dialog/prologue.json", "root": "prologue", "label": "Prologue: Awakening", "target_node": None},
        {"file": "game_data/dialog/dream1.json", "root": "dream_1", "label": "Mimpi 1: The Betrayal", "target_node": "Rumah Sakit"},
        {"file": "game_data/dialog/dream2.json", "root": "dream_2", "label": "Mimpi 2: Requiem of Silence", "target_node": "Lab Komputer"},
        {"file": "game_data/dialog/dream3.json", "root": "dream_3", "label": "Mimpi 3: His Heartbeat", "target_node": "Rumah"}
    ]

    while player.current_dream <= len(dream_sequence):
        current_idx = player.current_dream - 1
        active_scene = dream_sequence[current_idx]

<<<<<<< HEAD
        # ==========================================
        # integrasi graph & DFS (eksplorasi lokasi)
        # ==========================================
=======
        #==========================================
        #integrasi graph & DFS (eksplorasi lokasi)
        #==========================================
        #panggil map eksplorasi setelah prolog selesai (Sebelum Mimpi 1 & 2)
>>>>>>> 9788fe868ab1d1f53b0c0345946d2bbb18914eca
        if active_scene["root"] != "prologue":
            clear_terminal()
            print("─" * 60)
            print(" 🧭  MEMASUKI LABIRIN MEMORI (GRAPH EXPLORATION)  🧭")
            print("─" * 60)
            print(f" [Narator]: Kamu harus mencari letak petunjuk menuju '{active_scene['target_node']}'...")
            time.sleep(2)
            
<<<<<<< HEAD
            # Panggil mesin mimpi dengan target lokasi dinamis dari scene narasi saat ini
            lokasi_awal = "Ruang Kelas"
            mesin_eksplorasi = MesinMimpi(lokasi_awal, lokasi_target=active_scene["target_node"])
            mesin_eksplorasi.mulai_mimpi()
            
            # JIKA PEMAIN KELUAR PAKSA / GAGAL
            if mesin_eksplorasi.game_selesai and mesin_eksplorasi.lokasi_sekarang != active_scene["target_node"]:
                print("\n ⚠️  Eksplorasi gagal. Jaringan memori terputus.")
                time.sleep(2)
                break 

            # JIKA BERHASIL MENCAPAI TARGET LOKASI YANG BENAR
=======
            if player.current_dream == 1:
                mesin_eksplorasi = MesinMimpi("Lab Komputer")
            elif player.current_dream == 2:
                mesin_eksplorasi = MesinMimpi("Rumah")
            elif player.current_dream == 3:
                mesin_eksplorasi = MesinMimpi("Ruang Kelas") 
            else:
                mesin_eksplorasi = MesinMimpi()
            
            #mulai navigasi Graph
            mesin_eksplorasi.mulai_mimpi()
            
            if mesin_eksplorasi.game_selesai and mesin_eksplorasi.level_mimpi < 5:
                print("\n ⚠️  Eksplorasi dihentikan secara paksa oleh pemain.")
                print(" Kesadaranmu terputus dari labirin mimpi...")
                time.sleep(2)
                break  

            #jika berhasil mencapai level 5
>>>>>>> 9788fe868ab1d1f53b0c0345946d2bbb18914eca
            clear_terminal()
            print("─" * 60)
            print(" ✨  KUNCI MEMORI DITEMUKAN! KESADARAN TERTIKAI BERHASIL MEMBUKA GERBANG  ✨")
            print("─" * 60)
            time.sleep(2)

        print(f"\n[~] Menyelami {active_scene['label']}...")
        time.sleep(1.5)

        #narasi (decision tree)
        result = execute_narrative_loop(
            file_path=active_scene["file"],
            root_key=active_scene["root"],
            player=player,
            journal=journal,
            memory_stack=memory_stack
        )
    
        #dream over
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
            print("\n")
            input("[ Tekan ENTER untuk menyusun ulang kesadaran... ]".center(80))
            continue

        #jika scene berhasil diselesaikan, simpan otomatis dan lanjut tahap berikutnya
        if result == "SCENE_COMPLETED":
            clear_terminal()
            print("─" * 60)
            print(f" 🎉   TAHAPAN {active_scene['label'].upper()} TERSURAT   🎉")
            print(" Kesadaranmu berhasil bertahan melampaui manifestasi trauma.")
            print("─" * 60)
            
            #tampilkan ringkasan memory stack jangka pendek saat ini
            memory_stack.display()
            
            player.current_dream += 1
            player.anxiety_level = 0
            #menyimpan progress real-time ke savegame.txt
            journal.save_game(player, dream_vault, memory_vault, player.current_dream, current_node)
            
            if player.current_dream <= len(dream_sequence):
                input("\n[ Tekan ENTER untuk menyelami lapisan mimpi berikutnya... ]")

    #ending Utama Permainan
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





