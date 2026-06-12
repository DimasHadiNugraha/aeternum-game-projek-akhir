from utils.vault import MemoryVault
from utils.memory_stack import MemoryStack


class Player:

    def __init__(self, name):

        self.name = name

        #kondisi mental
        self.anxiety_level = 0
        self.max_anxiety = 30

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

        self.rewind_keys = 1          #jumlah kunci pembalik waktu awal yang dimiliki player
        self.decision_history = []     #stack LIFO untuk menyimpan jejak node cerita sebelum bercabang

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

   


    #reset state mimpi
    def reset_dream_state(self):

        self.anxiety_level = 0
        self.dream_over = False

    