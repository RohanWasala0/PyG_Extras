import pygame

# Your Pygame game code starts here
def run_game():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Pygame Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0)) # Fill screen with black
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_game()