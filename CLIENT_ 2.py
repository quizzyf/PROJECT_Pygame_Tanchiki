import json
import pprint
import socket

import pygame

W, H = 600, 600
FPS = 30

pygame.init()
scr = pygame.display.set_mode((W, H))
clock_ = pygame.time.Clock()

pygame.display.set_icon(pygame.image.load('images/tanchiki/icon_tanchiki.ico'))
bg = pygame.image.load('images/tanchiki/bg_tanki.png').convert()
bg_pause = pygame.image.load('images/tanchiki/bg_pause_game_tanki.png').convert()
boost_img = pygame.image.load('images/tanchiki/boost.png').convert_alpha()
boost_img_or = pygame.image.load('images/tanchiki/boost_or.png').convert_alpha()
medkit_img_or = pygame.image.load('images/tanchiki/medkit_or.png').convert_alpha()
bullet_img = pygame.image.load('images/tanchiki/bullet_tank.png').convert_alpha()
effects_img = [pygame.image.load('images/tanchiki/effect_shield.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_slow.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_teleport.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_speed.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_-1hp.png').convert_alpha(),
               pygame.image.load('images/tanchiki/effect_+1att.png').convert_alpha()
               ]
main_disp_img = pygame.image.load('images/tanchiki/main_disp.png').convert_alpha()
medkit_img = pygame.image.load('images/tanchiki/medkit.png').convert_alpha()
nastr_spravka_bg_img = pygame.image.load('images/tanchiki/nastroiki_spravka.png').convert_alpha()
spravka_off_img = pygame.image.load('images/tanchiki/spravka.png').convert_alpha()
spravka_onl_img = pygame.image.load('images/tanchiki/spravka_online.png').convert_alpha()
tank_img, tank1_img = pygame.image.load('images/tanchiki/tank.png').convert_alpha(), \
    pygame.image.load('images/tanchiki/tank1.png').convert_alpha()
tank_razr_img, tank1_razr_img = pygame.image.load('images/tanchiki/tank1_razr.png').convert_alpha(),\
    pygame.image.load('images/tanchiki/tank2_razr.png').convert_alpha()
wall_img = pygame.image.load('images/tanchiki/wall_tank.png').convert_alpha()
zvuk_on_img, zvuk_off_img = pygame.image.load('images/tanchiki/zvuk_tanchiki_on.png').convert_alpha(),\
    pygame.image.load('images/tanchiki/zvuk_tanchiki_off.png').convert_alpha()
tank1_hp = pygame.image.load('images/tanchiki/tank1_hp.png').convert_alpha()
tank2_hp = pygame.image.load('images/tanchiki/tank2_hp.png').convert_alpha()

# upload fonts
font_schet = pygame.font.Font('Fonts/Intro.ttf', 15)
font_st_disp_errors = pygame.font.Font('Fonts/PsychicForce2012Monospaced.ttf', 20)
font_st_disp = pygame.font.Font('Fonts/PsychicForce2012Monospaced.ttf', 40)
font_sprav_main_nastr = pygame.font.Font('Fonts/PsychicForce2012Monospaced.ttf', 120)
TYPES_OF_IMAGES = {1: [tank_img, tank1_img], 2: wall_img, 3: bullet_img}


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


exist_scnd_tank = False
f_online_game = True
find_room = True
game_pause = False
while f_online_game:
    if not exist_scnd_tank:
        print('viv')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f_online_game = False
                st_ekran = False
        scr.blit(pygame.image.load('images/tanchiki/wait_for_players.png'), (0, 0))
        pygame.display.update()
        clock_.tick(FPS)
    if find_room:
        for i in [8000, 8001, 8002, 8003, 8004]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            try:
                sock.connect(('localhost', i))
                data = sock.recv(1024).decode()
                if data == 'F':
                    sock.close()
                    continue
                if data == '2':
                    print('ЕСТЬ!!!')
                    exist_scnd_tank = True
                    find_room = False
                    break
                else:
                    find_room = False
                    break
            except ConnectionRefusedError as e:
                if e.errno == 10061:
                    txt_error_online_game = 'Сервер временно не работает'
                    f_online_game = False
                    break
    data = sock.recv(1024).decode()
    if data[0] == '2':
        print('ЕСТЬ!!!!!')
        exist_scnd_tank = True
    if f_online_game and exist_scnd_tank:
        print('fdsfsd')

        TYPES_OF_IMAGES = {1: [tank_img, tank1_img], 2: wall_img, 3: bullet_img}

        old_data = []
        runnin = True
        while runnin:
            message = '<0,0>'
            message_v = '0'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runnin = False
                    f_online_game = False
                    st_ekran = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        message = '<2>'
                        message_v = '2'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_pause = True
            if game_pause:
                game_pause_f = 1
                scr.blit(bg_pause, (0, 0))
                while game_pause_f:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            st_ekran = False
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                game_pause_f = 0
                                game_pause = False
                        scr.blit(main_disp_img, (0, 0))
                        txt_su = font_sprav_main_nastr.render('Pause', True, (255, 255, 255))
                        scr.blit(txt_su, (W // 2 - txt_su.get_width() // 2, 0))
                        data = sock.recv(2 ** 24)
                        print(data)
                        pygame.display.update()
                        clock_.tick(FPS)
            elif not game_pause:
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
                data = sock.recv(2 ** 24)
                print(data)
                data = json.loads(find_inf(data))
                if data:
                    old_data = data
                pprint.pprint(data)
                # рисуем все
                scr.blit(bg, (0, 0))
                for i in old_data:
                    n_cl, num_t, x, y, hp, pos = i.values()
                    if n_cl == 1:
                        scr.blit(pygame.transform.rotate(TYPES_OF_IMAGES[n_cl][num_t - 1], (pos - 1) * 90), (x, y))
                        if num_t == 1:
                            scr.blit(tank2_hp, (W - 150, 0), ((30 * (hp - 5)), 0, 150, 30))
                        else:
                            scr.blit(tank1_hp, (0, 0), (abs(30 * (hp - 5)), 0, 150, 30))
                    if n_cl == 2:
                        scr.blit(TYPES_OF_IMAGES[n_cl], (x, y))
                    if n_cl == 3:
                        scr.blit(pygame.transform.rotate(TYPES_OF_IMAGES[n_cl], (pos - 1) * 90), (x, y))

                pygame.display.update()
                clock_.tick(FPS)