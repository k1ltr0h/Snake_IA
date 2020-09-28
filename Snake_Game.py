import pygame, sys, time, random, math


# Game variables

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 120

# Window size
frame_size_x = 720
frame_size_y = 480

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#Imgs
bg = pygame.image.load("snake.png")

#Clases
class GameObject:
    def __init__(self, x_, y_, size_x, size_y):
        self.pos = [x_, y_]
        self.dim = [size_x, size_y]

class node(GameObject):
    def __init__(self, x_, y_):
        super().__init__(x_, y_, 10, 10)
        self.link_up = 1
        self.link_down = 1
        self.link_right = 1
        self.link_left = 1
        self.euclidean_cost = 0
    def setLinkUp(self, cost):
        self.link_up = cost
    def setLinkDown(self, cost):
        self.link_down = cost
    def setLinkLeft(self, cost):
        self.link_left = cost
    def setLinkRight(self, cost):
        self.link_right = cost

class Snake(GameObject):
    def __init__(self, x_=100, y_=50):
        super().__init__(x_, y_, size_x=10, size_y=10)
        self.reset()

    def grow(self):
        self.score += 1

    def update(self):
        self.move()

    def reset(self, x_=100, y_=50):
        self.pos = [x_, y_]
        self.snake_body = [[x_, y_], [x_-10, y_], [x_-(2*10), y_]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def pressKey(self, key):
        # W -> Up; S -> Down; A -> Left; D -> Right
        if key == pygame.K_UP or key == ord('w'):
            self.change_to = 'UP'
        if key == pygame.K_DOWN or key == ord('s'):
            self.change_to = 'DOWN'
        if key == pygame.K_LEFT or key == ord('a'):
            self.change_to = 'LEFT'
        if key == pygame.K_RIGHT or key == ord('d'):
            self.change_to = 'RIGHT'

    def move(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.pos[1] -= 10
        if self.direction == 'DOWN':
            self.pos[1] += 10
        if self.direction == 'LEFT':
            self.pos[0] -= 10
        if self.direction == 'RIGHT':
            self.pos[0] += 10

class Food(GameObject):
    def __init__(self):
        super().__init__(x_=0, y_=0, size_x=10, size_y=10)
        self.generate()

    def generate(self):
        self.pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]

    def update(self):
        pass

class Screen(GameObject):
    def __init__(self, x_=0, y_=0, size_x=720, size_y=480):
        super().__init__(x_, y_, size_x, size_y)
        self.game_window = pygame.display.set_mode((size_x, size_y))
        self.player = Snake()
        self.food = Food()
        self.agent = Agent(self.food)
        self.food_spawn = True
        self.state = "menu"

    def gameOver(self):
        self.my_font = pygame.font.SysFont('times new roman', 90)
        self.game_over_surface = self.my_font.render('YOU DIED', True, red)
        self.game_over_rect = self.game_over_surface.get_rect()
        self.game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        self.game_window.fill(black)
        self.game_window.blit(self.game_over_surface, self.game_over_rect)
        self.showScore(0, red, 'times', 20)
        pygame.display.flip()
        self.state = "gameover"
        self.player.reset()

    def showScore(self, choice=1, color=white, font="consolas", size=20):
        #show_score(1, white, 'consolas', 20)
        self.score_font = pygame.font.SysFont(font, size)
        self.score_surface = self.score_font.render('Score : ' + str(self.player.score), True, color)
        self.score_rect = self.score_surface.get_rect()
        if choice == 1:
            self.score_rect.midtop = (frame_size_x/10, 15)
        else:
            self.score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        self.game_window.blit(self.score_surface, self.score_rect)

    def changeState(self):
        if self.state == "play":
            self.state = "pause"
        elif self.state == "pause":
            self.state = "play"
        elif self.state == "gameover":
            self.state = "play"
        elif self.state == "menu" and self.pos[0] == 0:
            self.state = "play"
        elif self.state == "menu" and self.pos[0] == 740:
            self.state = "simulation"

    def update(self):
        if self.state == "play":
            self.player.snake_body.insert(0, list(self.player.pos))
            if self.player.pos[0] == self.food.pos[0] and self.player.pos[1] == self.food.pos[1]:
                self.player.grow()
                self.food_spawn = False
            else:
                self.player.snake_body.pop()
            if not self.food_spawn:
                self.food.generate()
            self.food_spawn = True
            # Moving the snake
            self.player.update()
            self.food.update()
            # Game Over conditions
            # Getting out of bounds
            if self.player.pos[0] < 0 or self.player.pos[0] > frame_size_x-10:
                self.gameOver()
            if self.player.pos[1] < 0 or self.player.pos[1] > frame_size_y-10:
                self.gameOver()
            # Touching the snake body
            for block in self.player.snake_body[1:]:
                if self.player.pos[0] == block[0] and self.player.pos[1] == block[1]:
                    self.gameOver()
        elif self.state == "simulation":
            self.agent.snake_body.insert(0, list(self.agent.pos))
            if self.agent.pos[0] == self.food.pos[0] and self.agent.pos[1] == self.food.pos[1]:
                self.agent.grow()
                self.food_spawn = False
            else:
                self.agent.snake_body.pop()
            if not self.food_spawn:
                self.food.generate()
            self.food_spawn = True
            # Moving the snake
            self.food.update()
            self.agent.update()
            # Game Over conditions
            # Getting out of bounds
            if self.agent.pos[0] < 0 or self.agent.pos[0] > frame_size_x-10:
                self.agent.reset()
            if self.agent.pos[1] < 0 or self.agent.pos[1] > frame_size_y-10:
                self.agent.reset()
            # Touching the snake body
            for block in self.agent.snake_body[1:]:
                if self.agent.pos[0] == block[0] and self.agent.pos[1] == block[1]:
                    print("auch")
                    self.agent.reset()
            
    def render(self):
        # GFX
        if self.state == "play":
            self.game_window.fill(black)
            for pos in self.player.snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(self.game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            # Snake food
            pygame.draw.rect(self.game_window, white, pygame.Rect(self.food.pos[0], self.food.pos[1], 10, 10))
            self.showScore()

        elif self.state == "simulation":
            self.game_window.fill(black)
            for pos in self.agent.snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                #print(self.agent.pos)
                pygame.draw.rect(self.game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            # Snake food
            pygame.draw.rect(self.game_window, white, pygame.Rect(self.food.pos[0], self.food.pos[1], 10, 10))
            self.showScore()

        elif self.state == "menu":
            self.game_window.blit(bg, (0, 0), (self.pos[0], self.pos[1], 740, 480))
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

class Agent(Snake):
    def __init__(self, food):
        super().__init__()
        self.wall_cost = 1000
        self.food = food
        self.dist = 0
        self.priority = []
        self.path = []

    def euclidean_dist(self, pos):
        dist_x = self.food.pos[0] - pos[0]
        dist_y = self.food.pos[1] - pos[1]
        return math.sqrt(dist_x**2 + dist_y**2)
    
    def greedy(self, pos = []):
        if not pos:
            pos = self.pos
        #print(pos)
        short_dist = None
        tmp_move = []
        collision = False
        up = [pos[0], pos[1]-10]
        down = [pos[0], pos[1]+10]
        left = [pos[0]-10, pos[1]]
        right = [pos[0]+10, pos[1]]
        moves = [up, down, left, right, pos]
        block = self.snake_body
        for move in moves:
            #if not collision and not (move in block):
            dist = self.euclidean_dist(move)
            if short_dist == None or dist <= short_dist:
                short_dist = dist
                tmp_move = move
            collision = False
                    
        self.path.append(tmp_move)
        if(short_dist != 0):
            self.greedy(tmp_move)
        
        #print(self.path, self.direction, short_dist)

    def ucs(self):
        pass
    def a_Star(self):
        pass
    def update(self):
        if not self.path:
            self.greedy()
        else:
            self.move()
    def move(self):
        self.pos = self.path[0]
        self.path.pop(0)
#Fin Clases

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake')
#game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
screen = Screen()

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
if __name__ == '__main__':
    player = screen.player

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.changeState()
                if screen.state == "play":
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    player.pressKey(event.key)
                if screen.state == "menu":
                    if (event.key == pygame.K_LEFT or event.key == ord('a')) and screen.pos[0] != 0:
                        screen.pos[0] -= 740 
                    elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and screen.pos[0] != 740:
                        screen.pos[0] += 740 
                    #print(screen.pos)
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        screen.update()
        screen.render()
