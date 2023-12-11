from random import choice, randint

import pygame as pg

# Константы для размеров
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = 32, 24
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

# Цвета 
DESK_BG_COLOR = (232, 232, 232)
APPLE_BG_COLOR = (255, 0, 0)
APPLE_FG_COLOR = (93, 216, 228)
SNAKE_BG_COLOR = (0, 255, 0)
SNAKE_FG_COLOR = (93, 216, 228)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
TURNS = { # Повороты (клавиша, старое направление) -> новое направление
    (pg.K_UP,     DOWN): DOWN,
    (pg.K_UP,       UP): UP,
    (pg.K_UP,     LEFT): UP,
    (pg.K_UP,    RIGHT): UP,
    
    (pg.K_DOWN,   DOWN): DOWN,
    (pg.K_DOWN,     UP): UP,
    (pg.K_DOWN,   LEFT): DOWN,
    (pg.K_DOWN,  RIGHT): DOWN,
    
    (pg.K_LEFT,   DOWN): LEFT,
    (pg.K_LEFT,     UP): LEFT,
    (pg.K_LEFT,   LEFT): LEFT,
    (pg.K_LEFT,  RIGHT): RIGHT,
    
    (pg.K_RIGHT,  DOWN): RIGHT,
    (pg.K_RIGHT,    UP): RIGHT,
    (pg.K_RIGHT,  LEFT): LEFT,
    (pg.K_RIGHT, RIGHT): RIGHT,
}

CLOCK_FRAMERATE_MILLISECONDS = 10


class GameObject:
    """
    Базовый класс для игровых объектов.
    """
    def __init__(self, bg_color, fg_color):
        """Инициализация базового игрового объекта."""
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def free_cell(self, surface, position):
        pg.draw.rect(surface, DESK_BG_COLOR, pg.Rect(position, (CELL_SIZE, CELL_SIZE)))
    
    def draw_cell(self, surface, position):
        rect = pg.Rect(position, (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(surface, self.bg_color, rect)
        pg.draw.rect(surface, self.fg_color, rect, 1)
    
    def draw(self, surface):
        """Метод для отрисовки объекта. Переопределяется в подклассах."""
        pass


class Snake(GameObject):
    """
    Класс для представления змейки в игре.
    """
    def __init__(self, bg_color=SNAKE_BG_COLOR, fg_color=SNAKE_FG_COLOR):
        """Инициализация змейки."""
        super().__init__(bg_color, fg_color)
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Пересчет позиций на один шаг."""
        head = self.get_head_position()
        x, y = self.direction
        new = (
            ((head[0] + (x * CELL_SIZE)) % SCREEN_WIDTH),
            (head[1] + (y * CELL_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new)
        self.last = (
            self.positions.pop() 
        if len(self.positions) > self.length else 
            None
        )

    def reset(self):
        """Сброс змейки к начальному состоянию после столкновения."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """
        Отрисовка змейки на игровом поле.

        Args:
            surface: поверхность для отрисовки (pg.Surface).
        """
        # Отрисовка головы змейки
        self.draw_cell(surface, self.positions[0])
        # Затирание последнего сегмента
        if self.last:
            self.free_cell(surface, self.last)

    def update_direction(self, next_direction):
        """Обновление направления движения змейки, если оно было изменено."""
        self.direction = next_direction


class Apple(GameObject):
    """
    Класс для представления яблока в игре.
    """
    def __init__(self, snake, bg_color=APPLE_BG_COLOR, fg_color=APPLE_FG_COLOR):
        """Инициализация яблока."""
        super().__init__(bg_color, fg_color)
        self.randomize_position(snake)

    def randomize_position(self, snake):
        """Случайное размещение яблока на игровом поле."""
        while self.position in snake.positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                randint(0, GRID_HEIGHT - 1) * CELL_SIZE
            )

    def draw(self, surface):
        """
        Отрисовка яблока на игровом поле.

        Args:
            surface: поверхность для отрисовки (pg.Surface).
        """
        self.draw_cell(surface, self.position)


def handle_keys(snake):
    """Обработка нажатий клавиш."""
    for event in pg.event.get():
        if event.type != pg.KEYDOWN:
            continue
        # Выход из игры
        if event.key == pg.K_ESCAPE:
            return False
         # Изменение направлеения
        if event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):
            snake.update_direction(TURNS[(event.key, snake.direction)])
    return True


def main():
    """Главная функция для запуска игры."""
    # Инициализация PyGame
    pg.init()
    pg.display.set_caption('Змейка. Выход: Esc') # Заголовок окна
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    screen.fill(DESK_BG_COLOR)

    snake = Snake()
    apple = Apple(snake)
    apple.draw(screen)

    clock = pg.time.Clock()
    while True:
        clock.tick(CLOCK_FRAMERATE_MILLISECONDS)
        if not handle_keys(snake): 
            break

        snake.move()
        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
            apple.draw(screen)

        # Проверка на столкновение с самим собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(DESK_BG_COLOR)
            apple.draw(screen)
        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
