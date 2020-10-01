import pygame, sys, time, random, math, gc


# Game variables

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 60

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
        self.pos = [100,50]

    def generate(self, snake_body):
        while True:
            #print("hols\n")
            pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            if pos not in snake_body:
                self.pos = pos
                break

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
        if self.state == "play":
            self.score_surface = self.score_font.render('Score : ' + str(self.player.score), True, color)
        else:
            self.score_surface = self.score_font.render('Score : ' + str(self.agent.score), True, color)
        self.score_rect = self.score_surface.get_rect()
        if choice == 1:
            self.score_rect.midtop = (frame_size_x/10, 15)
        else:
            self.score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        self.game_window.blit(self.score_surface, self.score_rect)

    def changeState(self, newState):

        if self.state == "play":
            self.agent.reset()
        elif self.state == "simulation":
            self.agent.reset()
        elif self.state == "pause":
            pass
        elif self.state == "menu":
            pass
        
        prevState = self.state
        self.state = newState

        if self.state == "play":
            pass
        elif self.state == "simulation":
            pass
        elif self.state == "pause":
            pass
        elif self.state == "menu":
            pass

    def update(self):
        if self.state == "play":
            self.player.snake_body.insert(0, list(self.player.pos))
            if self.player.pos[0] == self.food.pos[0] and self.player.pos[1] == self.food.pos[1]:
                self.player.grow()
                self.food_spawn = False
            else:
                self.player.snake_body.pop()
            if not self.food_spawn:
                self.food.generate(self.player.snake_body)
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
                self.food.generate(self.agent.snake_body)
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

class Node(GameObject):
    def __init__(self, x_, y_):
        super().__init__(x_, y_, 10, 10)
        self.node_up = None
        self.node_down = None
        self.node_right = None
        self.node_left = None
        self.euclidean_cost = 0
    def setCost(self, cost):
        self.euclidean_cost = cost
    def setAsWall(self):
        self.euclidean_cost = 10000
    def addNode(self):
        pass

class World(Screen):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def createWorld(self):
        self.nodes.append(Node(self.food.pos[0], self.food.pos[1]))
        for block in self.agent.snake_body:
            self.nodes.append(Node(block.pos[0], block.pos[1]).setAsWall())

    def update(self):
        super().update()

    def reset(self):
        self.nodes = []

        


class Agent(Snake):
    def __init__(self, food):
        super().__init__()
        self.wall_cost = 1000
        self.food = food
        self.dist = 0
        self.priority = []
        self.path = []
        self.visited = []

    def euclidean_dist(self, pos):
        dist_x = self.food.pos[0] - pos[0]
        dist_y = self.food.pos[1] - pos[1]
        return math.sqrt(dist_x**2 + dist_y**2)

    def greedy(self):
        pos = self.pos
        short_dist = None

        while short_dist != 0:
            short_dist = None
            tmp_move = []
            #print(pos)
            up = [pos[0], pos[1]-10]
            down = [pos[0], pos[1]+10]
            left = [pos[0]-10, pos[1]]
            right = [pos[0]+10, pos[1]]
            moves = [up, down, left, right]
            block = self.snake_body
            for move in moves:
                if move not in block and move[0] >= 0 and move[0] <= frame_size_x-10 and move[1] >= 0 and move[1] <= frame_size_y-10:
                    dist = self.euclidean_dist(move)
                    #print(dist, short_dist, self.food.pos, self.pos, self.snake_body)
                    if (short_dist == None or dist <= short_dist) and move not in self.path:
                        short_dist = dist
                        tmp_move = move
                        #print("->",move,"\n")
            if tmp_move == []:
                #print("\n aquí \n")
                print(self.path, self.priority, self.pos)
                break
                #self.reset()
                #print(block)
                #exit()
            else:
                self.path.append(tmp_move)
                pos = tmp_move
        
            #print(block, self.food.pos, "\n", self.path, "\n")
    def greedy_Priority(self):
        pos = self.pos
        short_dist = None
        self.visited = []
        while short_dist != 0:
            short_dist = None
            sprint_moves = []
            sprint_costs = []
            #print(pos)
            up = [pos[0], pos[1]-10]
            down = [pos[0], pos[1]+10]
            left = [pos[0]-10, pos[1]]
            right = [pos[0]+10, pos[1]]
            moves = [up, down, left, right]
            block = self.snake_body
            for move in moves:
                if move not in block and move not in self.path and move not in self.visited and move[0] >= 0 and move[0] <= frame_size_x-10 and move[1] >= 0 and move[1] <= frame_size_y-10:
                    dist = self.euclidean_dist(move)
                    #sprint_costs.append(dist)
                    sprint_moves.append(move)
                    sprint_costs.append(dist)
            sprint_costs = sorted(sprint_costs)
            #print(sprint_costs)
            temp_moves = []
            for cost in sprint_costs:
                for move in sprint_moves:
                    if cost == self.euclidean_dist(move) and move not in temp_moves:
                        temp_moves.append(move)
            sprint_moves = temp_moves
            self.priority.insert(0, sprint_moves)
            if self.priority[0] == []:
                while self.priority[0] == []:
                    #print(self.path)
                    if self.path != []:
                        #print("list: ",self.priority)
                        #print("Path: ", self.path)
                        self.visited.append(self.path[-1])
                        self.priority.pop(0)
                        self.path.pop()
                        if self.path != []:
                            self.pos = self.path[-1]
                        else:
                            break
                    else:
                        break
                    #print(block)
                if self.path == []:
                    break
                self.path.append(self.priority[0][0])
                #print("Fuera: ", self.priority[0][0])
                pos = self.priority[0][0]
                self.priority[0].pop(0)
            else:
                short_dist = sprint_costs[0]
                self.path.append(sprint_moves[0])
                pos = sprint_moves[0]
                #print(pos)
                self.priority[0].pop(0)
            #print(block, self.food.pos, "\n", self.path, "\n")

    def ucs(self):
        pass

    def a_Star(self):
        pass

    def update(self):
        if not self.path:
            self.greedy_Priority()
        try:
            self.move()
        except:
            self.reset()

    def move(self):
        self.pos = self.path[0]
        self.path.pop(0)

    def reset(self):
        super().reset()
        self.path = []
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
world = World()

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
if __name__ == '__main__':
    player = world.player

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if world.state == "play":
                        world.changeState("pause")
                    elif world.state == "pause":
                        world.changeState("play")
                    elif world.state == "menu":
                        if world.pos[0] == 0:
                            world.changeState("play")
                        if world.pos[0] == 740:
                            world.changeState("simulation")
                    elif world.state == "gameover":
                        world.changeState("play")
                if event.key == pygame.K_q or event.key == ord("q"):
                    if world.state == "play" or world.state == "simulation":
                        world.changeState("menu")
                if world.state == "play":
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    player.pressKey(event.key)
                if world.state == "menu":
                    if (event.key == pygame.K_LEFT or event.key == ord('a')) and world.pos[0] != 0:
                        world.pos[0] -= 740 
                    elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and world.pos[0] != 740:
                        world.pos[0] += 740 
                    #print(screen.pos)
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        world.update()
        world.render()
