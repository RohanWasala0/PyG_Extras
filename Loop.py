import pygame 
import asyncio
import sys
from typing import Any

from Render import Render

async def loop(
    isRunning: bool,
    manager: Any = None,
    fps: float = 60.0,
):
    clock: pygame.time.Clock = pygame.time.Clock()
    while isRunning:

        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                isRunning = False

        Render(manager).render()

        pygame.display.update()
        manager.deltaTime = clock.tick(fps) / 100  # Time in seconds since last tick.
        await asyncio.sleep(0)

    if not isRunning:
        pygame.quit()
        sys.exit()