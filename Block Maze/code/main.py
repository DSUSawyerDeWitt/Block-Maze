from settings import *
from support import folder_importer
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Block Maze")
        self.clock = pygame.time.Clock()
        self.running = True
        self.tile_surf = folder_importer('..', 'images', 'Tiles')
        self.block_surf = folder_importer('..', 'images', 'Blocks')
        self.flipper_surf = folder_importer('..', 'images', 'Flippers')
        self.ball_surf = folder_importer('..', 'images', 'Ball')
        self.held_block = None
        self.holding_block = False

        self.all_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.held_sprite = pygame.sprite.Group()
        self.flipper_sprites = pygame.sprite.Group()
        self.triangle_sprites = pygame.sprite.Group()
        self.square_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.tube_sprites = pygame.sprite.Group()

        Ball((self.all_sprites, self.ball_sprites), self.ball_surf['BaseBall2'], (288,416), self.block_sprites, self.tube_sprites)

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                x = (col * TILE_SIZE) + 64#WINDOW_WIDTH // 2
                y = (row * TILE_SIZE) + 64#WINDOW_HEIGHT // 2
                self.background_tile = Background_Tile((self.all_sprites, self.background_sprites), self.tile_surf['Background_Tile'], (x,y))
                if row == 1 or col == 1:
                    self.triangle_block = Down_Triangle_Block((self.all_sprites, self.block_sprites, self.triangle_sprites), self.block_surf['Down_Triangle_1'], (x,y), self.background_sprites, self)
                if row == 5 and (col == 5):# or col == 4): #CHANGE THIS TO SQUARE WHEN I GET NEW SPRITES
                    self.block_1 = Down_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Down_Square_2'], (x,y), self.background_sprites, self)
                if row == 6 and col == 6:
                    self.block_4 = Left_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Left_Square_5'], (x,y), self.background_sprites, self)
        for row in range(GRID_ROWS + 2):
            for col in range(GRID_COLUMNS + 2):
                x = (col * TILE_SIZE)
                y = (row * TILE_SIZE)
                if row == 0 and (col != 0 and col != GRID_COLUMNS + 1): #Top
                    self.background_tile = Background_Tile((self.all_sprites, self.tube_sprites), self.tile_surf['Top_Tube'], (x,y))
                elif col == 0 and (row != 0 and row != GRID_ROWS + 1) and row != 3: #Left
                    self.background_tile = Background_Tile((self.all_sprites, self.tube_sprites), self.tile_surf['Left_Tube'], (x,y))
                elif col == 0 and row == 3:
                    self.background_tile = Left_Exit_Tube((self.all_sprites, self.tube_sprites), self.tile_surf['Left_Exit_Tube'], (x,y), self.ball_sprites)
                elif col == GRID_COLUMNS + 1 and (row != 0 and row != GRID_ROWS + 1): #Right
                    self.background_tile = Background_Tile((self.all_sprites, self.tube_sprites), self.tile_surf['Right_Tube'], (x,y))
                elif row == (GRID_ROWS + 1) and (col != 0 and col != GRID_COLUMNS + 1): #Bottom
                    self.background_tile = Background_Tile((self.all_sprites, self.tube_sprites), self.tile_surf['Bottom_Tube'], (x,y))
                elif row == 0 and col == 0: #Top Left Corner
                    self.background_tile = Top_Left_Corner_Tube((self.all_sprites, self.tube_sprites), self.tile_surf['Top_Left_Tube'], (x,y), self.ball_sprites)
                elif row == 0 and col == GRID_COLUMNS + 1: #Top Right Corner
                    self.background_tile = Top_Right_Corner_Tube((self.all_sprites, self.tube_sprites), self.tile_surf['Top_Right_Tube'], (x,y), self.ball_sprites)
                elif row == GRID_ROWS + 1 and col == 0: #Bottom Left Corner
                    self.background_tile = Bottom_Left_Corner_Tube((self.all_sprites, self.tube_sprites), self.tile_surf['Bottom_Left_Tube'], (x,y), self.ball_sprites)
                elif row == GRID_ROWS + 1 and col == GRID_COLUMNS + 1: #Bottom Right Corner
                    self.background_tile = Bottom_Right_Corner_Tube((self.all_sprites, self.tube_sprites), self.tile_surf['Bottom_Right_Tube'], (x,y), self.ball_sprites)




    def get_all_triangle_positions(self):
        return [block.rect.center for block in self.block_sprites]
    
    def merge_blocks(self, pos, block_number):
        if block_number == 1: #CHANGE WHEN I GET NEW SPRITES
            self.block_1 = Down_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Down_Square_2'], pos, self.background_sprites, self)
        elif block_number == 2:
            self.block_2 = Up_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Up_Square_3'], pos, self.background_sprites, self)
        elif block_number == 3:
            self.block_3 = Up_Triangle_Block((self.all_sprites, self.block_sprites, self.triangle_sprites), self.block_surf['Up_Triangle_4'], pos, self.background_sprites, self)
        elif block_number == 4:
            self.block_4 = Left_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Left_Square_5'], pos, self.background_sprites, self)
        elif block_number == 5:
            self.block_5 = Right_Square_Block((self.all_sprites, self.block_sprites, self.square_sprites), self.block_surf['Right_Square_6'], pos, self.background_sprites, self)
    
    def run(self):
        while self.running:
            dt = self.clock.tick(165) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            self.display_surface.fill('#A0A0A0')
            self.all_sprites.update(dt)
            self.background_sprites.draw(self.display_surface)
            self.triangle_sprites.draw(self.display_surface)
            self.flipper_sprites.draw(self.display_surface)
            self.square_sprites.draw(self.display_surface)
            self.held_sprite.draw(self.display_surface)
            self.ball_sprites.draw(self.display_surface)
            self.tube_sprites.draw(self.display_surface)
            pygame.display.update()



if __name__ == "__main__":
    game = Game()
    game.run()