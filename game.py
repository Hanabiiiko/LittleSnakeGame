import os
import random
import time
import keyboard
from entities import Snake, Apple, UP, DOWN, LEFT, RIGHT

class Game:
    def __init__(self, height, width, speed):
        self.height = height
        self.width = width
        self.speed = speed
        self.snake = Snake([(5, 5), (5, 6), (5, 7)], UP)
        self.apple = None
        self.score = 0
        self.is_game_over = False
        self.next_direction = UP
        self.spawn_apple()

    def spawn_apple(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake.body:
                self.apple = Apple((x, y))
                break

    def board_matrix(self):
        return [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def render(self):
        matrix = self.board_matrix()
        if self.apple:
            ax, ay = self.apple.position
            matrix[ay][ax] = '*'

        for i, (sx, sy) in enumerate(self.snake.body):
            if 0 <= sx < self.width and 0 <= sy < self.height:
                matrix[sy][sx] = 'X' if i == 0 else 'O'

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Счет: {self.score} (Для досрочного выхода нажмите ESC)")
        print('+' + '-' * self.width + '+')
        for row in matrix:
            print('|' + ''.join(row) + '|')
        print('+' + '-' * self.width + '+')

    def play(self):
        keyboard.unhook_all()
        last_update_time = time.time()
        self.next_direction = self.snake.direction
        self.render()

        while not self.is_game_over:
            if keyboard.is_pressed('w') and self.snake.direction != DOWN:
                self.next_direction = UP
            elif keyboard.is_pressed('s') and self.snake.direction != UP:
                self.next_direction = DOWN
            elif keyboard.is_pressed('a') and self.snake.direction != RIGHT:
                self.next_direction = LEFT
            elif keyboard.is_pressed('d') and self.snake.direction != LEFT:
                self.next_direction = RIGHT
            elif keyboard.is_pressed('esc'):
                break

            current_time = time.time()
            if current_time - last_update_time >= self.speed:
                self.snake.set_direction(self.next_direction)
                hx, hy = self.snake.head()
                dx, dy = self.snake.direction
                new_head = (hx + dx, hy + dy)

                if (new_head[0] < 0 or new_head[0] >= self.width or
                    new_head[1] < 0 or new_head[1] >= self.height or
                    new_head in self.snake.body):
                    self.is_game_over = True
                    self.render()
                    print(f"\nБАМ! Вы врезались. Игра окончена.")
                    break

                if self.apple and new_head == self.apple.position:
                    self.score += 1
                    self.snake.grow(new_head)
                    self.spawn_apple()
                else:
                    self.snake.take_step(new_head)
                
                self.render()
                last_update_time = current_time
                
            time.sleep(0.01)


        keyboard.unhook_all()
        time.sleep(1)
        return self.score