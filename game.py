from settings import *
from random import choice

from timer import Timer

class Game:
    def __init__(self):
        
        # General
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # Linjer
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # Block Test
        # self.block = Block(self.sprites , pygame.Vector2(3,5), 'blue')  # Plasserer "sprite" objektet som argument

        # Tetromino Test
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

        # Timer
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

    def create_new_tetromino(self):

        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        # print('timer')
        self.tetromino.move_down()

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()


    # Tegne opp grid
    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(), y),1)

        self.surface.blit(self.line_surface, (0,0))

    def run(self):

        # Timer oppdatering
        self.input()
        self.timer_update()
        self.sprites.update()

        # Opptegning
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)  # Sier hvilken "overflate/layer" jeg vil tegne opp på

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING)) # Blit = Block Image Transfer
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2,2)


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data): # Skal sette sammen forskjellige former ut ifra "BLOCK" Klassen min

        # Setup ---> Henter det den trenger av data ut ifra settings.py
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data


        # Mekke Blokkær 
        self.block = [Block(group, pos, self.color) for pos in self.block_positions]

    # Kollisjoner
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.block]
        return True if any(collision_list) else False
    
    
    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.block]
        return True if any(collision_list) else False

    # Bevegelser

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.block, amount):
            for block in self.block:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.block, 1):
            for block in self.block:
                block.pos.y += 1
        else:
            for block in self.block:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = 1
            # Lager ny tetromino når den kolliderer med bunnen
            self.create_new_tetromino()


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        # Generell opptegning
        super().__init__(group)  # Super init kan ta imot 1. argument(parameter) i dette tilfellet en gruppe. 
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # Posisjon, her har jeg med meg 2 parametere/argumenter, jeg kan da fange de via index slik som vist under:
        # x = pos[0] * CELL_SIZE
        # y = pos[1] * CELL_SIZE

        # En mer effektiv måte å gjøre det på dynamisk er å vruke Vector2 (innebygget i pygames) slik som dette:

        # Posisijon (final one):
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft = (x,y))

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        
        # Mekker det umulig å legge blokkær (tetromino's) inni hverandre vertikalt
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if  y >= ROWS:
            return True
        
        # Mekker det umulig å legge blokkær (tetromino's) inni hverandre horisontalt
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

        
        

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE