from random import choice, randint 
 
import pygame as pg 
 
 
# Константы для размеров поля и сетки: 
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480 
GRID_SIZE = 20 
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE 
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE 
 
# Направления движения: 
UP = (0, -1) 
DOWN = (0, 1) 
LEFT = (-1, 0) 
RIGHT = (1, 0) 
 
# Цвет фона - черный: 
BOARD_BACKGROUND_COLOR = (0, 0, 0) 
 
# Цвет границы ячейки 
BORDER_COLOR = (93, 216, 228) 
 
# Цвет яблока 
APPLE_COLOR = (255, 0, 0) 
 
# Цвет змейки 
SNAKE_COLOR = (0, 255, 0) 
 
# Скорость движения змейки: 
SPEED = 20 
 
# Настройка игрового окна: 
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32) 
 
# Заголовок окна игрового поля: 
pg.display.set_caption('Змейка. Esc for quit') 
 
# Настройка времени: 
clock = pg.time.Clock() 
 
 
class GameObject: 
    """Parent class GameObject""" 
 
    def __init__(self, body_color=None) -> None: 
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)) 
        self.body_color = body_color 
 
    def draw(self): 
        """Stub method.""" 
 
 
class Snake(GameObject): 
    """Child class of GameObject class""" 
 
    def __init__(self, body_color=SNAKE_COLOR): 
        super().__init__(body_color=body_color) 
        self.reset() 
        self.direction = RIGHT 
 
    def update_direction(self): 
        """Changing the direction of the snake""" 
        if self.next_direction: 
            self.direction = self.next_direction 
            self.next_direction = None 
 
    def move(self): 
        """Snake movement""" 
        head_position_x, head_position_y = self.get_head_position 
        direction_x, direction_y = self.direction 
        self.position = ((head_position_x + (direction_x * GRID_SIZE)) 
                         % SCREEN_WIDTH, (head_position_y 
                         + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT) 
 
        self.positions.insert(0, self.position) 
 
        if len(self.positions) > self.length: 
            self.last = self.positions.pop() 
        else: 
            self.last = None 
 
    def draw(self): 
        """Drawing a snake""" 
        for position in self.positions[:-1]: 
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE))) 
            pg.draw.rect(screen, self.body_color, rect) 
            pg.draw.rect(screen, BORDER_COLOR, rect, 1) 
 
        # Отрисовка головы змейки 
        head_rect = pg.Rect(self.get_head_position, (GRID_SIZE, GRID_SIZE)) 
        pg.draw.rect(screen, self.body_color, head_rect) 
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1) 
 
        # Затирание последнего сегмента 
        if self.last: 
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE)) 
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect) 
 
    @property 
    def get_head_position(self): 
        """Returning the value of the snake's head""" 
        return self.positions[0] 
 
    def reset(self): 
        """Reset the position of the snake in certain situations""" 
        self.length = 1 
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))] 
        self.direction = choice([UP, DOWN, RIGHT, LEFT]) 
        self.next_direction = None 
        self.last = None 
 
 
class Apple(GameObject): 
    """Child class of GameObject class""" 
 
    def __init__(self, body_color=APPLE_COLOR, occupied_positions=[]): 
        super().__init__(body_color=body_color) 
        self.randomize_position(occupied_positions) 
 
    def randomize_position(self, occupied_positions=[]): 
        """Randomize the position of the apple""" 
        while True: 
            self.position = (randint(0, GRID_WIDTH) * GRID_SIZE, 
                             randint(0, GRID_HEIGHT) * GRID_SIZE) 
            if self.position not in occupied_positions: 
                break 
 
    def draw(self): 
        """Drawing an apple""" 
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE)) 
        pg.draw.rect(screen, self.body_color, rect) 
        pg.draw.rect(screen, BORDER_COLOR, rect, 1) 
 
 
def handle_keys(game_object):

    """Handling Keypress Events""" 
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            pg.quit() 
            raise SystemExit 
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_UP and game_object.direction != DOWN: 
                game_object.next_direction = UP 
            elif event.key == pg.K_DOWN and game_object.direction != UP: 
                game_object.next_direction = DOWN 
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT: 
                game_object.next_direction = LEFT 
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT: 
                game_object.next_direction = RIGHT 
            elif event.key == pg.K_ESCAPE: 
                pg.quit() 
 
 
def main(): 
    """Main func""" 
    # Инициализация PyGame: 
    pg.init() 
    # Тут нужно создать экземпляры классов. 
    snake = Snake(body_color=SNAKE_COLOR) 
    apple = Apple(body_color=APPLE_COLOR, occupied_positions=snake.positions) 
 
    while True: 
        clock.tick(SPEED) 
        handle_keys(snake) 
        snake.update_direction() 
        snake.move() 
 
        if snake.get_head_position == apple.position: 
            apple.randomize_position(snake.position) 
            snake.length += 1 
 
        elif snake.get_head_position in snake.positions[1:]: 
            snake.reset() 
            screen.fill(BOARD_BACKGROUND_COLOR) 
            apple.randomize_position(snake.position) 
 
        apple.draw() 
        snake.draw() 
        pg.display.update() 
 
 
if __name__ == '__main__': 
    main()
