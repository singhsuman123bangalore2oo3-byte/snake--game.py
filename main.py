from random import randrange

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class SnakeBoard(Widget):
    grid_size = 20

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)
        self.reset()

    def reset(self):
        middle = self.grid_size // 2
        self.snake = [
            (middle - 1, middle),
            (middle, middle),
            (middle + 1, middle),
        ]
        self.direction = (-1, 0)
        self.next_direction = self.direction
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.draw()

    def new_food(self):
        empty = [
            (x, y)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if (x, y) not in self.snake
        ]
        return empty[randrange(len(empty))]

    def set_direction(self, direction):
        if direction != (-self.direction[0], -self.direction[1]):
            self.next_direction = direction

    def step(self, _dt):
        if self.game_over:
            return

        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.snake[-1]
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (
            0 <= new_head[0] < self.grid_size
            and 0 <= new_head[1] < self.grid_size
        )
        eating = new_head == self.food
        body = self.snake if eating else self.snake[1:]

        if hit_wall or new_head in body:
            self.game_over = True
            self.draw()
            return

        self.snake.append(new_head)

        if eating:
            self.score += 1
            self.food = self.new_food()
        else:
            self.snake.pop(0)

        self.draw()

    def draw(self, *_args):
        self.canvas.clear()

        if self.width <= 0 or self.height <= 0:
            return

        cell = min(self.width, self.height) / self.grid_size
        board_size = cell * self.grid_size
        left = self.x + (self.width - board_size) / 2
        bottom = self.y + (self.height - board_size) / 2

        with self.canvas:
            Color(0.06, 0.08, 0.12, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.12, 0.16, 0.21, 1)
            Rectangle(pos=(left, bottom), size=(board_size, board_size))

            Color(1, 0.28, 0.24, 1)
            food_x, food_y = self.food
            Rectangle(
                pos=(left + food_x * cell, bottom + food_y * cell),
                size=(cell * 0.86, cell * 0.86),
            )

            for index, (snake_x, snake_y) in enumerate(self.snake):
                if index == len(self.snake) - 1:
                    Color(0.34, 1, 0.47, 1)
                else:
                    Color(0.12, 0.78, 0.32, 1)

                Rectangle(
                    pos=(left + snake_x * cell, bottom + snake_y * cell),
                    size=(cell * 0.86, cell * 0.86),
                )


class SnakeGame(App):
    def build(self):
        self.title = "Snake Game"
        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        self.status = Label(
            text="Score: 0",
            size_hint_y=None,
            height=48,
            font_size="22sp",
            bold=True,
        )
        root.add_widget(self.status)

        self.board = SnakeBoard()
        root.add_widget(self.board)

        controls = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=150,
            spacing=5,
        )

        up_row = BoxLayout(spacing=5)
        up_row.add_widget(Widget())
        up_row.add_widget(self.make_button("▲", (0, 1)))
        up_row.add_widget(Widget())
        controls.add_widget(up_row)

        middle_row = BoxLayout(spacing=5)
        middle_row.add_widget(self.make_button("◀", (-1, 0)))
        middle_row.add_widget(self.make_button("▼", (0, -1)))
        middle_row.add_widget(self.make_button("▶", (1, 0)))
        controls.add_widget(middle_row)

        root.add_widget(controls)

        restart = Button(
            text="Restart",
            size_hint_y=None,
            height=48,
            font_size="18sp",
        )
        restart.bind(on_release=self.restart)
        root.add_widget(restart)

        Clock.schedule_interval(self.update_game, 0.15)
        return root

    def make_button(self, text, direction):
        button = Button(text=text, font_size="28sp")
        button.bind(
            on_release=lambda _button: self.board.set_direction(direction)
        )
        return button

    def update_game(self, dt):
        self.board.step(dt)

        if self.board.game_over:
            self.status.text = f"Game over! Score: {self.board.score}"
        else:
            self.status.text = f"Score: {self.board.score}"

    def restart(self, *_args):
        self.board.reset()
        self.status.text = "Score: 0"


if __name__ == "__main__":
    SnakeGame().run()
