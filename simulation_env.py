import pygame
import matplotlib.pyplot as plt
import numpy as np
# HI BRAD I MADE A CHANGE !!!!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Agent(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y, speed_multiplier):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Set height, width # original set to 0
        screen_size = screen_size=pygame.display.get_surface().get_size()

        agent_size = normalise_units_wall_position(input=[[0.018, 0.018]], screen_size=screen_size, conversion_type="pixels")
        self.image = pygame.Surface(agent_size[0]) # This is the size of the agent
        self.image.fill(BLACK)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        y = normalise_units_wall_position(input=[[y]], screen_size=screen_size, conversion_type="pixels")
        x = normalise_units_wall_position(input=[[x]], screen_size=screen_size, conversion_type="pixels")
        self.rect.y = y[0][0]
        self.rect.x = x[0][0]
        self.speed_multiplier = speed_multiplier

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        # NOTE: As game window gets smaller the agent can travers pixel space quicker.
        # Reduce speed multplier to stop agent moving so fast pygame cant detect collisons
        self.change_x = self.speed_multiplier * x
        self.change_y = self.speed_multiplier * y

        #print("change x = ", self.change_x)
        #print("change y = ", self.change_y)

    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):
    """ Base class for all rooms. """ # THIS IS THE PARENT

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 1"""

    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [
                 [0.0, 0.0,   1.0,  0.033, BLACK],
                 [0.0, 0.967, 1.0,  0.033, BLACK],
                 [0.487, 0.083, 0.025, 0.833, BLACK]
                 ]


        walls = normalise_units_wall_position(input=walls, screen_size=pygame.display.get_surface().get_size(), conversion_type="pixels")
                # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room2(Room):
    """This creates all the walls in room 2"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, BLACK],
                 [0, 350, 20, 250, BLACK],
                 [780, 0, 20, 250, BLACK],
                 [780, 350, 20, 250, BLACK],
                 [20, 0, 760, 20, BLACK],
                 [20, 580, 760, 20, BLACK],
                 [190, 50, 20, 500, BLACK],
                 [590, 50, 20, 500, BLACK]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room3(Room):
    """This creates all the walls in room 3"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, BLACK],
                 [0, 350, 20, 250, BLACK],
                 [780, 0, 20, 250, BLACK],
                 [780, 350, 20, 250, BLACK],
                 [20, 0, 760, 20, BLACK],
                 [20, 580, 760, 20, BLACK]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)

        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, BLACK)
            self.wall_list.add(wall)


def normalise_units_wall_position(input, screen_size, conversion_type):
    # Note pygame.display.get_surface().get_size() gets game window size
    for i, item in enumerate(input, start=0):
        for j, val in enumerate(item[0:4], start=1):

            if conversion_type == "pixels":
                if j % 2 == 0:
                    # convert y and screen hieght to pixels for normalised units between 0-1
                    input[i][j - 1] = round(val * screen_size[1])
                else:
                    input[i][j - 1] = round(val * screen_size[0])

            elif conversion_type == "normalised_units":
                if j % 2 == 0:
                    # convert y and screen hieght to pixels for normalised units between 0-1
                    input[i][j - 1] = round(val / screen_size[1], 3)
                else:
                    input[i][j - 1] = round(val / screen_size[0], 3)

    return input

def main():
    """ Main Program """

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800 , 600])

    # Set the title of the window
    pygame.display.set_caption('Maze Runner')

      # Create the agent paddle object orginal (50, 50)
    agent = Agent(x=0.062, y=0.062, speed_multiplier=5)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(agent)

    rooms = []


    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    joysticks = []
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick '", joysticks[-1].get_name(), "'")

    clock = pygame.time.Clock()

    done = False

    x = 0
    y = 0
    while not done:

        # --- Event Processing ---

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True

        #pygame.event.pump()

        x = joysticks[0].get_axis(0)
        y = joysticks[0].get_axis(1)


        if x > -0.1 and x < 0.1:
            x= 0.0

        if y > -0.1 and y < 0.1:
            y = 0.0

        # clip maximum acceleration
        speed_limit = 1
        if x < speed_limit * -1:
            x = speed_limit * -1

        elif x > speed_limit:
            x = speed_limit

        if y < speed_limit * -1:
            y = speed_limit * -1

        elif y > speed_limit:
            y = speed_limit

        print("x = ", x, " y = ", y)

        agent.changespeed(x, y)
        # gets pixels for every frame. greyscale and normalise THIS NEEDS ADDING TO AUTOENCODER PORT
        pixels = np.mean(pygame.surfarray.array3d(screen), axis=2) /255
        agent_pixels_x = [agent.rect.x, agent.rect.x + agent.rect.size[0]]
        agent_pixels_y = [agent.rect.y, agent.rect.y + agent.rect.size[1]]
        pixels[agent_pixels_x[0]:agent_pixels_x[1] + 1, agent_pixels_y[0]:agent_pixels_y[1] + 1] = 1.0
        pixels = pixels.swapaxes(1, 0)

        # print("x =", agent.rect.x," y =",agent.rect.y)
        # fig = plt.figure()
        # plt.imshow(pixels)
        # plt.colorbar()
        # plt.grid(False)
        # plt.show(block=False)
        # plt.pause(1)
        # plt.close(fig)

        # --- Game Logic ---

        agent.move(current_room.wall_list)

        if agent.rect.x < -15:
            if current_room_no == 0:
                current_room_no = 2
                current_room = rooms[current_room_no]
                agent.rect.x = 790
            elif current_room_no == 2:
                current_room_no = 1
                current_room = rooms[current_room_no]
                agent.rect.x = 790
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                agent.rect.x = 790

        if agent.rect.x > 801:
            if current_room_no == 0:
                current_room_no = 1
                current_room = rooms[current_room_no]
                agent.rect.x = 0
            elif current_room_no == 1:
                current_room_no = 2
                current_room = rooms[current_room_no]
                agent.rect.x = 0
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                agent.rect.x = 0

        # --- Drawing ---
        screen.fill(WHITE)

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
