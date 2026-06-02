from utils.vault import MemoryVault
from utils.memory_stack import MemoryStack


class Player:

    def __init__(self, name):

        self.name = name

        #kondisi mental
        self.anxiety_level = 0
        self.max_anxiety = 75

        #progress game
        self.current_dream = 1

        #vault player
        self.memory_vault = MemoryVault("Memory Vault")
        self.dream_vault = MemoryVault("Dream Vault")

        #stack ingatan jangka pendek
        self.memory_stack = MemoryStack(max_size=5)

        #statistik pilihan player
        self.correct_choices = 0
        self.wrong_choices = 0

        #status game
        self.is_awakened = False
        self.dream_over = False

    #tambah anxiety
    def increase_anxiety(self, amount):

        self.anxiety_level += amount

        #batasin anxiety maksimal
        if self.anxiety_level > self.max_anxiety:
            self.anxiety_level = self.max_anxiety

        #kalau anxiety penuh langsung dream over
        if self.anxiety_level >= self.max_anxiety:
            self.dream_over = True

    #kurangin anxiety
    def decrease_anxiety(self, amount):

        self.anxiety_level -= amount

        #anxiety tidak boleh minus
        if self.anxiety_level < 0:
            self.anxiety_level = 0

    #simpan memory ke stack
    def remember(self, memory):

        self.memory_stack.push(memory)

    #tambah fragment ke vault
    def add_fragment(self, fragment):

        #fragment emosi di dream vault
        if fragment.fragment_type == "emotion":

            self.dream_vault.add_item(
                fragment.name,
                "emotion_fragment",
                fragment.description,
                fragment.value
            )

        #fragment memori di memory vault
        elif fragment.fragment_type == "memory":

            self.memory_vault.add_item(
                fragment.name,
                "memory_fragment",
                fragment.description,
                fragment.value
            )

    #tambah statistik pilihan benar
    def add_correct_choice(self):

        self.correct_choices += 1

    #tambah statistik pilihan salah
    def add_wrong_choice(self):

        self.wrong_choices += 1

    #reset state mimpi
    def reset_dream_state(self):

        self.anxiety_level = 0
        self.dream_over = False

    #cek apakah player overwhelm
    def is_overwhelmed(self):

        return self.anxiety_level >= self.max_anxiety

    #tampilkan status player
    def display_status(self):

        print("\n" + "=" * 40)
        print("        ✦ PLAYER STATUS ✦")
        print("=" * 40)

        print(f"Nama              : {self.name}")
        print(f"Dream Saat Ini    : {self.current_dream}")
        print(f"Anxiety Level     : {self.anxiety_level}/{self.max_anxiety}")
        print(f"Pilihan Benar     : {self.correct_choices}")
        print(f"Pilihan Salah     : {self.wrong_choices}")

        print("=" * 40 + "\n")