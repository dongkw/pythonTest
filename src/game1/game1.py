#导入所需的模块
import sys
import pygame
from random import randint
import demo



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    my_hero = demo.hero(400, 300, 50, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 鼠标左键点击
                    x, y = event.pos
                    my_hero.move(x, y)
                if event.button == 3:  # 鼠标右键点击
                    my_hero.shoot()  # 发射子弹
        my_hero.update()

        screen.fill((255, 255, 255))
        my_hero.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()