class Character:
    def __init__(self, name, role, dialogue_tree):
        self.name = name
        self.role = role
        self.dialogue_tree = dialogue_tree

lumiere = Character(
    "Lumiere",
    "Guide",
    {}
)

class Choice:
    def __init__(self, text, next_node, anxiety_change=0, fragment_reward=0):
        self.text = text
        self.next_node = next_node
        self.anxiety_change = anxiety_change
        self.fragment_reward = fragment_reward

class DialogueNode:
    def __init__(self, text, choices=None, ending=False):
        self.text = text
        self.choices = choices if choices else []
        self.ending = ending

        