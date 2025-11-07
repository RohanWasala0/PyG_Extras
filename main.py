import pygame
import asyncio

import Loop, Manager
from Entity import Entity


class Object(metaclass=Entity):
    def __init__(self) -> None:
        self.name = "Object"
        self.transform = pygame.Vector3(16, 16, 0)
        self.color = (190, 170, 0)


Object()
manager = Manager.Manager(
    screen_size=(640, 480),
    world_size=(640, 480),
)


def main():
    print("Hello from pyg-extras!")
    print("Testing Something")

    asyncio.run(Loop.loop(isRunning=True, manager=manager))


if __name__ == "__main__":
    main()
