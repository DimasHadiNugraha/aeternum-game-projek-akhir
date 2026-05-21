class Fragment:
    def __init__(self, fragment_id, name, description):
        self.fragment_id = fragment_id
        self.name = name
        self.description = description

class EmotionFragment(Fragment):
    def __init__(self, fragment_id, name, emotion_type, value, description):
        super().__init__(fragment_id, name, description)

        self.emotion_type = emotion_type
        self.value = value

class MemoryFragment(Fragment):
    def __init__(self, fragment_id, title, memory_piece, description):
        super().__init__(fragment_id, title, description)

        self.memory_piece = memory_piece