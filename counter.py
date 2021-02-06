class Counter:
    def __init__(self, parent, x, y, n1, n2, n3):
        """Initialises counters."""
        self.parent = parent
        self.x = x
        self.y = y
        self.numbers = [n1, n2, n3]

    def draw(self):
        for i in range(0, 3):
            self.parent.game_display.blit(
                self.parent.images[self.numbers[i]], (self.x+(15*i), self.y))

    def increment(self):
        """Increments the total number of the counter."""
        if self.numbers[2] < 9:
            self.numbers[2] += 1
        elif self.numbers[1] < 9:
            self.numbers[1] += 1
            self.numbers[2] = 0
        else:
            self.numbers[0] += 1
            self.numbers[1] = 0
            self.numbers[2] = 0

    def decrement(self):
        """Decrements the total number of the counter."""
        if self.numbers[2] > 0:
            self.numbers[2] -= 1
        elif self.numbers[1] > 0:
            self.numbers[1] -= 1
            self.numbers[2] = 9
        elif self.numbers[0] > 0:
            self.numbers[0] -= 1
            self.numbers[1] = 9
            self.numbers[2] = 9

    def get_val(self):
        """Returns the value of the counter."""
        total_val = self.numbers[0] * 100
        total_val += self.numbers[1] * 10
        total_val += self.numbers[2]
        return total_val

    def set_val(self, aim):
        """Sets the value of the counter"""
        while aim > self.get_val():
            self.increment()
        while self.get_val() > aim:
            self.decrement()
