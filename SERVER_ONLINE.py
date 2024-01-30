import random as ran
import socket
import sys
import threading
import time
import pygame
import json

W, H = 600, 600
FPS = 30

pygame.init()
clock_ = pygame.time.Clock()


def foo(m_socket, port):
    class Medkit(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.name_class = 4
            self.num = 0
            self.image = pygame.Surface((40, 20))
            self.rect = self.image.get_rect()
            self.killed = False
            self.pos = 0
            self.hp = 1
            self.rect.x, self.rect.y = ran.randint(0, 9) * 60 + 5, ran.randint(1, 9) * 60 + 5
            while (pygame.sprite.spritecollide(self, walls, False) or
                   pygame.sprite.spritecollide(self, tanks, False)):
                self.rect.x, self.rect.y = ran.randint(0, 9) * 60 + 5, ran.randint(1, 9) * 60 + 5

        def update(self):
            self.num = (self.num + 0.05) % 2
            hits_medkit = pygame.sprite.spritecollide(self, tanks, False)
            if hits_medkit and hits_medkit[0].hp != 5:
                if hits_medkit[0].hp < 4:
                    hits_medkit[0].hp += 2
                else:
                    hits_medkit[0].hp = 5
                self.dokill()

        def dokill(self):
            self.killed = True
            self.kill()


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
            self.hp = 5
            self.tank_end_g = ''
            if num == 0:
                if spis_zn_tank_1 == [(0, 0), 5]:
                    self.rect.x = num * 19 * 30
                    self.rect.y = ran.randint(1, 19) * 30
                    while pygame.sprite.spritecollide(self, walls, False):
                        self.rect.x = num * 19 * 30
                        self.rect.y = ran.randint(1, 19) * 30
                    self.hp = 5
                else:
                    x, y = spis_zn_tank_1[0]
                    self.rect.x = x
                    self.rect.y = y
                    self.hp = spis_zn_tank_1[1]
            elif num == 1:
                if spis_zn_tank_2 == [(0, 0), 5]:
                    self.rect.x = num * 19 * 30
                    self.rect.y = ran.randint(1, 19) * 30
                    while pygame.sprite.spritecollide(self, walls, False):
                        self.rect.x = num * 19 * 30
                        self.rect.y = ran.randint(1, 19) * 30
                    self.hp = 5
                else:
                    x, y = spis_zn_tank_2[0]
                    self.rect.x = x
                    self.rect.y = y
                    self.hp = spis_zn_tank_2[1]
            self.speed = 2
            self.pos = 1
            self.old_pos = self.pos
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
                if self.rect.bottom > 600:
                    self.rect.bottom = 600
                self.pos = 3
            if n_x == 0 and n_y == -1:
                self.rect.y += self.speed * n_y
                if self.rect.top < 30:
                    self.rect.top = 30
                self.pos = 1

            if self.old_pos != self.pos and self.pos in [1, 3]:
                self.rect.x = round(self.rect.x / 15) * 15
            if self.old_pos != self.pos and self.pos in [2, 4]:
                self.rect.y = round(self.rect.y / 15) * 15
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
            self.hp = 1
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
            self.hp = 1
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
    medkits = pygame.sprite.Group()
    for i in range(100):
        x, y = ran.randint(0, 19) * 30, ran.randint(1, 19) * 30
        wall = Block(x, y)
        pole_of_blocks[x // 30][y // 30] = wall
        all_sprites.add(wall)
        walls.add(wall)
    tank_1 = None
    tank_2 = None
    end_of_game = False
    spis_zn_tank_1 = [(0, 0), 5]
    spis_zn_tank_2 = [(0, 0), 5]
    players = []
    runnin = True
    current_time_mk = 10
    f_medkit = False
    start_time_mk = time.time()
    shetchik_mk = 0

    error_for_off_server = 0
    f_error_for_off_server = False
    while runnin:
        # Есть ли челы ждущие входа
        try:
            new_sock, address = m_socket.accept()
            if len(tanks) < 2 and not f_error_for_off_server:
                new_sock.setblocking(False)
                print('Есть один', address, port)
                if not tank_1:
                    tank_1 = Tank(new_sock, 0)
                    all_sprites.add(tank_1)
                    tanks.add(tank_1)
                    players.append(tank_1)
                else:
                    tank_2 = Tank(new_sock, 1)
                    all_sprites.add(tank_2)
                    tanks.add(tank_2)
                    players.append(tank_2)
                slovar_of_conns[port] += 1
                for pl in players:
                    pl.sock.send(str(len(tanks)).encode())
            else:
                new_sock.send('F'.encode())
        except:
            pass
        if tank_1 or tank_2:
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
            # отправляем изменения челам
            for player in players:
                try:
                    if len(tanks) == 2:
                        sprite_data = []
                        for sprite in all_sprites:
                            sprite_dict = {
                                '1': sprite.name_class,
                                '2': int(sprite.num),
                                '3': sprite.rect.x,
                                '4': sprite.rect.y,
                                '5': sprite.hp,
                                '6': sprite.pos
                            }
                            sprite_data.append(sprite_dict)
                        mesg = json.dumps(sprite_data).encode('utf-8')
                        player.sock.send(mesg)
                        player.errors = 0
                        error_for_off_server = 0
                    else:
                        if not end_of_game:
                            player.sock.send(str(len(tanks)).encode())
                        else:
                            player.sock.send(player.tank_end_g.encode())
                except:
                    if len(tanks) == 2:
                        player.errors += 1
                        if player.errors >= 10:
                            player.sock.close()
                            players.remove(player)
                            all_sprites.remove(player)
                            tanks.remove(player)
                            if player == tank_1:
                                spis_zn_tank_1 = [(player.rect.x, player.rect.y), player.hp]
                                tank_1 = None
                            else:
                                spis_zn_tank_2 = [(player.rect.x, player.rect.y), player.hp]
                                tank_2 = None
                            print(f'Отключен {player}')
            if len(tanks) == 1:
                error_for_off_server += 1
                if error_for_off_server >= 300:
                    for player in players:
                        try:
                            player.sock.send('OFF_SERVER'.encode())
                        except:
                            pass
                        players.remove(player)
                        all_sprites.remove(player)
                        tanks.remove(player)
                        print('Сервер свободен')
                        return
            all_sprites_for_update.update()
            if len(tanks) == 2:
                if f_medkit:
                    current_time_mk = int(time.time() - start_time_mk)

                if len(medkits) < 3:
                    if current_time_mk >= 10 and shetchik_mk < 5:
                        shetchik_mk += 1
                        medkit = Medkit()
                        medkits.add(medkit)
                        all_sprites.add(medkit)
                        all_sprites_for_update.add(medkit)
                        start_time_mk = time.time()
                        current_time_mk = 0
                    f_medkit = True

                if len(medkits) >= 3:
                    current_time_mk = 0
                    start_time_mk = time.time()
                    f_medkit = False

                try:
                    pygame.sprite.groupcollide(walls, bullets, True, True)
                    if pygame.sprite.spritecollide(tank_1, bullets_t_2, True):
                        tank_1.hp -= tank_2.attack
                        if tank_1.hp == 0:
                            tank_1.tank_end_g = 'G_O_0'
                            tank_2.tank_end_g = 'G_O_1'
                            end_of_game = True
                            f_error_for_off_server = True
                    if pygame.sprite.spritecollide(tank_2, bullets_t_1, True):
                        tank_2.hp -= tank_1.attack
                        if tank_2.hp == 0:
                            tank_1.tank_end_g = 'G_O_1'
                            tank_2.tank_end_g = 'G_O_0'
                            end_of_game = True
                            f_error_for_off_server = True
                except:
                    pass
            clock_.tick(FPS)


def run_server(port):
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.bind(('0.0.0.0', port))
    main_socket.setblocking(False)
    main_socket.listen(2)
    while True:
        print(f'Сервер запущен на порту {port}')
        foo(main_socket, port)


if __name__ == '__main__':
    server_ports = [8000, 8001, 8002, 8003, 8004]
    slovar_of_conns = {i: 0 for i in server_ports}
    for port in server_ports:
        server_thread = threading.Thread(target=run_server, args=(port,))
        server_thread.start()
