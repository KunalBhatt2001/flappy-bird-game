"""
Date of completion and edit:  September 1, 2019
Developer: Gitesh Kumar

"""
"""
 *******************************************************************************************************************************

    THIS IS A FLAPPY BIRD GAME THAT IS QUITE A SIMPLE LOOKING GAME BUT IT IS A HARD GAME THAT MAY MAKE YOU TO 
    SCRATCH YOUR HEAD.....

    IN THIS PROJECT I WILL BE MAKING A SIMPLE FLAPPY BIRD GAME USING THE PYTHON LIBRARY NAMED "pygame"
    WE WILL BE USING THIS LIBRARY FOR CREATING THE BASIC INTERFACE OF THE GAME...

    LET'S GET STARTED........................ :) :)

 *******************************************************************************************************************************
"""
#pygame is imported for the making of the game
import pygame

#the module random is used for the random placing of the tubes ie. randomly placing the tubes of different height
#in the game
import random
import os
import time

#the package named neat is used for the implementation of the neural network
#used to implement the AI (Artificial Intelligence) in the game to make it 
#playable by the machine.......  
import neat

#import visualize
#import pickle
pygame.font.init()  # initialise the font

# Now we are setting the dimensions of the screen and loading of the image
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50) 
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

# this sets the window frame using its height and the width
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# it gives the name to the game window
pygame.display.set_caption("Flappy Bird")

# here we give the path where ew are storing the image of the pipe
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())

# here we give the path where we are storing the image of background
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

# here we give the path where we are storing the images of the bird
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]

# here we give the path where ew are storing the image of the base
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

# it is the initial value of the generations
gen = 0

class Bird:
    """
    Bird class representing the flappy bird
    """

    #  maximum rotation means to tilt the bird in degrees when the bird  has to mave upwards 
    #  and tilt when it has  to move downward  
    MAX_ROTATION = 25

    #  reference used to get the images of the bird
    IMGS = bird_images

    #  how much the bird rotate every time  the bird move in the game
    ROT_VEL = 20

    #  how long we are  showing the bird animation and how faster and slower the 
    #  bird will be moving
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        # here the x,y  will be representing the strating position of the bird
        self.x = x
        self.y = y

        # tilt is how much the image is to be titlted and at the beginning the value is 0 as at this time the bird is not
        # moving
        self.tilt = 0  # degrees to tilt
        
        # this deals about the physics of the bird that how many times it fell down or get up
        self.tick_count = 0

        # the velocity of the bird will be zero at the begining as the bird is not moving
        self.vel = 0


        self.height = self.y
        self.img_count = 0

        # this will be the list initial bird image when it is not moving
        self.img = self.IMGS[0]

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        """
        As we can see that the velocity value in self.vel = -10.5 is negative as in the pygame window the position of
        the (0,0) coordinates is the top left corner and the moving of the left/right and up/down is mearure in the 
        positive or negative directions

        So, the value velocity in the "X - DIRECTION" will be as usual that is its :
        1. value is positive when we are moving in the "RIGHT" side or in the right direction.
        2. value is negative when we are moving in the "LEFT" side or in the left direction.

        So, the value velocity in the "Y - DIRECTION" will be a bit unusual that is its :
        1. value is positive when we are moving in the "DOWNWARD" side or in the right direction.
        2. value is negative when we are moving in the "UPWARD" side or in the left direction.

        """
        self.vel = -10.5

        # this tick count will keep a count of when we jumped and we changed the initial value again to 0
        self.tick_count = 0

        # this will give position of the height that is from where it started moving from
        self.height = self.y

    def move(self):
        """
        make the bird move
        :return: None
        """
        # this will give position of the height that is from where it started moving from

        #here, a tick happen and a frame went by and counts how many times we move since the last jump
        self.tick_count += 1

        # for downward acceleration
        # the displacement that how many pixels we are moving up or down in this particular frame 
        # ie. we get this when we change the y position of the bird in that frame
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        """
        here , the above equation is typically a physics equation 

        in this equation,
        self.tick_count ---> it gives us the number of ticks or the number of seconds the bird is moving in the frame
                           its value is always up ie. the value of this thing always increases....
      
        this equation actually tells us based on the our current bird velocity how much we are moving up or down

        eg.  -10.5 * 1 + 1.5 * 1** 2 = -9
             "   * 2 +  "  * 2 ** 2 = -7.7
                 ............
                 ie. the value will keep on decreasing and we get an arch like trajectory of the bird
        """

        # terminal velocity
        if displacement >= 16: # here 16 represents the no of pixels ie. 16 pixels
            #this means the velocity is not too up or not too down
            displacement = (displacement/abs(displacement)) * 16 

        if displacement < 0:
            displacement -= 2  # it means that when the bird is moving up move a little bit more up

        self.y = self.y + displacement  # we will now change the y displacement with the help of this displacement

        # here we are doing the tilting of the bird ie. tilt up or tilt down
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION: 
                # here the bird is not  moved slowly upward but is moved rapidly due to the MAX_ROTATION (25 DEGREES)
                self.tilt = self.MAX_ROTATION


        else:  # tilt down
            if self.tilt > -90:
                # here the the bird will go completely down (nose down) 
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        self.img_count += 1

        # following are the se tof conditions that are used to diplay the bird images according to the 
        # context that at what time the bird will have the wings in the position   
        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # tilt the bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        """
        Do collision for our bird
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.img)


class Pipe():
    """
    represents a pipe object
    """
    GAP = 200  # represents the space in between our pipes
    VEL = 5    #  

    def __init__(self, x):

        """
        Here, we see only the x parameter as the height of the tube placed will be completely
        random....
        initialize pipe object
        :param x: int
        :return" None
        """
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is drawn
        self.top = 0
        self.bottom = 0
        
        # flipping of the pipe to get the top pipe
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)

        # to get the bottom pipe in the game 
        self.PIPE_BOTTOM = pipe_img

        self.passed = False  # this that if the pipe has passed the pipe or not

        self.set_height()

    def set_height(self):
        """
        this method will define the position of the pipe ie. where the gap of the pipe is, what is the positon
        all of this stuff is completely random
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        this method will move the pipe in the x-direction....
        here the pipe in moved in the x-direction based on the velocity of the pipe with which it move in each frame....
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    #******************************************************************************************************************************

    # MOST DIFFICULLT PART OF THE CODE IE. IMPLEMENTING THE COLLIDE ALGORITHM

    def collide(self, bird, win):
        """
        here we use mask..to check the overlapping or touching pixels
        offset = how far away are these masks are away from each other
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)  
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))  
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # caluculates the point of collision of the bird and the bottom pipe using the offset value of bottom pipe
        # returns true of false
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 

        # caluculates the point of collision of the bird and the top pipe using the offset value of top pipe
        # returns true or false
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            # if the bird collides with the top or bottom pipe the function will return "true" otherwise it will return "false"
            return True

        return False
    
    #**************************************************************************************************************************


class Base:
    """
    Represnts the moving floor of the game
    """
    VEL = 5  # should be equal to that of pipe so that they appear to move at same speed
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH     #cycle back

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH      #cycle back

    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):  # draw the elements in the game at the basic frame
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))
    

    #drawing of the pipes in the game window
    for pipe in pipes:
        pipe.draw(win)

    # drawing of the base in the game window
    base.draw(win)

    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        bird.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    global WIN, gen
    win = WIN
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''

#********************************************************************************************************************************

# IMPLEMENTING THE NEAT(NEURAL NETWORK ALGORITHM)

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """

    # all the sub headings that are used in the configuration file are listed below
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    # HERE THE "eval_genom" is the fitness function that we have to run the no of generations (in this case it is 50)
    winner = p.run(eval_genomes, 50) 

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

#***************************************************************************************************************************************

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
