import json
import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
for i in [8000, 8001, 8002, 8003, 8004]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect(('localhost', i))
    data = sock.recv(1024).decode()
    print(data)
    if data == 'F':
        sock.close()
        continue
    else:
        break

W, H = 600, 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((W, H))
clock_ = pygame.time.Clock()

tank_img, tank1_img = pygame.image.load('images/tanchiki/tank.png').convert_alpha(), \
    pygame.image.load('images/tanchiki/tank1.png').convert_alpha()
wall_img = pygame.image.load('images/tanchiki/wall_tank.png').convert_alpha()
bullet_img = pygame.image.load('images/tanchiki/bullet_tank.png').convert_alpha()
TYPES_OF_IMAGES = {1: [tank_img, tank1_img], 2: wall_img, 3: bullet_img}

bg = pygame.image.load('images/tanchiki/bg_tanki.png').convert()


def find_inf(s):
    otkr = None
    s = s.decode('utf-8')
    for i in range(len(s)):
        if s[i] == '[':
            otkr = i
        if s[i] == ']' and otkr is not None:
            zakr = i
            res = s[otkr + 1: zakr]
            return '[' + res + ']'
    return '[]'


old_data = []
runnin = True
while runnin:
    message = '<0,0>'
    message_v = '0'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnin = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                message = '<2>'
                message_v = '2'

    # считываем команду
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        message = f'<-1,0,{message_v}>'
    elif keys[pygame.K_s]:
        message = f'<0,1,{message_v}>'
    elif keys[pygame.K_w]:
        message = f'<0,-1,{message_v}>'
    elif keys[pygame.K_d]:
        message = f'<1,0,{message_v}>'
    sock.send(message.encode())
    # получаем изменения
    data = sock.recv(2**24)
    data = json.loads(find_inf(data))
    if data:
        old_data = data

    # рисуем все
    screen.blit(bg, (0, 0))
    for i in old_data:
        n_cl, num_t, x, y, pos = i.values()
        if n_cl == 1:
            screen.blit(pygame.transform.rotate(TYPES_OF_IMAGES[n_cl][num_t - 1], (pos - 1) * 90), (x, y))
        if n_cl == 2:
            screen.blit(TYPES_OF_IMAGES[n_cl], (x, y))
        if n_cl == 3:
            screen.blit(pygame.transform.rotate(TYPES_OF_IMAGES[n_cl], (pos - 1) * 90), (x, y))

    pygame.display.update()
    clock_.tick(FPS)