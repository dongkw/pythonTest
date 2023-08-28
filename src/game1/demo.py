import pygame
import math


class hero():
    def __init__(self, x_position, y_position, length, height):
        self.x = x_position
        self.y = y_position
        self.l = length
        self.h = height
        self.player_ship = pygame.image.load("data/hero.png")  # Placeholder surface, replace with actual ship image
        # self.player_ship = pygame.transform.scale(self.player_ship, (length // 0.3, height // 0.3))  # 缩小图像
        self.angle = 0
        self.target_x = None
        self.target_y = None
        self.bullets = []  # 子弹列表

    def draw(self, win):
        cx, cy = pygame.mouse.get_pos()
        dx, dy = cx - self.x, cy - self.y
        if abs(dx) > 0 or abs(dy) > 0:
            self.angle = math.atan2(-dx, -dy) * 57.2957795

        img_copy = pygame.transform.rotate(self.player_ship, self.angle + 90)  # 旋转角度为90度

        # if dx < 0:  # 向左走时翻转图像
        #     img_copy = pygame.transform.flip(img_copy, False, True)

        rotated_rect = img_copy.get_rect(center=(round(self.x), round(self.y)))

        win.blit(img_copy, rotated_rect)
        for bullet in self.bullets:  # 绘制子弹
            bullet.draw(win)

    def move(self, x, y):
        self.target_x = x
        self.target_y = y
        dx, dy = self.target_x - self.x, self.target_y - self.y
        if abs(dx) > 0 or abs(dy) > 0:
            self.angle = math.atan2(-dx, -dy) * 57.2957795  # 计算角度

    def update(self):
        if self.target_x is not None and self.target_y is not None:
            dx, dy = self.target_x - self.x, self.target_y - self.y
            if abs(dx) > 0 or abs(dy) > 0:
                dist = math.hypot(dx, dy)
                speed = 2  # 设置移动速度
                self.x += min(dist, speed) * dx / dist
                self.y += min(dist, speed) * dy / dist
        for bullet in self.bullets:  # 更新子弹
            bullet.update(self.angle)

    def shoot(self):
        bullet = Bullet(self.x, self.y, self.angle)  # 创建子弹对象
        self.bullets.append(bullet)  # 将子弹添加到列表中

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self,angle):
        speed = 10  # 子弹速度

        self.x += math.cos(math.radians(angle)) * speed
        self.y += math.sin(math.radians(angle)) * speed

    def draw(self, win):

        pygame.draw.circle(win, (255, 0, 0), (round(self.x), round(self.y)), 5)

