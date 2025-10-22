from pygame import (
    Vector2,
    Surface, display, SRCALPHA, init,
    sprite, 
)
from typing import Any, Tuple, Set

class Manager:
    def __init__(
        self,
        screen_size: Tuple[int, int],
        world_size: Tuple[int, int] = (0, 0),
        window_caption: str = "My game",
    ):
        """Initializes the game manager with window and world settings.

        Args:
            screen_size (Tuple[int, int]): The size of the game window.
            world_size (Tuple[int, int], optional): The size of the game world. Defaults to (0, 0).
            window_caption (str, optional): The caption for the game window. Defaults to "My game".
        """
        init()
        self.deltaTime: float = 0.0

        # Window settings
        self.WINDOW_WIDTH: int = screen_size[0]
        self.WINDOW_HEIGHT: int = screen_size[1]
        self.WINDOW_SIZE: Tuple[int, int] = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.WINDOW: Surface = display.set_mode(self.WINDOW_SIZE, SRCALPHA)

        # World settings
        self.WORLD_WIDTH: int = world_size[0] if world_size[0] != 0 else self.WINDOW_WIDTH
        self.WORLD_HEIGHT: int = world_size[1] if world_size[1] != 0 else self.WINDOW_HEIGHT
        self.WORLD_SIZE: Tuple[int, int] = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.WORLD_SURFACE: Surface = Surface(self.WORLD_SIZE, SRCALPHA)

        self.INPUT_CHART = {}
        self._timers = {}

        display.set_caption(window_caption)