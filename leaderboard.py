class Leaderboard:
    """Object which stores the top player for each gamemode"""

    def __init__(self, parent):
        self.parent = parent
        self.default_leaderboard = {
            "easy":       ("???", "999"),
            "medium":     ("???", "999"),
            "hard":       ("???", "999"),
            "concentric": ("???", "000")
        }
        self.leaderboard = self.default_leaderboard.copy()

    def draw(self):
        easy = self.parent.font.render('{:<12}{:<10}{}'.format(
            'Easy', self.leaderboard["easy"][0], self.leaderboard["easy"][1]), True, (255, 0, 0))
        medium = self.parent.font.render(
            '{:<12}{:<10}{}'.format('Medium', self.leaderboard["medium"][0], self.leaderboard["medium"][1]), True, (255, 0, 0))
        hard = self.parent.font.render('{:<12}{:<10}{}'.format(
            'Hard', self.leaderboard["hard"][0], self.leaderboard["hard"][1]), True, (255, 0, 0))
        concentric = self.parent.font.render(
            '{:<12}{}{:>10}'.format('Concentric', self.leaderboard["concentric"][0], ' stage ' + str(self.leaderboard["concentric"][1])), True, (255, 0, 0))
        self.parent.game_display.blit(easy, (50, 90))
        self.parent.game_display.blit(medium, (50, 120))
        self.parent.game_display.blit(hard, (50, 150))
        self.parent.game_display.blit(concentric, (50, 180))

    def load(self):
        try:
            lb_file = open('data/leader.txt')
            text = lb_file.read().split('\n')
            for i, mode in enumerate(self.leaderboard):
                self.leaderboard[mode] = tuple(text[i].split(','))

            lb_file.close()
        except FileNotFoundError:
            self.reset()

    def update(self, gamemode, name, value):
        #current_value = self.leaderboard[gamemode.lower()][1]
        # if int(value) > current_value:
        self.leaderboard[gamemode.lower()] = (name, value)
        self.save()

    def reset(self):
        self.leaderboard = self.default_leaderboard.copy()
        self.save()

    def save(self):
        text = ''
        for mode in self.leaderboard.values():
            text += '{},{}\n'.format(mode[0], mode[1])
        lb_file = open('data/leader.txt', 'w')
        lb_file.write(text)
        lb_file.close()
