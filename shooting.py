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

# 敵の数だけ要素を追加
enemies = []
# 弾の数だけ要素を追加
bullets = []

# リストの要素を更新
def update_list(list):
    for elem in list:
        elem.update()

# リストの要素を描画
def draw_list(list):
    for elem in list:
        elem.draw()

# リストの要素を初期化
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.is_alive:
            list.pop(i)
        else:
            i += 1

# プレイヤーを管理するクラス
class Player:
    # 初期化
    def __init__(self, x, y):
        self.x = x  # x座標
        self.y = y  # y座標
        self.size = PLAYER_SIZE  # 大きさ
        self.is_alive = True  #生きているかどうか
        
    # プレイヤーが移動するため、更新する
    def update(self):
        # ←キーが押されたらx座標、-方向へ
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        # →キーが押されたらx座標、+方向へ
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED
        # ↑キーが押されたらy座標、-方向へ
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED
        # ↓キーが押されたらy座標、+方向へ
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED
            
        # プレイヤーが領域を出ないようにする
        # 左側
        self.x = max(self.x, 0)
        # 右側
        self.x = min(self.x, pyxel.width - self.size)
        # 上端
        self.y = max(self.y, 0)
        # 下端
        self.y = min(self.y, pyxel.height - self.size)

        # スペースキーを押すと、弾をとばす
        if pyxel.btnp(pyxel.KEY_SPACE):
            # プレイヤーの位置から、少し離れて弾が置かれる
            Bullet(
                self.x + PLAYER_SIZE / 2 - BULLET_WIDTH * 2, self.y - PLAYER_SIZE * 1.5
            )
            # 効果音
            pyxel.play(0, 0)
            
    # プレイヤー（円形）を描画
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, PLAYER_COLOR)

# 弾を管理するクラス
class Bullet:
    # 初期化
    def __init__(self, x, y):
        self.x = x  # x座標
        self.y = y  # y座標
        self.w = BULLET_WIDTH  # 幅
        self.h = BULLET_HEIGHT  # 高さ
        self.is_alive = True  # 生きているかどうか
        bullets.append(self) # 弾のリスト作成
    
    # 弾がとんでいくため、更新
    def update(self):
        # 上方向に飛んでいくため、スピード分だけy座標を減らす
        self.y -= BULLET_SPEED
        # 画面より上に行くと、弾が消える
        if self.y + self.h - 1 < 0:
            self.is_alive = False
            
    # 弾（長方形）を描画
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)

# 敵を管理するクラス
class Enemy:
    # 初期化
    def __init__(self, x, y):
        self.x = x  # x座標
        self.y = y  # y座標
        self.size = ENEMY_SIZE  #大きさ
        self.is_alive = True  #生きているかどうか
        enemies.append(self)  #敵のリストを作成
        
    # 敵が移動するため、更新
    def update(self):
        # 下方向へ移動する
        self.y += ENEMY_SPEED
        # 画面より下に行くと、敵が消える
        if self.y > pyxel.height - 1 + ENEMY_SIZE:
            self.is_alive = False
            
    # 敵（丸）を描画
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, ENEMY_COLOR)

# 全体の更新処理、描画処理を管理
class App:
    def __init__(self):
        pyxel.init(200, 200)  # ゲームの領域 
        pyxel.load('resource.pyxres')  # ファイル読み込み
        self.scene = SCENE_TITLE  # ゲーム画面
        self.score = 0  # スコア
        self.player = Player(pyxel.width / 2, pyxel.height - 20)  # プレイヤークラス初期化
        pyxel.run(self.update, self.draw)  # 実行
    
    # 更新処理
    def update(self):
        # qを押すと、ゲーム終了
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
            
        # シーンの場合分け
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    # タイトルシーン
    def update_title_scene(self):
        # エンターキーを押すと、スタート
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    
    def update_play_scene(self):
        # フレーム数がENEMY_FREQUENCYで割り切れる時、敵を生成
        if pyxel.frame_count % ENEMY_FREQUENCY == 0:
            Enemy(pyxel.rndi(0, pyxel.width - ENEMY_SIZE), - ENEMY_SIZE)

        # 敵に弾が当たっているか、敵の数だけ判定する
        for enemy in enemies:
            for bullet in bullets:
                if (
                    enemy.x + enemy.size > bullet.x  # 敵と弾の位置、サイズ
                    and bullet.x + bullet.w > enemy.x - enemy.size
                    and enemy.y + enemy.size > bullet.y
                    and bullet.y + bullet.h > enemy.y - enemy.size
                ):  # 弾が敵に当たった時
                    enemy.is_alive = False  # 敵を消す
                    bullet.is_alive = False  # 弾を消す
                    pyxel.play(1, 1)  # 効果音
                    self.score += 10  # スコアを増やす
        
        # プレイヤーが敵と当たっているか、敵の数だけ判定する
        for enemy in enemies:
            if (
                self.player.x + self.player.size > enemy.x - enemy.size  # プレイヤーと敵の位置、サイズ
                and enemy.x + enemy.size > self.player.x - self.player.size
                and self.player.y + self.player.size > enemy.y - enemy.size
                and enemy.y + enemy.size > self.player.y - self.player.size
            ):  # プレイヤーが敵に当たった時
                enemy.is_alive = False  # 敵が消える
                pyxel.play(1, 1)  # 効果音
                self.scene = SCENE_GAMEOVER  # ゲームオーバー画面

        
        self.player.update()  # プレイヤーの移動、状態の更新
        update_list(bullets)  # リスト内の弾の状態を更新
        update_list(enemies)  # 敵の動きや状態を更新
        cleanup_list(enemies)  # 画面外に出た敵を消す
        cleanup_list(bullets)  # 画面外に出た弾を消す

    # ゲームオーバーになった際の更新
    def update_gameover_scene(self):
        update_list(bullets)  # リスト内の弾の状態を更新
        update_list(enemies)  # リスト内の敵の動きや状態を更新
        cleanup_list(enemies)  # 画面外に出た敵を消す
        cleanup_list(bullets)  # 画面外に出た弾を消す

        # エンターキーを押すとプレイ画面に戻る
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2  # プレイヤーの位置を初期化、画面の中央に
            self.player.y = pyxel.height - 20
            self.score = 0  # スコアリセット
            enemies.clear()  # 敵リストをリセット
            bullets.clear()  # 弾リストをリセット

    # 描画処理
    def draw(self):
        pyxel.cls(7)  # 画面を黒でクリア（塗りつぶし）
        if self.scene == SCENE_TITLE:  # タイトル画面
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:  # プレイ画面
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:  # ゲームオーバー画面
            self.draw_gameover_scene()

    # タイトル画面
    def draw_title_scene(self):
        pyxel.blt(16, 60, 0, 0, 0, 168, 12, 7)  # イメージ描画
        pyxel.text(80, 140, "PRESS ENTER", 0)  # テキスト描画

    # プレイ画面
    def draw_play_scene(self):
        pyxel.text(4, 4, "SCORE " + str(self.score), 0)  # スコア表示
        self.player.draw()  # プレイヤー表示
        draw_list(bullets)  # 弾表示
        draw_list(enemies)  # 敵表示

    # ゲームオーバー画面
    def draw_gameover_scene(self):
        pyxel.text(4, 4, "SCORE " + str(self.score), 0)  # スコア表示
        draw_list(bullets)  # 弾の描画
        draw_list(enemies)  # 敵の描画
        pyxel.text(82, 60, "GAME OVER", 0)  # ゲームオーバー表示
        pyxel.text(80, 140, "PRESS ENTER", 0)  # "PRESS ENTER" 表示


App()
