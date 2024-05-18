import enum


class Player(enum.Enum):
    X = 1
    O = 2

    @property
    def other(self):
        return self.X if self == self.O else self.O

    @property
    def turns(self):
        return f"{self.name}'s Turn"

    @property
    def winning(self):
        return f"{self.name} wins!"
