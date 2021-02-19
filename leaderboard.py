class Leaderboard:
    """Object which stores the top player for each gamemode"""

    def __init__(self):
        self.leaderboard = {
            "easy":       ("???", 999),
            "medium":     ("???", 999),
            "hard":       ("???", 999),
            "concentric": ("???", 000)
        }

    def load(self):
        self.leaderboard = {}
        lb_file = open('data/leader.txt')
        text = lb_file.read().split('\n')
        for i in range(0, len(text)):
            self.leaderboard[i] = text[i].split(',')

        lb_file.close()

    def create_file(self):
        pass

    def save(self):
        text = ''
        for i in range(0, 4):
            text += '{},{}\n'.format(self.leaderboard[i][0],
                                     self.leaderboard[i][1])
        lb_file = open('data/leader.txt', 'w')
        lb_file.write(text)
        lb_file.close()

    def draw(self):
        pass
