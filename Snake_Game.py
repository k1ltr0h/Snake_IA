import pygame, sys, time, random, math, gc


# Game variables

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
#difficulty = 60

# Window size
frame_size_x = 720
frame_size_y = 480

difficulty_var = 20

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#Imgs
menu_bg = pygame.image.load("imgs/snake.png")
#game_bg = pygame.image.load("imgs/background.png")


#Clases
class GameObject:
    def __init__(self, x_, y_, size_x, size_y):
        self.pos = [x_, y_]
        self.dim = [size_x, size_y]

class Snake(GameObject):
    def __init__(self, x_=100, y_=50):
        super().__init__(x_, y_, size_x=10, size_y=10)
        self.reset()
        self.highScore = 0

    def grow(self):
        self.score += 1
        if self.score > self.highScore:
            self.highScore = self.score

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
        self.pos = [500,50]

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
        self.prevState = ""
        self.difficulty = 100

    def gameOver(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.showScore(0, red, 'times', 20)
        pygame.display.flip()
        self.state = "gameover"
    
    def options(self):
        self.game_window.fill(black)
        my_font = pygame.font.SysFont('times new roman', 30)
        if self.prevState == "play":

            if self.difficulty == difficulty_var:
                dif = " Easy >"
            elif self.difficulty == difficulty_var*2:
                dif = "< Normal >"
            elif self.difficulty == difficulty_var*3:
                dif = "< Difícil >"
            elif self.difficulty == difficulty_var*4:
                dif = "< Muy difícil >"
            elif self.difficulty == difficulty_var*5:
                dif = "< Imposible"
            
            dificultad_surface = my_font.render('Dificultad: ', True, red)
            dif_lvl_surface = my_font.render(dif, True, red)
            dificultad_rect = dificultad_surface.get_rect()
            dif_lvl_surface_rect = dif_lvl_surface.get_rect()
            dificultad_rect.midtop = (frame_size_x/3, frame_size_y/4)
            dif_lvl_surface_rect.midtop = (2*frame_size_x/3, frame_size_y/4)
            self.game_window.blit(dificultad_surface, dificultad_rect)
            self.game_window.blit(dif_lvl_surface, dif_lvl_surface_rect)

        elif self.prevState == "simulation":
            alg_index = self.agent.algorithm

            if alg_index == 0:
                alg = self.agent.algorithm_array[alg_index] + " >"
            elif alg_index == 1:
                alg = "< " + self.agent.algorithm_array[alg_index] + " >"
            elif alg_index == 2:
                alg = "< " + self.agent.algorithm_array[alg_index]

            algorithm_surface = my_font.render('Algoritmo: ', True, red)
            alg_type_surface = my_font.render(alg , True, red)
            algorithm_rect = algorithm_surface.get_rect()
            alg_type_rect = alg_type_surface.get_rect()
            algorithm_rect.midtop = (frame_size_x/3, frame_size_y/4)
            alg_type_rect.midtop = (2*frame_size_x/3, frame_size_y/4)
            self.game_window.blit(algorithm_surface, algorithm_rect)
            self.game_window.blit(alg_type_surface, alg_type_rect)


    def showScore(self, choice=1, color=white, font="consolas", size=20):
        #show_score(1, white, 'consolas', 20)
        self.score_font = pygame.font.SysFont(font, size)
        if self.state == "play":
            self.score_surface = self.score_font.render('Score : ' + str(self.player.score), True, color)
            self.highScore_surface = self.score_font.render('HighScore : ' + str(self.player.highScore), True, color)
        else:
            self.score_surface = self.score_font.render('Score : ' + str(self.agent.score), True, color)
            self.highScore_surface = self.score_font.render('HighScore : ' + str(self.agent.highScore), True, color)
        self.score_rect = self.score_surface.get_rect()
        self.highScore_rect = self.highScore_surface.get_rect()
        if choice == 1:
            self.score_rect.midtop = (frame_size_x/10, 15)
            self.highScore_rect.midtop = (4*frame_size_x/5, 15)
        else:
            self.score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        self.game_window.blit(self.score_surface, self.score_rect)
        self.game_window.blit(self.highScore_surface, self.highScore_rect)

    def changeState(self, newState):

        if self.state == "play":
            pass
        elif self.state == "simulation":
            pass
        elif self.state == "pause":
            pass
        elif self.state == "menu":
            self.player.reset()
            self.agent.reset()
            self.difficulty = 40
        elif self.state == "gameover":
            self.player.reset()
            self.agent.reset()

        
        self.prevState = self.state
        self.state = newState

        if self.state == "play":
            pass
        elif self.state == "simulation":
            self.difficulty = 100
        elif self.state == "pause":
            pass
        elif self.state == "menu":
            pass
        elif self.state == "gameover":
            pass
            
    def render(self):
        # GFX
        if self.state == "play":
            self.game_window.fill(black)
            #self.game_window.blit(game_bg, (0, 0))
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
            #self.game_window.blit(game_bg, (0, 0))
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
            self.game_window.blit(menu_bg, (0, 0), (self.pos[0], self.pos[1], 720, 480))
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(self.difficulty)

class Node(GameObject):
    def __init__(self, x_, y_):
        super().__init__(x_, y_, 10, 10)
        self.node_up = None
        self.node_down = None
        self.node_right = None
        self.node_left = None
        self.euclidean_cost = 0
        self.up = [self.pos[0], self.pos[1]-10]
        self.down = [self.pos[0], self.pos[1]+10]
        self.left = [self.pos[0]-10, self.pos[1]]
        self.right = [self.pos[0]+10, self.pos[1]]
        self.fullConnected = False

    def update(self):
        if self.node_up != None and self.node_down != None and self.node_left != None and self.node_right != None:
            self.fullConnected = True

    def setCost(self, cost):
        self.euclidean_cost = cost
    def setAsWall(self):
        self.euclidean_cost = 10000

    def addUp(self):
        self.node_up = Node(self.pos[0], self.pos[1]-10)
        return self.node_up

    def addDown(self):
        self.node_down = Node(self.pos[0], self.pos[1]+10)
        return self.node_down

    def addLeft(self):
        self.node_left = Node(self.pos[0]-10, self.pos[1])
        return self.node_left

    def addRight(self):
        self.node_right = Node(self.pos[0]+10, self.pos[1])
        return self.node_right

class Graph:
    def __init__(self, startNode):
        self.nodes = [startNode]
        self.explored = [] #nodos fullConnected

    def addNode(self, node, dir, cost):
        if dir == 0:
            newNode = node.addUp()
        elif dir == 1:
            newNode = node.addDown()
        elif dir == 2:
            newNode = node.addLeft()
        elif dir == 3:
            newNode = node.addRight()
    
        self.nodes.append(newNode)
        newNode.setCost(cost)

class World(Screen):
    def __init__(self):
        super().__init__()

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

        self.checkCollitions()

    def reset(self):
        self.nodes = []

    def checkCollitions(self):
        # Game Over conditions
        if self.state == "play":
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


class Agent(Snake):
    def __init__(self, food):
        super().__init__()
        self.food = food
        self.dist = 0
        self.map = []
        self.priority = []
        self.path = []
        self.visited = []
        self.algorithm = 1
        self.algorithm_array = ["Greedy", "Greedy_DFS_Priority", "RRT"]
        self.readWorld()
        self.cleanTree()

    def cleanTree(self):
        self.tree = Graph(Node(self.pos[0], self.pos[1]))
    
    def readWorld(self):
        self.map = []
        for node in range(int(frame_size_x/10)):
            x = node*10
            for otherNode in range(int(frame_size_y/10)):
                y = otherNode*10
                self.map.append([x, y])

        for node in self.snake_body[1:]:
            self.map.remove(node)

        if self.snake_body[0] != self.snake_body[1]:
            self.map.remove(self.snake_body[0])

    def euclidean_dist(self, pos, obj = None):
        if obj == None:
            obj = self.food.pos
        dist_x = obj[0] - pos[0]
        dist_y = obj[1] - pos[1]
        return math.sqrt(dist_x**2 + dist_y**2)

    def rrt(self):
        pos = self.pos
        self.readWorld()
        self.cleanTree()
        self.visited = []
        while True:
            q_rand = self.map[random.randrange(len(self.map))]
            tmp_cost = None
            tmp_move = None
            tmp_node = None
            move_flag = 0

            #Implementar zonas para encontrar el nodo más cercano con mayor eficiencia
            
            for node in self.tree.nodes:

                if node.pos not in self.visited:
                    counter = 0
                    moves = [node.up, node.down, node.left, node.right]

                    for move in moves:
                        cost = self.euclidean_dist(move, q_rand)
                        if move in self.map and (tmp_cost == None or tmp_cost > cost):
                            tmp_cost = cost
                            tmp_move = move
                            tmp_node = node
                            move_flag = counter
                        counter = counter + 1
                    if tmp_move == None:
                        self.visited.append(node.pos)
                    else:
                        break           
                    
            self.tree.addNode(tmp_node, move_flag, tmp_cost)
            self.map.remove(tmp_move)

            #print(len(self.map))
            #print(len(self.tree.nodes))

            if tmp_move == self.food.pos:
                print("Objetivo encontrado e.e!!!\n", self.food.pos)
                break

        # Greedy DFS Priority para grafos
        pos = self.tree.nodes[0]
        self.visited = []
        while pos.pos != self.food.pos:
            links = [pos.node_up, pos.node_down, pos.node_left, pos.node_right]
            tmp_cost = None
            sprint_costs = []

            for node in links[::-1]:
                if node == None or node in self.visited:
                    links.remove(node)

            for node in links:
                for otherNode in links:
                    if node != otherNode and otherNode.euclidean_cost < node.euclidean_cost:
                        index_a = links.index(node)
                        index_b = links.index(otherNode)
                        tmp = node
                        links[index_a] = otherNode
                        links[index_b] = tmp

            self.priority.insert(0, links)
            if self.priority[0] == []:

                while self.priority[0] == []:
                    self.visited.append(self.path[-1])
                    self.priority.pop(0)
                    self.path.pop()


                self.path.append(self.priority[0][0])
                pos = self.priority[0][0]
                self.priority[0].pop(0)

            else:
                self.path.append(links[0])
                pos = links[0]
                self.priority[0].pop(0)
               
        for node in range(len(self.path)):
           self.path[node] = self.path[node].pos

    def greedy(self):
        pos = self.pos
        short_dist = None

        while short_dist != 0:
            short_dist = None
            tmp_move = []
            up = [pos[0], pos[1]-10]
            down = [pos[0], pos[1]+10]
            left = [pos[0]-10, pos[1]]
            right = [pos[0]+10, pos[1]]
            moves = [up, down, left, right]
            block = self.snake_body

            for move in moves:
                if move not in block and move[0] >= 0 and move[0] <= frame_size_x-10 and move[1] >= 0 and move[1] <= frame_size_y-10:
                    dist = self.euclidean_dist(move)
                    if (short_dist == None or dist <= short_dist) and move not in self.path:
                        short_dist = dist
                        tmp_move = move

            if tmp_move == []:
                break
            else:
                self.path.append(tmp_move)
                pos = tmp_move
        
    def greedy_Priority(self):
        pos = self.pos
        first_pos = self.pos
        short_dist = None
        self.visited = []
        self.priority = []
        fin = False
        while short_dist != 0:
            short_dist = None
            sprint_moves = []
            sprint_costs = []

            up = [pos[0], pos[1]-10]
            down = [pos[0], pos[1]+10]
            left = [pos[0]-10, pos[1]]
            right = [pos[0]+10, pos[1]]
            moves = [up, down, left, right]
            block = self.snake_body

            for move in moves:
                if move not in block and move not in self.path and move not in self.visited and move[0] >= 0 and move[0] <= frame_size_x-10 and move[1] >= 0 and move[1] <= frame_size_y-10:
                    dist = self.euclidean_dist(move)
                    sprint_moves.append(move)
                    sprint_costs.append(dist)

            sprint_costs = sorted(sprint_costs)
            temp_moves = []

            for cost in sprint_costs:
                for move in sprint_moves:
                    if cost == self.euclidean_dist(move) and move not in temp_moves:
                        temp_moves.append(move)

            sprint_moves = temp_moves
            self.priority.insert(0, sprint_moves)

            if self.priority[0] == []:

                while self.priority[0] == []:
                    if self.path != []:
                        self.visited.append(self.path[-1])
                        self.priority.pop(0)
                        self.path.pop()
                    else:
                        fin = True
                        break

                if fin:
                    pos = first_pos
                    self.path.append(pos)
                    self.greedy()
                    break

                self.path.append(self.priority[0][0])
                pos = self.priority[0][0]
                self.priority[0].pop(0)

            else:
                short_dist = sprint_costs[0]
                self.path.append(sprint_moves[0])
                pos = sprint_moves[0]
                self.priority[0].pop(0)

    def ucs(self):
        pass

    def a_Star(self):
        pass

    def update(self):
        if not self.path:
            if self.algorithm_array[self.algorithm] == "Greedy_DFS_Priority":
                self.greedy_Priority()
            elif self.algorithm_array[self.algorithm] == "Greedy":
                self.greedy()
            elif self.algorithm_array[self.algorithm] == "RRT":
                self.rrt()
        
        self.move()

    def move(self):
        if self.path != []:
            self.pos = self.path[0]
            self.path.pop(0)
        else:
            self.reset()

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

                    if world.state == "play" or world.state == "simulation":
                        world.changeState("pause")
                    elif world.state == "pause" and world.prevState == "play":
                        world.changeState("play")
                    elif world.state == "pause" and world.prevState == "simulation":
                        world.changeState("simulation")

                    elif world.state == "menu":
                        if world.pos[0] == 0:
                            world.changeState("play")
                        if world.pos[0] == 720:
                            world.changeState("simulation")

                    elif world.state == "gameover":
                        world.changeState("play")

                if event.key == pygame.K_q or event.key == ord("q"):
                    if world.state == "play" or world.state == "simulation":
                        world.changeState("menu")
                if world.state == "play":
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    player.pressKey(event.key)

                elif world.state == "menu":
                    if (event.key == pygame.K_LEFT or event.key == ord('a')) and world.pos[0] != 0:
                        world.pos[0] -= frame_size_x 
                    elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and world.pos[0] != frame_size_x:
                        world.pos[0] += frame_size_x 

                elif world.state == "pause":
                    if world.prevState == "play":
                        if (event.key == pygame.K_LEFT or event.key == ord('a')) and world.difficulty != difficulty_var:
                            world.difficulty -= difficulty_var 
                        elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and world.difficulty != difficulty_var*5:
                            world.difficulty += difficulty_var
                    elif world.prevState == "simulation":
                        if (event.key == pygame.K_LEFT or event.key == ord('a')) and world.agent.algorithm != 0:
                            world.agent.algorithm -= 1 
                        elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and world.agent.algorithm != len(world.agent.algorithm_array)-1:
                            world.agent.algorithm += 1
                    world.options()
                
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        world.update()
        world.render()
