class Leaderboard:
    """Object which stores the top player for each gamemode"""

    def __init__(self):
        self.leaderboard = {
            "easy":       ("???", 999),
            "medium":     ("???", 999),
            "hard":       ("???", 999),
            "concentric": ("???", 000)
        }

    def create_file(self):
        pass

    def draw(self):
        easy = self.font.render('{:<12}{:<10}{}'.format(
            'Easy', self.leaderboard[0][0], self.leaderboard[0][1]), True, (255, 0, 0))
        medium = self.font.render(
            '{:<12}{:<10}{}'.format('Medium', self.leaderboard[1][0], self.leaderboard[1][1]), True, (255, 0, 0))
        hard = self.font.render('{:<12}{:<10}{}'.format(
            'Hard', self.leaderboard[2][0], self.leaderboard[2][1]), True, (255, 0, 0))
        concentric = self.font.render(
            '{:<12}{}{:>10}'.format('Concentric', self.leaderboard[3][0], ' stage ' + self.leaderboard[3][1]), True, (255, 0, 0))
        self.game_display.blit(easy, (50, 90))
        self.game_display.blit(medium, (50, 120))
        self.game_display.blit(hard, (50, 150))
        self.game_display.blit(concentric, (50, 180))

    def load(self):
        # self.leaderboard = {}
        lb_file = open('data/leader.txt')
        text = lb_file.read().split('\n')
        # for i in range(0, len(text)):
        for i, mode in enumerate(self.leaderboard):
            mode = tuple(text[i].split(','))

        lb_file.close()

    def reset(self):
        pass

    def save(self):
        text = ''
        # for i in range(0, 4):
        for mode in self.leaderboard:
            text += '{},{}\n'.format(mode[0], mode[1])
        lb_file = open('data/leader.txt', 'w')
        lb_file.write(text)
        lb_file.close()
