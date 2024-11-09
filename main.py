import pygame
import sys
from game_state import GameState

def main():
    pygame.init()
    game = GameState()
    
    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if game.state == config.MENU:
                    game.handle_menu_input(event)
                elif game.state == config.GAME_OVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game.state = config.MENU
            
            game.update()
            game.draw()
            
    finally:
        game.hardware.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()