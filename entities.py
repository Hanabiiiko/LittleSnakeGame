UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def take_step(self, position):
        self.body.insert(0, position)
        self.body.pop()

    def grow(self, position):
        self.body.insert(0, position)

    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.body[0]

class Apple:
    def __init__(self, position):
        self.position = position