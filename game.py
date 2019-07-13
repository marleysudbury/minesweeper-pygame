# Pygame remake of my old Minesweeper clone
# Same assets and mostly the same logic
# (c) Marley Sudbury 2019

import pygame
import random
import time
from tile import Tile
from counter import Counter


class Game:
    """The game class."""
    def __init__(self):
        """Initialises game objects."""
        self.TILE_SIZE = 21
        self.game_state = "MENU"
        self.game_mode = "EASY"
        self.W_WIDTH = 600
        self.W_HEIGHT = 500
        self.stop = False

        self.images = {}
        self.load_images()
        self.background = self.images["PLAY"]

        self.cols = 0
        self.rows = 0
        self.mines = 0
        self.grid_x = 0
        self.grid_y = 0
        self.tiles = []
        self.timer = False
        self.start = False
        self.start_time = 0
        self.time = Counter(30, 15, 0, 0, 0)
        self.mine_left = Counter(30 + (15 * 5), 15, 0, 0, 0)

        self.won = False
        self.lost = False

        pygame.init()
        self.game_display = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))
        pygame.display.set_caption("Minesweeper by Marley")

    def loop(self):
        """The game loop."""
        while not self.stop:
            self.handle_events()
            pos = pygame.mouse.get_pos()
            if self.game_state == "MENU":
                if pos[0] > 300:
                    if pos[1] < 190:
                        self.background = self.images["PLAY"]
                    elif 190 <= pos[1] < 230:
                        self.background = self.images["STORY"]
                    elif 230 <= pos[1] < 275:
                        self.background = self.images["OPTIONS"]
                    elif 275 <= pos[1]:
                        self.background = self.images["LEADERBOARD"]
            elif self.game_state == "PLAY":
                if pos[1] < 187:
                    self.background = self.images["GAME_1"]
                elif 187 <= pos[1] < 230:
                    self.background = self.images["GAME_2"]
                elif 230 <= pos[1] < 274:
                    self.background = self.images["GAME_3"]
                elif 274 <= pos[1] < 316:
                    self.background = self.images["GAME_4"]
                else:
                    self.background = self.images["GAME_5"]
            elif self.game_state == "PLAYING":
                current_time = time.time()
                # print("Start time: {}\nCurrent time: {}\nDif: {}\nTimer: {}".format(self.start_time, current_time, current_time-self.start_time, self.timer))
                if current_time - self.start_time >= 1 and self.timer:
                    # print("ACTIVATE")
                    self.start_time = current_time
                    self.time.increment()
                self.background = self.images["GAME_BG"]
            elif self.game_state == "STORY":
                self.background = self.images["STORY_SCREEN"]

            # Draw
            self.game_display.blit(self.background, (0, 0))
            if self.game_state == "PLAYING":
                self.display_tiles()
                self.display_counters()
                if self.lost:
                    self.game_display.blit(self.images["LOSE"], (0, 0))
                elif self.won:
                    self.game_display.blit(self.images["WIN"], (0, 0))
            pygame.display.update()
        pygame.quit()
        quit()

    def win(self):
        self.won = True
        self.timer = False
        for row in self.tiles:
            for tile in row:
                if tile.covered and not tile.mine:
                    tile.covered = False

    def lose(self):
        self.lost = True
        self.timer = False
        for row in self.tiles:
            for tile in row:
                if tile.mine and tile.covered:
                    tile.covered = False

    def clearing(self, t):
        (i, j) = t
        if i == 0 and j == 0:
            # Top left
            adjacent = [(i, j+1), (i+1, j+1), (i+1, j)]
        elif i == 0 and j == self.cols - 1:
            # Top right
            adjacent = [(i, j-1),
                        (i+1, j-1), (i+1, j)]
        elif i == self.rows - 1 and j == 0:
            # Bottom left
            adjacent = [(i-1, j), (i-1, j+1),
                                  (i, j+1)]
        elif i == self.rows - 1 and j == self.cols - 1:
            # Bottom right
            adjacent = [(i-1, j-1), (i-1, j),
                        (i, j-1)]
        elif i == 0:
            # Top row
            adjacent = [(i, j-1), (i, j+1),
                        (i+1, j-1), (i+1, j), (i+1, j+1)]
        elif i == self.rows - 1:
            # Bottom row
            adjacent = [(i-1, j-1), (i-1, j), (i-1, j+1),
                        (i, j-1), (i, j+1)]
        elif j == 0:
            # Left column
            adjacent = [(i-1, j), (i-1, j+1),
                                  (i, j+1),
                        (i+1, j), (i+1, j+1)]
        elif j == self.cols - 1:
            # Right column
            adjacent = [(i-1, j-1), (i-1, j),
                        (i, j-1),
                        (i+1, j-1), (i+1, j)]
        else:
            # Otherwise
            adjacent = [(i-1, j-1), (i-1, j), (i-1, j+1),
                        (i, j-1), (i, j+1),
                        (i+1, j-1), (i+1, j), (i+1, j+1)]

        if self.tiles[i][j].adj == 0:
            for x in range(0, len(adjacent)):
                n_t = adjacent[x]
                if self.tiles[n_t[0]][n_t[1]].covered:
                    self.tiles[n_t[0]][n_t[1]].covered = False
                    self.clearing(n_t)

    def display_tiles(self):
        for row in self.tiles:
            for tile in row:
                if tile.flagged:
                    sprite = self.images["FLAGGED"]
                elif tile.covered and not self.won:
                    sprite = self.images["COVERED"]
                elif tile.exploded:
                    sprite = self.images["EXPLODED"]
                elif tile.mine:
                    sprite = self.images["MINE"]
                elif tile.adj > 0:
                    sprite = self.images["T_" + str(tile.adj)]
                else:
                    sprite = self.images["UNCOVERED"]

                self.game_display.blit(sprite, (tile.x, tile.y))

    def display_counters(self):
        # Time counter
        num = self.time.num_1
        x = self.time.x
        y = self.time.y
        self.game_display.blit(self.images[num], (x, y))

        num = self.time.num_2
        x = self.time.x + 15
        y = self.time.y
        self.game_display.blit(self.images[num], (x, y))

        num = self.time.num_3
        x = self.time.x + 30
        y = self.time.y
        self.game_display.blit(self.images[num], (x, y))

        # Mine counter
        num = self.mine_left.num_1
        x = self.mine_left.x
        y = self.mine_left.y
        self.game_display.blit(self.images[num], (x, y))

        num = self.mine_left.num_2
        x = self.mine_left.x + 15
        y = self.mine_left.y
        self.game_display.blit(self.images[num], (x, y))

        num = self.mine_left.num_3
        x = self.mine_left.x + 30
        y = self.mine_left.y
        self.game_display.blit(self.images[num], (x, y))

    def start_game(self):
        if self.game_mode == "EASY":
            self.rows = 9
            self.cols = 9
            self.mines = 10
        elif self.game_mode == "MEDIUM":
            self.rows = 16
            self.cols = 16
            self.mines = 40
        elif self.game_mode == "HARD":
            self.rows = 20
            self.cols = 27
            self.mines = 101

        self.mine_left.set_val(self.mines)

        self.grid_x = (self.W_WIDTH / 2) - ((self.cols * self.TILE_SIZE)/2)
        self.grid_y = (self.W_HEIGHT / 2) - ((self.rows * self.TILE_SIZE)/2) + 28

        self.tiles = []

        for i in range(0, self.rows):
            new_row = []
            for j in range(0, self.cols):
                new_row.append(Tile(self.grid_x + (self.TILE_SIZE * j), self.grid_y + (self.TILE_SIZE * i)))
            self.tiles.append(new_row)

    def click_grid(self, type):
        pos = pygame.mouse.get_pos()
        if self.tiles[0][0].x <= pos[0] <= self.tiles[0][self.cols-1].x + self.TILE_SIZE and self.tiles[0][0].y <= pos[1] <= self.tiles[self.rows-1][self.cols-1].y + self.TILE_SIZE:
            # User has clicked inside tile grid
            the_tile = None
            tuple_cov = (0, 0)
            for i in range(0, len(self.tiles)):
                for j in range(0, len(self.tiles[i])):
                    tile = self.tiles[i][j]
                    if tile.x <= pos[0] <= tile.x + self.TILE_SIZE and tile.y <= pos[1] <= tile.y + self.TILE_SIZE:
                        the_tile = tile
                        tuple_cov = (i, j)

            if self.start:
                (i, j) = tuple_cov
                self.place_mines(i, j)
                self.count_adjacent()
                self.start = False
                self.timer = True
                self.start_time = time.time()
            if type == 1:
                # Uncover tile if not flagged
                if not the_tile.flagged:
                    the_tile.covered = False
                    if the_tile.mine:
                        the_tile.exploded = True
                        self.lose()
                    else:
                        self.clearing(tuple_cov)
            else:
                # Toggle flag (unless it is already uncovered)
                if the_tile.covered:
                    # the_tile.flagged = not the_tile.flagged
                    if the_tile.flagged:
                        the_tile.flagged = False
                        self.mine_left.increment()
                    else:
                        the_tile.flagged = True
                        self.mine_left.decrement()
                        if self.mine_left.get_val() == 0:
                            correct = True
                            for row in self.tiles:
                                for tile in row:
                                    if tile.mine and not tile.flagged or not tile.mine and tile.flagged:
                                        correct = False
                            if correct:
                                self.win()

    def place_mines(self, i, j):
        mine_to_place = self.mines
        while mine_to_place > 0:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
            if not self.tiles[row][col].mine and row != i and col != j:
                self.tiles[row][col].mine = True
                mine_to_place -= 1

    def count_adjacent(self):
        for i in range(0, len(self.tiles)):
            for j in range(0, len(self.tiles[i])):
                this_tile = self.tiles[i][j]
                if i == 0 and j == 0:
                    # Top left corner
                    this_tile.adj += self.check_neighbour(i, j, [4, 5, 6])
                elif i == 0 and j == self.cols - 1:
                    this_tile.adj += self.check_neighbour(i, j, [6, 7, 8])
                elif i == self.rows - 1 and j == 0:
                    this_tile.adj += self.check_neighbour(i, j, [2, 3, 4])
                elif i == self.rows - 1 and j == self.cols - 1:
                    this_tile.adj += self.check_neighbour(i, j, [1, 2, 8])
                elif i == 0:
                    this_tile.adj += self.check_neighbour(i, j, [4, 5, 6, 7, 8])
                elif i == self.rows - 1:
                    this_tile.adj += self.check_neighbour(i, j, [1, 2, 3, 4, 8])
                elif j == 0:
                    this_tile.adj += self.check_neighbour(i, j, [2, 3, 4, 5, 6])
                elif j == self.cols - 1:
                    this_tile.adj += self.check_neighbour(i, j, [1, 2, 6, 7, 8])
                else:
                    this_tile.adj += self.check_neighbour(i, j)

    def check_neighbour(self, i, j, n=[1, 2, 3, 4, 5, 6, 7, 8]):
        # 1 to 8 clockwise from top left to left
        total = 0
        if 1 in n and self.tiles[i-1][j-1].mine:
            total += 1
        if 2 in n and self.tiles[i-1][j].mine:
            total += 1
        if 3 in n and self.tiles[i-1][j+1].mine:
            total += 1
        if 4 in n and self.tiles[i][j+1].mine:
            total += 1
        if 5 in n and self.tiles[i+1][j+1].mine:
            total += 1
        if 6 in n and self.tiles[i+1][j].mine:
            total += 1
        if 7 in n and self.tiles[i+1][j-1].mine:
            total += 1
        if 8 in n and self.tiles[i][j-1].mine:
            total += 1
        return total

    def handle_events(self):
        """Handles events since the last loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # The bastards done a click
                if self.game_state == "MENU":
                    # The user has clicked in the menu!
                    if self.background == self.images["PLAY"]:
                        self.game_state = "PLAY"
                    elif self.background == self.images["STORY"]:
                        self.game_state = "STORY"
                    elif self.background == self.images["OPTIONS"]:
                        self.game_state = "OPTIONS"
                    else:
                        self.game_state = "LEADERBOARD"
                elif self.game_state == "PLAY":
                    if self.background == self.images["GAME_1"]:
                        self.game_mode = "EASY"
                    elif self.background == self.images["GAME_2"]:
                        self.game_mode = "MEDIUM"
                    elif self.background == self.images["GAME_3"]:
                        self.game_mode = "HARD"
                    else:
                        self.game_mode = "CUSTOM"
                    self.game_state = "PLAYING"
                    self.start = True
                    self.start_game()
                elif self.game_state == "PLAYING":
                    self.click_grid(event.button)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "MENU":
                        self.stop = True
                    elif self.game_state == "PLAYING":
                        self.timer = False
                        self.lost = False
                        self.won = False
                        self.time.set_val(0)
                        self.game_state = "PLAY"
                    else:
                        self.game_state = "MENU"

    def load_images(self):
        """Loads all images for the game."""
        # Menu options
        self.images["PLAY"] = pygame.image.load("data/play.png")
        self.images["STORY"] = pygame.image.load("data/story.png")
        self.images["OPTIONS"] = pygame.image.load("data/options.png")
        self.images["LEADERBOARD"] = pygame.image.load("data/leaderboard.png")

        # Game type selection
        self.images["GAME_1"] = pygame.image.load("data/gameMode1.png")
        self.images["GAME_2"] = pygame.image.load("data/gameMode2.png")
        self.images["GAME_3"] = pygame.image.load("data/gameMode3.png")
        self.images["GAME_4"] = pygame.image.load("data/gameMode4.png")
        self.images["GAME_5"] = pygame.image.load("data/gameMode5.png")

        # Play
        self.images["GAME_BG"] = pygame.image.load("data/blank.png")
        self.images["COVERED"] = pygame.image.load("data/tiles/COVtile.png")
        self.images["FLAGGED"] = pygame.image.load("data/tiles/FLAtile.png")
        self.images["UNCOVERED"] = pygame.image.load("data/tiles/UNCtile.png")
        self.images["MINE"] = pygame.image.load("data/tiles/MINtile.png")
        self.images["EXPLODED"] = pygame.image.load("data/tiles/EXPtile.png")
        self.images["T_1"] = pygame.image.load("data/tiles/1.png")
        self.images["T_2"] = pygame.image.load("data/tiles/2.png")
        self.images["T_3"] = pygame.image.load("data/tiles/3.png")
        self.images["T_4"] = pygame.image.load("data/tiles/4.png")
        self.images["T_5"] = pygame.image.load("data/tiles/5.png")
        self.images["T_6"] = pygame.image.load("data/tiles/6.png")
        self.images["T_7"] = pygame.image.load("data/tiles/7.png")
        self.images["T_8"] = pygame.image.load("data/tiles/8.png")
        self.images["WIN"] = pygame.image.load("data/won.png")
        self.images["LOSE"] = pygame.image.load("data/lost.png")

        # Story
        self.images["STORY_SCREEN"] = pygame.image.load("data/storyS.png")

        # Counter
        self.images["-"] = pygame.image.load("data/nums/-.png")
        self.images[0] = pygame.image.load("data/nums/0.png")
        self.images[1] = pygame.image.load("data/nums/1.png")
        self.images[2] = pygame.image.load("data/nums/2.png")
        self.images[3] = pygame.image.load("data/nums/3.png")
        self.images[4] = pygame.image.load("data/nums/4.png")
        self.images[5] = pygame.image.load("data/nums/5.png")
        self.images[6] = pygame.image.load("data/nums/6.png")
        self.images[7] = pygame.image.load("data/nums/7.png")
        self.images[8] = pygame.image.load("data/nums/8.png")
        self.images[9] = pygame.image.load("data/nums/9.png")


if __name__ == "__main__":
    game = Game()
    game.loop()
