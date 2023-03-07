import gymnasium as gym
import pygame
import numpy as np

window_width, window_height = 1000, 500
rotation_max, acceleration_max = 0.08, 0.5


class CustomEnv(gym.Env):
    def __init__(self):
        self.x = window_width/2
        self.y = window_height/2
        self.ang = 0.
        self.vel_x = 0.
        self.vel_y = 0.
        # self.observation_space = <gym.space >
        # self.action_space = <gym.space >

    def init_render(self):
        import pygame
        pygame.init()
        self.window = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()

    def reset(self):
        return observation

    def step(self, action=np.zeros((2), dtype=np.float64)):
        # action[0]: acceleration | action[1]: rotation

        # rotate
        self.ang = self.ang + rotation_max * action[1]
        if self.ang > np.pi:
            self.ang = self.ang - 2 * np.pi
        if self.ang < -np.pi:
            self.ang = self.ang + 2 * np.pi

        # accelarate
        acceleration = action[0]
        # backwards acceleration at half thrust
        if acceleration < 0:
            acceleration = acceleration * 0.5

        # set velocity
        self.vel_x = self.vel_x + acceleration_max * \
            acceleration * np.cos(self.ang)
        self.vel_y = self.vel_y - acceleration_max * \
            acceleration * np.sin(self.ang)

        # move
        self.x = self.x + self.vel_x
        self.y = self.y + self.vel_y

        # keep rocket on screen
        if self.x > window_width:
            self.x = self.x - window_width
        elif self.x < 0:
            self.x = self.x + window_width
        if self.y > window_height:
            self.y = self.y - window_height
        elif self.y < 0:
            self.y = self.y + window_height

        observation, reward, done, info = 0., 0., False, {}
        return observation, reward, done, info

    def render(self):
        self.window.fill((0, 0, 0))
        pygame.draw.circle(self.window, (0, 200, 200),
                           (int(self.x), int(self.y)), 6)

        # draw orientation
        p1 = (self.x - 10 * np.cos(self.ang), self.y + 10 * np.sin(self.ang))
        p2 = (self.x + 15 * np.cos(self.ang), self.y - 15 * np.sin(self.ang))
        pygame.draw.line(self.window, (0, 100, 100), p1, p2, 2)

        pygame.display.update()


def pressed_to_action(keytouple):
    action_turn = 0
    action_acc = 0

    if keytouple[pygame.K_DOWN] == 1:  # back
        action_acc -= 1
    if keytouple[pygame.K_UP] == 1:  # forward
        action_acc += 1
    if keytouple[pygame.K_LEFT] == 1:  # left  is -1
        action_turn += 1
    if keytouple[pygame.K_RIGHT] == 1:  # right is +1
        action_turn -= 1

    return np.array([action_acc, action_turn])


environment = CustomEnv()
environment.init_render()
run = True

while run:
    # set game speed to 30 fps
    environment.clock.tick(30)

    # controls
    # end while-loop when window is closed
    get_event = pygame.event.get()
    for event in get_event:
        if event.type == pygame.QUIT:
            run = False

    # get pressed keys, generate action
    get_pressed = pygame.key.get_pressed()
    action = pressed_to_action(get_pressed)

    # calculate one step
    environment.step(action)

    # render current state
    environment.render()

pygame.quit()
