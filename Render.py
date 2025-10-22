from pygame import (
    sprite, image, rect,
    Surface, Rect
)
from Entity import Entity
from Manager import Manager
from typing import List

class Render:
    def __init__(
        self,
        manager
    ):

        self.render_list: List[tuple[Surface, Rect]] = Entity.getRenderList()
        self.manager: Manager = manager

    def render(self):
        
        for entity in self.render_list:
            print(entity)
            self.manager.WORLD_SURFACE.blit(entity[0], entity[1])
    
        self.manager.WINDOW.blit(self.manager.WORLD_SURFACE, (0, 0))