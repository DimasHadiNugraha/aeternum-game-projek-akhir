class Player:
    def __init__(self, name):
        self.name = name

        #kondisi mental
        self.anxiety_level = 0
        self.max_anxiety = 30

        #progress
        self.current_dream = 1
        self.fragments_collected = []

        #vault
        self.inventory = []
        self.memory_stack = []

        #statistik pilihan
        self.correct_choices = 0
        self.wrong_choices = 0

        #status gem
        self.is_awakened = False
        self.dream_over = False

    #fungsi buat atur tingkat kecemasan
    def increase_anxiety(self, amount):
        self.anxiety_level += amount

        if self.anxiety_level >= self.max_anxiety:
            self.dream_over = True

    #fungsi buat nambah fragment
    def add_fragment(self, fragment):
        self.fragments_collected.append(fragment)

    #fungsi tumpuk memori
    def remember(self, memory):
        self.memory_stack.append(memory)

        if len(self.memory_stack) > 5:
            self.memory_stack.pop(0)

    #reset mimpi kalau udah dream 
    def reset_dream_state(self):
        self.anxiety_level = 0
        self.dream_over = False