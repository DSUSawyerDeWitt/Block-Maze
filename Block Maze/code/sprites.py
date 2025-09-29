from settings import *

#Should make one for Triangles and One for Squares
#Could Add a Blocks Class
class Block(pygame.sprite.Sprite):
    def __init__(self, groups, image, pos, background_sprites, game):
        super().__init__(groups)
        #self.image = image
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_frect(topleft = pos)
        self.background_sprites = background_sprites
        self.game = game
        self.holding_block = False
        #self.block_number = None

        if self.block_type == 'Square':
            flipper_image = game.flipper_surf[FLIPPER['FLIPPER_IMPORT'][self.block_number]]
            self.flipper_image = pygame.transform.scale(flipper_image, (64, 64))
            flipper_offset = FLIPPER['FLIPPER_PLACEMENT'][FLIPPER['FLIPPER_SIDE'][self.block_number]] #
            self.flipper = Flipper(self, self.flipper_image, flipper_offset)
            game.flipper_sprites.add(self.flipper)
            game.all_sprites.add(self.flipper)

    def Mouse_Clicked_Block_Check(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos) and mouse_pressed and self.game.held_block is None:
            return True
        else:
            return False

    def Mouse_Clicked_Block(self):
        self.holding_block = True
        self.game.held_block = self
        self.original_position = self.rect.center

        self.game.held_sprite.add(self)
        if self.block_type == 'Square': #change to square Later
            self.game.held_sprite.add(self.flipper)
        self.game.block_sprites.remove(self)

    def Mouse_Pressed(self, mouse_pos):
        self.rect = self.image.get_frect(center=mouse_pos)

    def Mouse_Released(self):
        closest_distance = float('inf')
        closest_tile = None
        for tile in self.background_sprites:
            tile_pos = tile.rect.center
            distance = math.sqrt((tile_pos[0] - self.rect.center[0])**2 + (tile_pos[1] - self.rect.center[1])**2)

            if distance < closest_distance:
                closest_distance = distance
                closest_tile = tile
        positions = self.game.get_all_triangle_positions()
        if closest_tile.rect.center not in positions: #If there is not another Block on this Tile
            self.rect.center = closest_tile.rect.center #Move the block to this Tile
            self.game.block_sprites.add(self)
        else: #If there is another block on this Tile
            if closest_tile.rect.center in positions:
                for block in self.game.block_sprites:
                    if block != self and block.rect.center == closest_tile.rect.center:
                        if block.block_number == self.block_number:
                            block.kill()  # Kill the block if it has the same position
                            self.rect.center = closest_tile.rect.center
                            self.game.merge_blocks(self.rect.topleft, self.block_number)
                            self.kill()
                            if self.block_type == 'Square':
                                self.flipper.kill()
                                block.flipper.kill()
                        else:
                            self.rect.center = self.original_position
                            self.game.block_sprites.add(self)

        self.holding_block = False #No longer holding a block
        self.game.held_block = None #Release the held Blocks Stats
        self.game.held_sprite.empty() #Emtpy the held_sprires group


    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if self.holding_block:#self.game.holding_block:
            if mouse_pressed:
                self.Mouse_Pressed(mouse_pos)
            else:
                self.Mouse_Released()

        elif self.Mouse_Clicked_Block_Check(mouse_pos, mouse_pressed):
             self.Mouse_Clicked_Block()

class Flipper(pygame.sprite.Sprite):
    def __init__(self, parent_block, image, offset):
        super().__init__()
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_frect()
        self.parent_block = parent_block
        self.offset = offset

        block_pos = self.parent_block.rect.topleft
        self.rect = self.image.get_frect(topleft=(
            block_pos[0] + self.offset[0],
            block_pos[1] + self.offset[1]
        ))


    def update(self, dt):
        if self.parent_block:
            block_pos = self.parent_block.rect.topleft
            self.rect.topleft = (block_pos[0] + self.offset[0], block_pos[1] + self.offset[1])

class Down_Triangle_Block(Block):
    def __init__(self, groups, triangle_image, pos, background_sprites, game):
        self.block_number = 1
        self.block_type = 'Triangle'
        super().__init__(groups, triangle_image, pos, background_sprites, game) #Calls the Parent cunstrutor.

class Down_Square_Block(Block): #Triangles for NOW
    def __init__(self, groups, block_image, pos, background_sprites, game):
        self.block_number = 2
        self.block_type = 'Square'
        super().__init__(groups, block_image, pos, background_sprites, game)

class Up_Square_Block(Block):
    def __init__(self, groups, block_image, pos, background_sprites, game):
        self.block_number = 3
        self.block_type = 'Square'
        super().__init__(groups, block_image, pos, background_sprites, game)

class Up_Triangle_Block(Block):
    def __init__(self, groups, block_image, pos, background_sprites, game):
        self.block_number = 4
        self.block_type = 'Triangle'
        super().__init__(groups, block_image, pos, background_sprites, game)

class Left_Square_Block(Block):
    def __init__(self, groups, block_image, pos, background_sprites, game):
        self.block_number = 5
        self.block_type = 'Square'
        super().__init__(groups, block_image, pos, background_sprites, game)

class Right_Square_Block(Block):
    def __init__(self, groups, block_image, pos, background_sprites, game):
        self.block_number = 6
        self.block_type = 'Square'
        super().__init__(groups, block_image, pos, background_sprites, game)

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, ball_image, pos, block_sprites, tube_sprites):
        super().__init__(groups)
        self.block_sprites = block_sprites
        self.tube_sprites = tube_sprites
        self.direction = pygame.Vector2(0,-1)
        self.image = pygame.transform.scale(ball_image, (16, 16))
        self.rect = self.image.get_frect(center = pos)
        self.inside_tube = False
        self.speed = 300
    
    def block_collision(self): #Switches direction when colliding with block
        for block in self.block_sprites:
            if block.rect.colliderect(self.rect):
                print(block.block_number) # POWER
                print(block.block_type)
                if self.direction.x > 0: #Ball moving Right
                    self.rect.right = block.rect.left
                    self.direction.x *= -1
                elif self.direction.x < 0: #Ball moving Left
                    self.rect.left = block.rect.right
                    self.direction.x *= -1
                elif self.direction.y > 0: #Ball moving Down
                    self.rect.bottom = block.rect.top
                    self.direction.y *= -1
                elif self.direction.y < 0: #Ball moving Up
                    self.rect.top = block.rect.bottom
                    self.direction.y *= -1

    def tube_collision(self): #Hits a Tube #should move this inside a Tube Class
        for tube in self.tube_sprites:
            if tube.rect.colliderect(self.rect):
                if self.direction.x > 0 and not self.inside_tube: #Right Tubes
                    if self.rect.center[0] >= tube.rect.center[0]:
                        self.inside_tube = True
                        self.rect.center = tube.rect.center
                        self.direction.y = -1
                        self.direction.x = 0
                elif self.direction.x < 0 and not self.inside_tube: #Left Tubes
                    if self.rect.center[0] <= tube.rect.center[0]:
                        self.inside_tube = True
                        self.rect.center = tube.rect.center
                        self.direction.y = 1
                        self.direction.x = 0
                        print(1)
                elif self.direction.y > 0 and not self.inside_tube: #Bottom Tubes
                    if self.rect.center[1] >= tube.rect.center[1]:
                        self.inside_tube = True
                        self.rect.center = tube.rect.center
                        self.direction.y = 0
                        self.direction.x = 1
                elif self.direction.y < 0 and not self.inside_tube: #Top Tubes
                    if self.rect.center[1] <= tube.rect.center[1]:
                        self.inside_tube = True
                        self.rect.center = tube.rect.center
                        self.direction.y = 0
                        self.direction.x = 1


    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.block_collision()
        self.tube_collision()
        self.rect.y += self.direction.y * self.speed * dt
        self.block_collision()
        self.tube_collision()

class Background_Tile(pygame.sprite.Sprite):
    def __init__(self, groups, block_image, pos):
        super().__init__(groups)
        self.image = block_image
        self.image = pygame.transform.scale(block_image, (64, 64))
        self.rect = self.image.get_frect(topleft = pos)


    def update(self, dt):
        pass

class Corner_Tube(pygame.sprite.Sprite):
    def __init__(self, groups, block_image, pos, ball_sprites, side):
        super().__init__(groups)
        self.image = block_image
        self.ball_sprites = ball_sprites
        self.side = side
        self.image = pygame.transform.scale(block_image, (64, 64))
        self.rect = self.image.get_frect(topleft = pos)

    def turn_ball(self): #Turns the ball if it hits a corner
        for ball in self.ball_sprites:
            if ball.rect.colliderect(self.rect):
                if self.side == 'Bottom Right':
                    if ball.rect.center[0] >= self.rect.center[0] and ball.direction.x == 1: #Ball moving Right
                        ball.rect.center = self.rect.center
                        ball.direction.x = TUBE['SIDE'][self.side][0] #0
                        ball.direction.y = TUBE['SIDE'][self.side][1] # -1
                    elif ball.rect.center[1] >= self.rect.center[1] and ball.direction.y == 1: #Ball moving Down
                        ball.rect.center = self.rect.center
                        ball.direction.x = TUBE['SIDE'][self.side][1] # -1
                        ball.direction.y = TUBE['SIDE'][self.side][0] # 0
                elif self.side == 'Bottom Left':
                    if ball.rect.center[0] <= self.rect.center[0] and ball.direction.x == -1: #Ball moving Left
                        ball.rect.center = self.rect.center
                        ball.direction.x = 0
                        ball.direction.y = -1
                    elif ball.rect.center[1] >= self.rect.center[1] and ball.direction.y == 1: #Ball moving Down
                        ball.rect.center = self.rect.center
                        ball.direction.x = 1
                        ball.direction.y = 0
                elif self.side == 'Top Left':
                    if ball.rect.center[0] <= self.rect.center[0] and ball.direction.x == -1:#Ball moving Left
                        ball.rect.center = self.rect.center
                        ball.direction.x = 0
                        ball.direction.y = 1
                    elif ball.rect.center[1] <= self.rect.center[1] and ball.direction.y == -1: #Ball moving Up
                        ball.rect.center = self.rect.center
                        ball.direction.x = 1
                        ball.direction.y = 0
                elif self.side == 'Top Right':
                    if ball.rect.center[0] >= self.rect.center[0] and ball.direction.x == 1: #Ball moving Right
                        ball.rect.center = self.rect.center
                        ball.direction.x = 0
                        ball.direction.y = 1
                    elif ball.rect.center[1] <= self.rect.center[1] and ball.direction.y == -1: #Ball Moving Up
                        ball.rect.center = self.rect.center
                        ball.direction.x = -1
                        ball.direction.y = 0

    def update(self, dt):
        self.turn_ball()

class Left_Exit_Tube(pygame.sprite.Sprite):
    def __init__(self, groups, image, pos, ball_sprites):
        super().__init__(groups)
        self.ball_sprites = ball_sprites
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_frect(topleft = pos)
        self.exiting_tube = False
        self.reentered = False

    def exit_tube(self):
        for ball in self.ball_sprites:
            if ball.rect.colliderect(self.rect): #Checks if the Ball reentered the same Tube.
                if ball.direction.x == -1 and not self.reentered:
                    self.reentered = True
                elif (self.rect.center[1] <= ball.rect.center[1]) and ball.direction.y == 1 and not self.reentered: #Send the Ball out, Ball moving down
                    ball.rect.center = self.rect.center
                    ball.direction.y = 0
                    ball.direction.x = 1
                    self.exiting_tube = True #The Ball is leaving the Tubes
                elif (self.rect.center[1] >= ball.rect.center[1]) and ball.direction.y == -1 and not self.reentered: #Send the Ball out, Ball moving Up
                    ball.rect.center = self.rect.center
                    ball.direction.y = 0
                    ball.direction.x = 1
                    self.exiting_tube = True #The Ball is leaving the Tubes
            elif not ball.rect.colliderect(self.rect) and self.exiting_tube: #Ball stops colliding and is now on the Game Floor
                ball.inside_tube = False #left it go back into the Tubes later
                self.exiting_tube = False
                self.reentered = False
            elif not ball.rect.colliderect(self.rect) and self.reentered: #Lets the Ball exit again next time it comes around
                self.reentered = False


    def update(self, dt):
        self.exit_tube()
                


class Bottom_Right_Corner_Tube(Corner_Tube): #Make this just Corner Class.
    def __init__(self, groups, block_image, pos, ball_sprites):
        self.side = 'Bottom Right'
        super().__init__(groups, block_image, pos, ball_sprites, self.side)

class Bottom_Left_Corner_Tube(Corner_Tube): #Make this just Corner Class.
    def __init__(self, groups, block_image, pos, ball_sprites):
        self.side = 'Bottom Left'
        super().__init__(groups, block_image, pos, ball_sprites, self.side)

class Top_Left_Corner_Tube(Corner_Tube): #Make this just Corner Class.
    def __init__(self, groups, block_image, pos, ball_sprites):
        self.side = 'Top Left'
        super().__init__(groups, block_image, pos, ball_sprites, self.side)

class Top_Right_Corner_Tube(Corner_Tube): #Make this just Corner Class.
    def __init__(self, groups, block_image, pos, ball_sprites):
        self.side = 'Top Right'
        super().__init__(groups, block_image, pos, ball_sprites, self.side)
