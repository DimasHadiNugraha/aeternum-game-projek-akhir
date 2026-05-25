#menyimpan nama, role, dan dialog tree setiap karakter
class Character:
    def __init__(self, name, role, dialogue_tree=None, description=""):
        self.name = name
        self.role = role
        self.description = description

        self.dialogue_tree = dialogue_tree
    def __str__(self):
        return f"{self.name} ({self.role})"

"""
class choice:
pilihan dialog buat player. 
setiap choice bisa: lanjut ke node berikutnya, nambah anxiety, dapetim fragment
"""
class Choice:
    def __init__(self, text, next_node=None, anxiety_change=0, fragment_reward=None):
        self.text = text
        self.next_node = next_node
        self.anxiety_change = anxiety_change
        self.fragment_reward = fragment_reward
    def __str__(self):
        return self.text
       
"""
class dialog:
dialog isinya teks, speaker dan choices.
"""
class DialogueNode:
    def __init__(self, node_id, text, speaker=None, choices=None, ending=False):
        self.text = text
        self.node_id = node_id
        self.speaker = speaker
        self.choices = choices if choices else []
        self.ending = ending

    def add_choice(self, choice): #tambahin choice baru ke node
        if isinstance(choice, Choice):
         self.choices.append(choice)

    def is_ending(self): #buat cek apaakh node ini ending
        return self.ending
    
    def display(self):
        print("\n" + "=" * 50)

        if self.speaker:
            print(f"{self.speaker}:")
            print()
        print(self.text)

        if self.ending:
            print("\n[ENDING]")

        print("=" * 50)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice.text}")

    def __str__(self):
        return f"DialogueNode({self.node_id})"
    

        