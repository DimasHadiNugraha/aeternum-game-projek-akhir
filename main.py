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
    clear_terminal()
    print("""
 █████╗ ███████╗████████╗███████╗██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║████╗ ████║
███████║█████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║██║   ██║██╔████╔██║
██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██║╚██╔╝██║
██║  ██║███████╗   ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
    """)
    print("                 ✦ FRAGMENTS OF THE LUCID MIND 1.0 ✦        ")
    print("                      ⋆｡°✩ ───────────── ✩°｡⋆")
    print("  la bienvenue, Aeterie! Ayo mulai berkelana di dunia Aeternum✧")
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
        print("│" + "▶ NOTIFICATION".center(lebar_notif - 1) + " │")
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

def execute_narrative_loop(file_path, root_key, player, journal, start_node=None):
    """Membaca data narasi JSON dan mengeksekusi pohon keputusan dialog."""
    if not os.path.exists(file_path):
        print(f"[!] File data narasi {file_path} tidak ditemukan!")
        return False

    with open(file_path, "r") as f:
        story_data = json.load(f)

    scene = story_data[root_key]
    current_node_id = start_node if start_node is not None else scene["start_node"]
    nodes = scene["nodes"]

    while current_node_id is not None:
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
            return ("DREAM_OVER", current_node_id)

        speaker = node.get("speaker")
        if speaker:
            spk_name = player.name if speaker == "player" else speaker
            print(f"✧━━━『 [{spk_name.upper()}] 』━━━✧")
        else:
            print("✧━━━『 [NARRATOR] 』━━━✧")
        

        for line in node.get("text", []):
            if "{player_name}" in line:
                line = line.replace("{player_name}", player.name)
            typewriter(line, speed=0.01)
            time.sleep(0.2)
        print("─" * 60 + "\n")

        if node.get("ending") is False and speaker == "player":
            last_text = node.get("text", [""])[0]
            player.memory_stack.push(last_text)
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

    return ("SCENE_COMPLETED", current_node_id)

#============================
#4.GAME MAIN CONTROL CENTER
#============================

def main():
    #inisialisasi objek dasar player (nama default sebelum diinput)
    player = Player(name="Aeterie")
    player.fragment_count = 0 
    
    #menyiapkan instansiasi struktur data
    journal = DreamJournal()
    hash_table = HashTable()
    init_secrets(hash_table)

    display_welcome_screen()

    #menu awal Game (save / load game handling)
    current_dream = 1
    current_node = None
    
    #cek apakah ada save file
    save_file_path = "game_data/savegame.txt"
    
    if os.path.exists(save_file_path):
        #kalau ada file tersimpan, tanya pemain
        print("  [ ⧗ ] Progress ingatan masa lalu terdeteksi di sistem.")
        print("  ▶ Lanjutkan Mimpi - Continue (1)")
        print("  ▷ Mulai Mimpi Baru - New Game (2)")
        print("─" * 68)
        
        while True:
            pilihan = input("Pilih langkah awalmu (1/2): ")
            if pilihan == "1":
                #load game dari file
                result = journal.load_game(
                    player,
                    player.dream_vault,
                    player.memory_vault
                )
                if result:
                    current_dream, current_node = result
                    player.current_dream = current_dream  #result = (current_dream, current_node)
                    print(f"  [✓] Game dimuat. Lanjut dari Mimpi #{current_dream}.\n")
                break
            elif pilihan == "2":
                #new game, hapus save lama
                print("\nMengubur trauma lama...")
                journal.clear()  #hapus journal dan savegame.txt
                time.sleep(1)
                current_dream = 1
                current_node = None
                break
            else:
                print("  [!] Pilihan tidak valid, coba lagi.")
    
    else:
        #tidak ada save, mulai baru
        input("  [ Tekan ENTER Untuk Memulai Permainan... ]")

        current_dream = 1
        current_node = 0
    #alur urutan eksekusi tahapan mimpi
    dream_sequence = [
        {"file": "game_data/dialog/prologue.json", "root": "prologue", "label": "Prologue: Awakening", "target_node": None},
        {"file": "game_data/dialog/dream1.json", "root": "dream_1", "label": "Mimpi 1: The Betrayal", "target_node": "Lab Komputer"},
        {"file": "game_data/dialog/dream2.json", "root": "dream_2", "label": "Mimpi 2: Requiem of Silence", "target_node": "Rumah"},
        {"file": "game_data/dialog/dream3.json", "root": "dream_3", "label": "Mimpi 3: His Heartbeat", "target_node": "Ruang Kelas"}
    ]

    while player.current_dream <= len(dream_sequence):
        current_idx = player.current_dream - 1
        active_scene = dream_sequence[current_idx]

        #==========================================
      # ==========================================
        # INTEGRASI GRAPH & DFS (EKSPLORASI LOKASI) - FIXED
        # ==========================================
        if active_scene["root"] != "prologue":
            clear_terminal()
            print("─" * 60)
            print("    ◈ MEMASUKI LABIRIN MEMORI (DREAM EXPLORATION) ◈")
            print("✦・┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈・✦")
            print(f" [Narator]: Kamu harus mencari letak mimpi selanjutnya. Petunjuk: '{active_scene['target_node']}'...")
            time.sleep(2)
            
            #tentukan lokasi awal berdasarkan mimpi saat ini 
            lokasi_awal = "Rumah"
            if player.current_dream == 2:
                lokasi_awal = "Ruang Kelas"
            elif player.current_dream == 3:
                lokasi_awal = "Lab Komputer"
            else:
                lokasi_awal = "Rumah"



            #inisialisasi & jalankan 
            mesin_eksplorasi = MesinMimpi(lokasi_awal, lokasi_target=active_scene["target_node"])
            mesin_eksplorasi.mulai_mimpi()
            
            #validasi Hasil Eksplorasi
            #cek apakah pemain keluar paksa atau gagal mencapai target node
            if mesin_eksplorasi.game_selesai:
                if mesin_eksplorasi.lokasi_sekarang != active_scene["target_node"]:
                    print("\n !!  Eksplorasi gagal / dihentikan. Jaringan memori terputus.")
                    time.sleep(2)
                    break  #keluar dari game karena gagal
            
            clear_terminal()
            print(" ｡⋆୨୧˚   KUNCI MEMORI DITEMUKAN! MEMBUKA GERBANG MIMPI BERIKUTNYA...")
            print(" ──────────────────────────────────────────────────────────────────── ☾")
            time.sleep(2)

        print(f"\n[~] Menyelami {active_scene['label']}...")
        time.sleep(1.5)

        #narasi (decision tree)
        result, current_node  = execute_narrative_loop(
            file_path=active_scene["file"],
            root_key=active_scene["root"],
            player=player,
            journal=journal,
            start_node=current_node
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
                                                                                 
                                                                                 
            """
           
            print("\n" * 2)
            for line in ascii_art.strip().split('\n'):
                print(line.center(80))
            
            print("\n")
            print("💀 KESADARAN ANDA HANCUR (DREAM OVER) 💀".center(80))
            print("Anxiety Level mencapai batas puncak pertahanan mental.".center(80))
            print("Jiwamu terlempar kembali ke awal lapisan mimpi ini...".center(80))
            print("\n")
            print("═" * 80)
            
            player.reset_dream_state()
            journal.save_game(
                player,
                player.dream_vault,
                player.memory_vault,
                player.current_dream,
                current_node
            ) 
            print("\n")
            input("[ Tekan ENTER untuk menyusun ulang kesadaran... ]".center(80))
            continue

       #jika scene berhasil diselesaikan, simpan otomatis dan lanjut tahap berikutnya
        if result == "SCENE_COMPLETED":
            clear_terminal()
            
            #hitung data untuk rekapan
            total_fragments = player.dream_vault.size + player.memory_vault.size
            sisa_anxiety = player.max_anxiety - player.anxiety_level
            sisa_rewind = getattr(player, 'rewind_keys', 0) #mencegah error kalau rewind_keys belum di-set
            
            #menentukan status kondisi jiwa berdasarkan anxiety
            if player.anxiety_level < (player.max_anxiety * 0.3):
                kondisi_jiwa = "Sangat Stabil"
            elif player.anxiety_level < (player.max_anxiety * 0.7):
                kondisi_jiwa = "Sedikit Terguncang"
            else:
                kondisi_jiwa = "Kritis"

            #ui nya
            print("╔" + "═" * 67 + "╗")
            print("║" + f"✧ TAHAPAN {active_scene['label'].upper()} ✧".center(67) + "║")
            print("╚" + "═" * 67 + "╝\n")
            
            print('    "Satu kepingan memori kembali, menyisakan ruang hampa')
            print('     di kepalamu yang kini perlahan mulai terisi..."\n')
            
            print("  ┌─ ⋆ STATUS KESADARAN ⋆ " + "─" * 42 + "┐")
            print("  │" + " " * 67 + "│")
            print(f"  │  ▸ Kondisi Jiwa    : {kondisi_jiwa} (Sisa Toleransi: {sisa_anxiety})".ljust(69) + "│")
            print(f"  │  ▸ Total Fragment  : {total_fragments} Terkumpul".ljust(69) + "│")
            print(f"  │  ▸ Sisa Rewind Key : {sisa_rewind}".ljust(69) + "│")
            print("  │" + " " * 67 + "│")
            print("  └" + "─" * 67 + "┘\n")
            
            print("  Meringkas Stack Memori Jangka Pendek...")
            print("  [!] Terhubung ke Buku Harian (Dream Journal).\n")
            time.sleep(1.5) 
            
            # Tampilkan ringkasan memory stack jangka pendek saat ini
            player.memory_stack.display()
            
            #reset dan update state game
            player.current_dream += 1
            current_node = None
            player.anxiety_level = 0 #anxiety direset setiap masuk mimpi baru
            
            #menyimpan progress real time ke savegame.txt
            journal.save_game(
                player,
                player.dream_vault,
                player.memory_vault,
                player.current_dream,
                current_node
            )
            
            if player.current_dream <= len(dream_sequence):
                input("\n[ Tekan ENTER untuk menyelami lapisan mimpi berikutnya... ]")

        #================
    #5.ENDING UTAMA
    #================
    clear_terminal()
    time.sleep(1.0)

    typewriter(" . . .", speed=0.3)
    time.sleep(1.0)

    typewriter(f" [ Kesadaran ]: Sinkronisasi selesai. Kamu telah terbangun dari dunia Aeternum.", speed=0.03)
    time.sleep(0.8)
    typewriter(f" [ Memori ]: Seluruh fragment memori telah disimpan.", speed=0.03)
    time.sleep(0.8)

    print("\n" + "─" * 40)
    time.sleep(1.0)

    narasi_silent = [
        f"Kamu terbangun di kamarmu, dan kali ini... bukan mimpi.",
        f"Rasa cemas yang mencekikmu sepanjang malam... kini menguap.",
        f"Kamu melihat ke setiap sudut kamar, namun tidak dapat menemukan",
        f"keberadaan Lumiere. Perhatianmu teralih pada brace ditanganmu.",
        f"Tidak ada yang berubah, cederamu masih permanen. Karena semua",
        f"mimpi itu pada akhirnya hanya rekaan ingatanmu dan tidak bisa mengubah",
        f"kenyataan.",
        f"Selamat, {player.name}. Kamu berhasil melawan rasa takutmu untuk",
        f"menghadapi trauma yang sudah dikubur."
    ]

    for baris in narasi_silent:
        typewriter(baris, speed=0.04)
        time.sleep(0.8)

    print("\n" + "─" * 40 + "\n")
    input("[ Tekan ENTER untuk membaca sisa ingatanmu ]")

    #================
    # DREAM JOURNAL
    #================
    clear_terminal()

    print("✦ A E T E R N U M  |  D R E A M   J O U R N A L")
    print(f"Subjek: {player.name}  |  Status: Terbangun Seutuhnya")
    print("=" * 60)
    print(" Catatan yang berhasil diselamatkan dari alam bawah sadar:\n")

    journal.display()

    print("\n" + "=" * 60)

    #================
    # TRUE ENDING
    #================

    time.sleep(1)

    print("""
════════════════════════════════════════════════════════════

                    ✦ TRUE ENDING ✦

                  ☾ Fragment Recovered ☽
                          COMPLETE

                   ✦ Anxiety Conquered ✦
                          SUCCESS

════════════════════════════════════════════════════════════

        "Every dream must end,
         so that a new day can begin."

════════════════════════════════════════════════════════════
""")

    input("[ Tekan ENTER untuk melanjutkan ]")

    #================
    # THANK YOU SCREEN
    #================

    clear_terminal()

    print(r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                     A E T E R N U M                      ║
║                                                          ║
║              The dream has finally ended.               ║
║                                                          ║
║                  Thank you for playing.                 ║
║                                                          ║
║                        ☾ ✦ ☾                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    time.sleep(1)

    #================
    # ULASAN PEMAIN
    #================

    print("\n" + "═" * 60)
    print("                    🌙 U L A S A N 🌙")
    print("═" * 60)

    print("\nTerima kasih telah memainkan Aeternum!")
    print("Beri penilaianmu terhadap pengalaman bermain.\n")

    while True:
        try:
            rating = int(input("⭐ Rating (1 - 10): "))

            if 1 <= rating <= 10:
                break

            print("Masukkan angka antara 1 sampai 10.")

        except ValueError:
            print("Masukkan angka yang valid.")

    print()

    komentar = input("💭 Komentar : ")

    #================
    # SIMPAN ULASAN
    #================

    with open("ulasan_game.txt", "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("═" * 60 + "\n")
        file.write(f"Pemain   : {player.name}\n")
        file.write(f"Rating   : {rating}/10\n")
        file.write(f"Komentar : {komentar}\n")
        file.write("═" * 60 + "\n")

    print("\n")

    typewriter("✦ Menyimpan ulasan ke Memory Archive...", speed=0.03)

    time.sleep(1)

    print("✓ Rating berhasil disimpan")
    print("✓ Komentar berhasil disimpan")

    time.sleep(1)

    print("""
════════════════════════════════════════════════════════════

              Terima kasih atas perjalananmu.

                        ☾ ✦ ☾

════════════════════════════════════════════════════════════
""")

    input("[ Tekan ENTER untuk keluar dari Aeternum ]")

if __name__ == "__main__":
    main()





