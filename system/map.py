import json

class PetaGame:
    def __init__(self):
        self.tempat = {}

    def tambah_jalan(self, tempat1, tempat2):
        if tempat1 not in self.tempat:
            self.tempat[tempat1] = []
        if tempat2 not in self.tempat:
            self.tempat[tempat2] = []
        if tempat2 not in self.tempat[tempat1]:
            self.tempat[tempat1].append(tempat2)
        if tempat1 not in self.tempat[tempat2]:
            self.tempat[tempat2].append(tempat1)

    def tampilkan_peta(self):
        for tempat in self.tempat:
            print(f"{tempat} -> {self.tempat[tempat]}")

def load_world():
    with open("game_data/locations.json", "r") as file:
        data = json.load(file)

    peta_game = PetaGame()

    for tempat, jalan in data["locations"].items():
        for tujuan in jalan:
            peta_game.tambah_jalan(tempat, tujuan)

    return peta_game