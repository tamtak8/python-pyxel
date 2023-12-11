import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

PLAYER_SIZE = 8
PLAYER_COLOR = 5
PLAYER_SPEED = 2

BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 4

ENEMY_SIZE = 8
ENEMY_COLOR = 2
ENEMY_SPEED = 1.5
ENEMY_FREQUENCY = 9

enemies = []
bullets = []


def update_list(list):
    for elem in list:
        elem.update()


def draw_list(list):
    for elem in list:
        elem.draw()


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.is_alive:
            list.pop(i)
        else:
            i += 1


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.is_alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.size)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.size)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + PLAYER_SIZE / 2 - BULLET_WIDTH * 2, self.y - PLAYER_SIZE * 1.5
            )
            pyxel.play(0, 0)

    def draw(self):
        pyxel.circ(self.x, self.y, self.size, PLAYER_COLOR)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.is_alive = True
        bullets.append(self)

    def update(self):
        self.y -= BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.is_alive = True
        enemies.append(self)

    def update(self):
        self.y += ENEMY_SPEED
        if self.y > pyxel.height - 1 + ENEMY_SIZE:
            self.is_alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.size, ENEMY_COLOR)


class App:
    def __init__(self):
        pyxel.init(200, 200)
        pyxel.load('resource.pyxres')
        self.scene = SCENE_TITLE
        self.score = 0
        self.player = Player(pyxel.width / 2, pyxel.height - 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if pyxel.frame_count % ENEMY_FREQUENCY == 0:
            Enemy(pyxel.rndi(0, pyxel.width - ENEMY_SIZE), - ENEMY_SIZE)

        for enemy in enemies:
            for bullet in bullets:
                if (
                    enemy.x + enemy.size > bullet.x
                    and bullet.x + bullet.w > enemy.x - enemy.size
                    and enemy.y + enemy.size > bullet.y
                    and bullet.y + bullet.h > enemy.y - enemy.size
                ):
                    enemy.is_alive = False
                    bullet.is_alive = False
                    pyxel.play(1, 1)
                    self.score += 10

        for enemy in enemies:
            if (
                self.player.x + self.player.size > enemy.x - enemy.size
                and enemy.x + enemy.size > self.player.x - self.player.size
                and self.player.y + self.player.size > enemy.y - enemy.size
                and enemy.y + enemy.size > self.player.y - self.player.size
            ):
                enemy.is_alive = False
                pyxel.play(1, 1)
                self.scene = SCENE_GAMEOVER

        self.player.update()
        update_list(bullets)
        update_list(enemies)
        cleanup_list(enemies)
        cleanup_list(bullets)

    def update_gameover_scene(self):
        update_list(bullets)
        update_list(enemies)
        cleanup_list(enemies)
        cleanup_list(bullets)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            enemies.clear()
            bullets.clear()

    def draw(self):
        pyxel.cls(7)
        # self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        # pyxel.text(75, 60, "SHOOTING GAME", 0)
        pyxel.blt(16, 60, 0, 0, 0, 168, 12, 7)
        pyxel.text(80, 140, "PRESS SPACE", 0)

    def draw_play_scene(self):
        pyxel.text(4, 4, "SCORE " + str(self.score), 0)
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)

    def draw_gameover_scene(self):
        pyxel.text(4, 4, "SCORE " + str(self.score), 0)
        draw_list(bullets)
        draw_list(enemies)
        pyxel.text(82, 60, "GAME OVER", 0)
        pyxel.text(80, 140, "PRESS SPACE", 0)


App()