import pygame as p
from random import randint
from copy import deepcopy

BOX_SIZE = 50

DIMENSIONS = (10, 16)

screen = p.display.set_mode((DIMENSIONS[0]*BOX_SIZE, DIMENSIONS[1]*BOX_SIZE))
p.display.set_caption("Tetris")

clock = p.time.Clock()

class Board:
    pass

class Block:
    def __init__(self,c,r, colour):
        self.colour = colour
        self.surf = p.Surface((BOX_SIZE, BOX_SIZE))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(topleft=(c*BOX_SIZE, r*BOX_SIZE))

    def draw_block(self):
        screen.blit(self.surf, self.rect)

class Piece:
    def __init__(self):
        num = randint(0,6)
        self.rot = 0
        match num:
            case 0:
                self.shape = "I"
                colour = (0, 255, 255)
                self.blocks = [Block(3, -2, colour), Block(4, -2, colour), Block(5, -2, colour), Block(6, -2, colour)]
            case 1:
                self.shape = "O"
                colour = (255, 255, 0)
                self.blocks = [Block(4, -2, colour), Block(5, -2, colour), Block(4, -1, colour), Block(5, -1, colour)]
            case 2:
                self.shape = "J"
                colour = (0, 0, 255)
                self.blocks = [Block(3, -2, colour), Block(3, -1, colour), Block(4, -1, colour), Block(5, -1, colour)]
            case 3:
                self.shape = "L"
                colour = (255, 127, 0)
                self.blocks = [Block(4, -1, colour), Block(5, -1, colour), Block(6, -1, colour), Block(6, -2, colour)]
            case 4:
                self.shape = "Z"
                colour = (255, 0, 0)
                self.blocks = [Block(3, -2, colour), Block(4, -2, colour), Block(4, -1, colour), Block(5, -1, colour)]
            case 5:
                self.shape = "S"
                colour = (0, 255, 0)
                self.blocks = [Block(4, -1, colour), Block(5, -1, colour), Block(5, -2, colour), Block(6, -2, colour)]
            case 6:
                self.shape = "T"
                colour = (128, 0, 128)
                self.blocks = [Block(3, -1, colour), Block(4, -1, colour), Block(5, -1, colour), Block(4, -2, colour)]

    def draw_piece(self):
        for block in self.blocks:
            block.draw_block()

    def move(self, x=0, y=1):
        for block in self.blocks:
            block.rect.left += x*BOX_SIZE
            block.rect.top += y*BOX_SIZE

    def rotate(self):
        if self.rot == 4:
            self.rot = 0

        if self.rot % 2 == 0:
            even = 1
            odd = 0
        else:
            even = 0
            odd = 1

        if self.rot <= 1:
            dir = 1
        else: 
            dir = -1
        
        pivot = deepcopy(self.blocks[1].rect.topleft)

        match self.shape:
            case "I":
                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*odd*dir, pivot[1] - BOX_SIZE*even*dir)
                self.blocks[2].rect.topleft = (pivot[0] - BOX_SIZE*odd*dir, pivot[1] + BOX_SIZE*even*dir)
                self.blocks[3].rect.topleft = (pivot[0] - 2*BOX_SIZE*odd*dir, pivot[1] + 2*BOX_SIZE*even*dir)

            case "O":
                pass

            case "J":
                if self.rot == 1 or self.rot == 2:
                    ydir = 1
                else:
                    ydir = -1

                pivot = deepcopy(self.blocks[2].rect.topleft)
                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*odd*dir, pivot[1] - BOX_SIZE*even*dir)
                self.blocks[1].rect.topleft = (pivot[0] - BOX_SIZE*odd*dir, pivot[1] + BOX_SIZE*even*dir)
                self.blocks[3].rect.topleft = (pivot[0] + BOX_SIZE*dir, pivot[1] + BOX_SIZE*ydir)

            case "L":
                if self.rot == 0 or self.rot == 3:
                    xdir = 1
                else:
                    xdir = -1

                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*odd*dir, pivot[1] - BOX_SIZE*even*dir)
                self.blocks[2].rect.topleft = (pivot[0] - BOX_SIZE*odd*dir, pivot[1] + BOX_SIZE*even*dir)
                self.blocks[3].rect.topleft = (pivot[0] + BOX_SIZE*xdir, pivot[1] + BOX_SIZE*dir)

            case "Z":
                if self.rot == 1 or self.rot == 2:
                    ydir = 1
                else:
                    ydir = -1

                pivot = deepcopy(self.blocks[2].rect.topleft)
                self.blocks[3].rect.topleft = (pivot[0] - BOX_SIZE*odd*dir, pivot[1] + BOX_SIZE*even*dir)
                self.blocks[1].rect.topleft = (pivot[0] + BOX_SIZE*even*dir, pivot[1] + BOX_SIZE*odd*dir)
                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*dir, pivot[1] + BOX_SIZE*ydir)

            case "S":
                if self.rot == 0 or self.rot == 3:
                    xdir = 1
                else:
                    xdir = -1

                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*odd*dir, pivot[1] - BOX_SIZE*even*dir)
                self.blocks[2].rect.topleft = (pivot[0] + BOX_SIZE*even*dir, pivot[1] + BOX_SIZE*odd*dir)
                self.blocks[3].rect.topleft = (pivot[0] + BOX_SIZE*xdir, pivot[1] + BOX_SIZE*dir)

            case "T":
                self.blocks[0].rect.topleft = (pivot[0] + BOX_SIZE*odd*dir, pivot[1] - BOX_SIZE*even*dir)
                self.blocks[2].rect.topleft = (pivot[0] - BOX_SIZE*odd*dir, pivot[1] + BOX_SIZE*even*dir)
                self.blocks[3].rect.topleft = (pivot[0] + BOX_SIZE*even*dir, pivot[1] + BOX_SIZE*odd*dir)

        self.rot += 1
                

    def collision(self):
        left, right, down = False, False, False
        for block in self.blocks:
            # left
            if block.rect.left/BOX_SIZE == 0:
                left = True

            # right
            if block.rect.right/BOX_SIZE == DIMENSIONS[0]:
                right = True

            # down
            if block.rect.bottom/BOX_SIZE == DIMENSIONS[1]:
                down = True
        return {"left":left, "right":right, "down":down}

piece = Piece()
tick = 1
speed = 60

while True:
    collisions = piece.collision()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
        if event.type == p.KEYDOWN:
            if p.key.get_pressed()[p.K_c]:
                piece.rotate()

    if tick % speed == 0:
        if not(collisions["down"]):
            piece.move()
    tick += 1
    
    if tick % 5 == 0:
        if p.key.get_pressed()[p.K_LEFT] and not(collisions["left"]):
            piece.move(-1, 0)
        if p.key.get_pressed()[p.K_RIGHT] and not(collisions["right"]):
            piece.move(1, 0)

    screen.fill("Black")

    piece.draw_piece()
    p.display.update()

    clock.tick(60)
