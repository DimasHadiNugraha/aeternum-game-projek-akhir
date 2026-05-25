class Fragment:
    def __init__(self, fragment_id, name, description):
        self.fragment_id = fragment_id
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class EmotionFragment(Fragment):
    def __init__(self, fragment_id, name, emotion_type, value, description):
        super().__init__(fragment_id, name, description)

        self.fragment_type = "emotion"
        self.emotion_type = emotion_type
        self.value = value

class MemoryFragment(Fragment):
    def __init__(self, fragment_id, name, memory_piece, value, description):
        super().__init__(fragment_id, name, description)

        self.fragment_type = "memory"
        self.memory_piece = memory_piece
        self.value = value

    def display(self):
        print(f"\n[{self.fragment_type.upper()} FRAGMENT]")
        print(f"Nama : {self.name}")
        print(f"Deskripsi : {self.description}")

