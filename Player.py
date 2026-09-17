
class Player:

    def __init__(self, name):
        self.score = 0
        self.name = name
        self.id = None

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score
