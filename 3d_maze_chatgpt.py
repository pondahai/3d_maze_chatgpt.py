import pygame
import math

# 初始化Pygame
pygame.init()

# 設置顯示
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Maze Game")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# 迷宮設置
maze = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
]
tile_size = 50

# 玩家設置
player_x, player_y = 75, 75
player_angle = 0
player_speed = 2
mouse_sensitivity = 0.005

# 射線投射函數
def cast_ray(px, py, angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    for depth in range(1, 800):
        x = px + depth * cos_a
        y = py + depth * sin_a
        if maze[int(y // tile_size)][int(x // tile_size)] == 1:
            return depth, x, y
    return None, None, None

# 繪製3D視圖
def draw_3d_view():
    for col in range(width):
        angle = player_angle + math.radians(col / width * 60 - 30)
        depth, x, y = cast_ray(player_x, player_y, angle)
        if depth:
            wall_height = 5000 / (depth + 0.0001)
            color = 255 / (1 + depth * depth * 0.0001)
            pygame.draw.rect(screen, (color, color, color), (col, height // 2 - wall_height // 2, 1, wall_height))

# 檢查碰撞
def check_collision(x, y):
    if maze[int(y // tile_size)][int(x // tile_size)] == 1:
        return True
    return False

# 遊戲循環
running = True
clock = pygame.time.Clock()

# 隱藏滑鼠光標並捕捉滑鼠
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # 計算新的位置
    new_x, new_y = player_x, player_y
    if keys[pygame.K_w]:
        new_x += player_speed * math.cos(player_angle)
        new_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        new_x -= player_speed * math.cos(player_angle)
        new_y -= player_speed * math.sin(player_angle)
    if keys[pygame.K_a]:
        new_x += player_speed * math.cos(player_angle - math.pi / 2)
        new_y += player_speed * math.sin(player_angle - math.pi / 2)
    if keys[pygame.K_d]:
        new_x -= player_speed * math.cos(player_angle - math.pi / 2)
        new_y -= player_speed * math.sin(player_angle - math.pi / 2)
    
    # 檢查是否碰撞牆壁
    if not check_collision(new_x, player_y):
        player_x = new_x
    if not check_collision(player_x, new_y):
        player_y = new_y

    # 取得滑鼠移動量
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    player_angle += mouse_dx * mouse_sensitivity

    screen.fill(BLACK)
    draw_3d_view()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
