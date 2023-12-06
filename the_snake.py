from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона
BACKGROUND_COLOR = (0, 0, 0)

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.color = None

    def draw(self):
        pass


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.color = (0, 255, 0)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            ((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
            (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        )

        if len(self.positions) > 2 and new in self.positions[2:]:
            self._reset()
        else:
            self.positions.insert(0, new)
            self.last = (
                self.positions.pop() if len(self.positions) > self.length
                else None
            )

    def _reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BACKGROUND_COLOR)

    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BACKGROUND_COLOR, last_rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    def __init__(self):
        self.color = (255, 0, 0)

        self._randomize_position()

    def _randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


def main():
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(20)
        snake.handle_keys()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple._randomize_position()

        # Проверка на столкновение с самим собой
        if snake.get_head_position() in snake.positions[1:]:
            snake._reset()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
