import pygame, sys
import random

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

res = (720, 720)
screen = pygame.display.set_mode(res)
cell_size = 5
cell_num = 100
pygame.init()



def write_text(screen, string, pos, color = (255, 0, 0)):
    font = pygame.font.Font(None, 36)
    surface = font.render(string, False, color)
    screen.blit(surface, pos)

class Snake:
    def __init__(self, color = (0, 200, 0)):
        self.color = color
        self.tail = -1
        self.bodies = []
        self.head = [0, 0]
        self.rect = pygame.rect.Rect(0, 0, cell_size, cell_size)
        self.direction = RIGHT
        self.score = 0
        self.apple = [cell_num // 2, cell_num // 2]
        self.is_dead = False

    def create_apple(self):
        self.apple = [random.randint(0, cell_num - 1), random.randint(0, cell_num - 1)]
        if self.is_collide_apple():
            self.apple = [random.randint(0, cell_num - 1), random.randint(0, cell_num - 1)]    

    def is_head_collide_apple(self):
        if self.apple == self.head:
            return True
        return False

    def is_head_collide_self(self):
        for i in range(len(self.bodies) - 1):
            if self.head == self.bodies[i]:
                return True
        return False
    
    def is_collide_apple(self):        
        for i in range(len(self.bodies) - 1):
            if self.apple == self.bodies[i]:
                return True
        return self.is_head_collide_apple()

    def move(self):
        if self.tail != -1:
            self.bodies[self.tail] = [self.head[0], self.head[1]]
            self.tail -= 1
            if self.tail == -1:
                self.tail = len(self.bodies) - 1
            
        if self.direction == LEFT:
            self.head[0] -= 1
        elif self.direction == RIGHT:
            self.head[0] += 1
        elif self.direction == UP:
            self.head[1] -= 1
        elif self.direction == DOWN:
            self.head[1] += 1

        if 0 > self.head[0]:
            self.head[0] = cell_num - 1
        elif self.head[0] > cell_num - 1:
            self.head[0] = 0
        elif 0 > self.head[1]:
            self.head[1] = cell_num - 1
        elif self.head[1] > cell_num - 1:
            self.head[1] = 0

        if self.is_head_collide_apple():
            self.eat()
            self.create_apple()
        if self.is_head_collide_self():
            self.is_dead = True

    def eat(self):
        self.bodies.append([self.head[0], self.head[1]])
        self.score += 1
        if self.tail == -1:
            self.tail = 0
                    
    def draw(self, screen):
        for i in range(len(self.bodies)):
            self.rect.x = self.bodies[i][0] * cell_size
            self.rect.y = self.bodies[i][1] * cell_size
            pygame.draw.rect(screen, self.color, self.rect)
        self.rect.x = self.head[0] * cell_size
        self.rect.y = self.head[1] * cell_size
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

        self.rect.x = self.apple[0] * cell_size
        self.rect.y = self.apple[1] * cell_size
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        write_text(screen, str(self.score), (150, 0))
        if self.is_dead:
            write_text(screen, "Game over", (res[0] // 2, res[1] // 2))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = UP
            elif event.key == pygame.K_DOWN:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = RIGHT
            
            
snake = Snake()

clock = pygame.time.Clock()
fps_limit = 30

done = False
while not done:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        snake.process_event(event)
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                snake.eat()
            if event.key == pygame.K_r:
                snake.is_dead = False
            if event.key == pygame.K_w:
                fps_limit += 1
            if event.key == pygame.K_s:
                fps_limit -= 1
            if event.key == pygame.K_d:
                cell_num += 1
            if event.key == pygame.K_a:
                cell_num -= 1
    snake.move()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (50, 50, 50), pygame.rect.Rect(0, 0, cell_num * cell_size, cell_num * cell_size))
    snake.draw(screen)
    pygame.display.update()

pygame.quit()
sys.exit()
