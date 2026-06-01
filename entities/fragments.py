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
    def __init__(self, fragment_id, name, value, description):
        super().__init__(fragment_id, name, description)

        self.fragment_type = "memory"
        self.value = value

    def display(self):
        print(f"\n[{self.fragment_type.upper()} FRAGMENT]")
        print(f"Nama : {self.name}")
        print(f"Deskripsi : {self.description}")

MEMORY_FRAGMENTS = {
    "memory_fragment_001": MemoryFragment(
        "memory_fragment_001",
        "First Source Code",
        1,
        "Kamu mengingat bagaimana semuanya dimulai."
    ),

    "memory_fragment_002": MemoryFragment(
        "memory_fragment_002",
        "Empty Classroom",
        1,
        "Sebuah tempat yang pernah menjadi rumah kedua."
    ),

    "memory_fragment_003": MemoryFragment(
        "memory_fragment_003",
        "False Accusation",
        1,
        "Awal dari runtuhnya kepercayaan."
    )
}

EMOTION_FRAGMENTS = {
    "fragment_001": EmotionFragment(
        "fragment_001",
        "A Piece in Dissaray",
        "Anxiety",
        7,
        "Obat yang berantakkan... siapa yang sakit?"
    ),

    "fragment_002": EmotionFragment(
        "fragment_002",
        "The Same Headline",
        "Anxiety",
        7,
        "Siaran televisi yang berulang-ulang, memuakkan."
    ),

    "fragment_003": EmotionFragment(
        "fragment_003",
        "Crimson Scene",
        "Fear",
        3,
        "Kenapa ruangan ini dipenuhi darah? Menyeramkan sekali"
    ),

    "fragment_004": EmotionFragment(
        "fragment_004",
        "Obscured Visage",
        "Confused",
        5,
        "Wajahnya tidak kelihatan, tapi terasa familiar."
    ),

    "fragment_005": EmotionFragment(
        "fragment_005",
        "Burning Glaze",
        "Fear",
        3,
        "Tatapan mereka sangat tajam dan menyeramkan, aku ingi pergi dari sini."
    ),

    "fragment_006": EmotionFragment(
        "fragment_006",
        "The Written Walls",
        "Anxiety",
        3,
        "Coretan penuh makian, apa ini ditujukan kepadaku?"
    ),

    "fragment_007": EmotionFragment(
        "fragment_007",
        "Unforgotten Name",
        "Confused",
        5,
        "Namanya terasa tidak asing, seolah aku sudah menyebutnya ribuan kali."
    ),

    "fragment_d1_001": EmotionFragment(
        "fragment_d1_001",
        "A Masterpiece in Progress",
        "Amazed",
        5,
        "Projek ini keren sekali... apa aku yang membuatnya?"
    ),

    "fragment_d1_002": EmotionFragment(
        "fragment_d2_002",
        "An Endearing Voice",
        "Happy",
        7,
        "Dia memanggilku sahabat... hatiku terasa hangat."
    ),

    "fragment_d1_003": EmotionFragment(
        "fragment_d1_003",
        "Disordered Syntax",
        "Anxiety",
        3,
        "Berantakkan sekali."
    ),

    "fragment_d1_004": EmotionFragment(
        "fragment_d1_004",
        "The One Who Owned It",
        "Grateful",
        3,
        "Ini milikku..."
    ),

    "fragment_d1_005": EmotionFragment(
        "fragment_d1_005",
        "Recorded Time",
        "Confused",
        3,
        "..."
    ),

    "fragment_d1_006": EmotionFragment(
        "fragment_d1_006",
        "Recorded Conversation",
        "Anxiety",
        5,
        "Sejak kapan ini direkam, ya?"
    ),

    "fragment_d1_007": EmotionFragment(
        "fragment_d1_007",
        "Fragments Recovered",
        "Happy",
        7,
        "Langkah kecil ini ternyata membuahkan hasil! "
    )


}

