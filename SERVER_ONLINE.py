import random as ran
import socket
import sys
import threading
import time
import pygame
import json

# main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# main_socket.bind(('localhost', 10000))
# main_socket.setblocking(False)
# main_socket.listen(2)

W, H = 600, 600
FPS = 30

pygame.init()
clock_ = pygame.time.Clock()


def foo(m_socket, port):
    class Block(pygame.sprite.Sprite):
        def __init__(self, x_block, y_block):
            pygame.sprite.Sprite.__init__(self)
            self.name_class = 2
            self.num = 1
            self.pos = 1
            self.image = pygame.Surface((30, 30))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x_block, y_block
            self.hp = 1

        def update(self):
            if self.hp < 1:
                self.dokill()

        def dokill(self):
            x_t, y_t = self.rect.x // 30, self.rect.y // 30
            pole_of_blocks[x_t][y_t] = ''
            self.kill()

    class Tank(pygame.sprite.Sprite):
        def __init__(self, sock, num):
            pygame.sprite.Sprite.__init__(self)
            self.name_class = 1
            self.num = num
            self.errors = 0
            self.sock = sock
            self.image = pygame.Surface((30, 30))
            self.is_dead = False
            self.rect = self.image.get_rect()
            self.rect.x = num * 19 * 30
            self.rect.y = ran.randint(1, 19) * 30
            while pygame.sprite.spritecollide(self, walls, False):
                self.rect.x = num * 19 * 30
                self.rect.y = ran.randint(1, 19) * 30
            self.speed = 2
            self.pos = 1
            self.hp = 5
            self.shield = 0
            self.attack = 1

        def update(self, n_x=0, n_y=0, v=0):
            if v == 2:
                self.shoot()
            old_x, old_y = self.rect.x, self.rect.y
            if n_x == -1 and n_y == 0:
                self.rect.x += self.speed * n_x
                if self.rect.left < 0:
                    self.rect.left = 0
                self.pos = 2
            if n_x == 1 and n_y == 0:
                self.rect.x += self.speed * n_x
                if self.rect.right > 600:
                    self.rect.right = 600
                self.pos = 4
            if n_x == 0 and n_y == 1:
                self.rect.y += self.speed * n_y
                if self.rect.top < 30:
                    self.rect.top = 30
                self.pos = 3
            if n_x == 0 and n_y == -1:
                self.rect.y += self.speed * n_y
                if self.rect.bottom > 600:
                    self.rect.bottom = 600
                self.pos = 1
            if len(tanks) == 2:
                stolk_walls = pygame.sprite.spritecollide(self, walls, False)
                if self.num == 0:
                    stolk_tanks = pygame.sprite.collide_rect(tank_1, tank_2) if tank_1 in tanks else None
                else:
                    stolk_tanks = pygame.sprite.collide_rect(tank_2, tank_1) if tank_2 in tanks else None
                if stolk_walls or stolk_tanks:
                    self.rect.x, self.rect.y = old_x, old_y
            if self.hp <= 0:
                tanks.remove(self)
                all_sprites.remove(self)
                self.kill()

        def shoot(self):
            if not self.num:
                bull = Bullet1(self.rect.centerx, self.rect.centery, self.pos)
                all_sprites.add(bull)
                all_sprites_for_update.add(bull)
                bullets.add(bull)
                bullets_t_1.add(bull)
            else:
                bull = Bullet2(self.rect.centerx, self.rect.centery, self.pos)
                all_sprites.add(bull)
                all_sprites_for_update.add(bull)
                bullets.add(bull)
                bullets_t_2.add(bull)

    class Bullet1(pygame.sprite.Sprite):
        def __init__(self, x_bull, y_bull, pos_bull):
            pygame.sprite.Sprite.__init__(self)
            self.name_class = 3
            self.num = 1
            self.image = pygame.Surface((5, 5))
            self.rect = self.image.get_rect()
            self.pos = pos_bull
            self.speed = 10
            if pos_bull == 1:
                self.rect.bottom = y_bull
                self.rect.centerx = x_bull
            elif pos_bull == 2:
                self.rect.top = y_bull - 3
                self.rect.centerx = x_bull
            elif pos_bull == 3:
                self.rect.top = y_bull
                self.rect.centerx = x_bull
            elif pos_bull == 4:
                self.rect.bottom = y_bull + 3
                self.rect.centerx = x_bull

        def update(self):
            if self.pos == 1:
                self.rect.y -= self.speed
                if self.rect.y < 35:
                    self.kill()
            elif self.pos == 2:
                self.rect.x -= self.speed
                if self.rect.x < -5:
                    self.kill()
            elif self.pos == 3:
                self.rect.y += self.speed
                if self.rect.y > 605:
                    self.kill()
            elif self.pos == 4:
                self.rect.x += self.speed
                if self.rect.x > 605:
                    self.kill()

    class Bullet2(pygame.sprite.Sprite):
        def __init__(self, x_bull, y_bull, pos_bull):
            pygame.sprite.Sprite.__init__(self)
            self.name_class = 3
            self.num = 1
            self.image = pygame.Surface((5, 5))
            self.rect = self.image.get_rect()
            self.pos = pos_bull
            self.speed = 10
            if pos_bull == 1:
                self.rect.bottom = y_bull
                self.rect.centerx = x_bull
            elif pos_bull == 2:
                self.rect.top = y_bull - 3
                self.rect.centerx = x_bull
            elif pos_bull == 3:
                self.rect.top = y_bull
                self.rect.centerx = x_bull
            elif pos_bull == 4:
                self.rect.bottom = y_bull + 3
                self.rect.centerx = x_bull

        def update(self):
            if self.pos == 1:
                self.rect.y -= self.speed
                if self.rect.y < 35:
                    self.kill()
            elif self.pos == 2:
                self.rect.x -= self.speed
                if self.rect.x < -5:
                    self.kill()
            elif self.pos == 3:
                self.rect.y += self.speed
                if self.rect.y > 605:
                    self.kill()
            elif self.pos == 4:
                self.rect.x += self.speed
                if self.rect.x > 605:
                    self.kill()

    def find_inf(s):
        otkr = None
        for i in range(len(s)):
            if s[i] == '<':
                otkr = i
            if s[i] == '>' and otkr is not None:
                zakr = i
                res = s[otkr + 1: zakr]
                return list(map(int, res.split(',')))
        return ''

    pole_of_blocks = [['' for _ in range(20)] for _ in range(20)]
    all_sprites = pygame.sprite.Group()
    all_sprites_for_update = pygame.sprite.Group()
    tanks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bullets_t_1 = pygame.sprite.Group()
    bullets_t_2 = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    tank_1 = None
    tank_2 = None
    for i in range(100):
        x, y = ran.randint(0, 19) * 30, ran.randint(1, 19) * 30
        wall = Block(x, y)
        pole_of_blocks[x // 30][y // 30] = wall
        all_sprites.add(wall)
        walls.add(wall)
    game_f = True
    live_is = True
    game_pause = False
    players = []
    runnin = True
    while runnin:
        # Есть ли челы ждущие входа
        try:
            new_sock, address = m_socket.accept()
            if len(tanks) < 2:
                new_sock.setblocking(False)
                print('Есть один', address, port)
                if not tank_1:
                    tank_1 = Tank(new_sock, len(tanks))
                    all_sprites.add(tank_1)
                    tanks.add(tank_1)
                    players.append(tank_1)
                else:
                    tank_2 = Tank(new_sock, len(tanks))
                    all_sprites.add(tank_2)
                    tanks.add(tank_2)
                    players.append(tank_2)
                slovar_of_conns[port] += 1
            else:
                new_sock.send('F'.encode())
        except:
            pass
        # считываем команды от челов
        for player in players:
            try:
                data = player.sock.recv(1024)
                data = data.decode('utf-8')
                h = find_inf(data)
                if len(h) == 1:
                    player.update(0, 0, *h)
                else:
                    player.update(*h)

            except:
                pass
        # обработка команд от челов

        # отправляем изменения челам
        for player in players:
            try:
                sprite_data = []
                for sprite in all_sprites:
                    sprite_dict = {
                        'class': sprite.name_class,
                        'number_tank': sprite.num,
                        'x': sprite.rect.x,
                        'y': sprite.rect.y,
                        'pos': sprite.pos
                    }
                    sprite_data.append(sprite_dict)
                mesg = json.dumps(sprite_data).encode('utf-8')
                player.sock.send(mesg)
                player.errors = 0
            except:
                player.errors += 1
                if player.errors >= 150:
                    player.sock.close()
                    players.remove(player)
                    all_sprites.remove(player)
                    tanks.remove(player)
                    print('Отключен челикс')
        all_sprites_for_update.update()
        if len(tanks) == 2:
            pygame.sprite.groupcollide(walls, bullets, True, True)
            if pygame.sprite.spritecollide(tank_1, bullets_t_2, True):
                if tank_1.shield > 0:
                    tank_1.shield = -1
                else:
                    tank_1.hp -= tank_2.attack
            if pygame.sprite.spritecollide(tank_2, bullets_t_1, True):
                if tank_2.shield > 0:
                    tank_2.shield = -1
                else:
                    tank_2.hp -= tank_1.attack
        clock_.tick(FPS)


# Функция для запуска сервера
def run_server(port):
    # Создание сокета
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.bind(('localhost', port))
    main_socket.setblocking(False)
    main_socket.listen(2)
    print(f'Сервер запущен на порту {port}')
    foo(main_socket, port)


# Запуск серверов
if __name__ == '__main__':
    server_ports = [8000, 8001, 8002, 8003, 8004]
    slovar_of_conns = {i: 0 for i in server_ports}
    for port in server_ports:
        server_thread = threading.Thread(target=run_server, args=(port,))
        server_thread.start()
